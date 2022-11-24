#make the tictactoe game work
import random, json, glob, hashlib
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

spaces = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
name = "Bob"
moveNumber = 0
alice = []
bob = []

def pick_a_spot(spaces):
    chosen = random.randint(0, len(spaces)-1)
    letter = spaces[chosen]
    spaces.pop(chosen)
    return letter


def printtojson(tx):
    global moveNumber
    moveNumber = moveNumber + 1

    oldblock = "block" + str(moveNumber - 1) + ".json"
    #print(oldblock)
    previousblock = open(oldblock, "r")
    prevblk = previousblock.read()
    hashval = hashlib.sha256(prevblk.encode()).hexdigest()
    previousblock.close()

    nameofnewfile = "block" + str(moveNumber) +".json"
    #print(nameofnewfile)
    filewrite = open(nameofnewfile, "w")
    nnc = 0 #nonce
    condition = True
    while (condition == True):
        block = json.dumps({'TxID': moveNumber, 'Hash': hashval, "Nonce": nnc, 'Transaction': tx}, sort_keys=False, indent=4, separators=(',', ': '))
        newhashval = hashlib.sha256(block.encode()).hexdigest()
        #print(block)
        if int(newhashval,16) < 2**244:
            condition = False
        
        nnc += 1 
    filewrite.write(block)
    filewrite.close()
    return block

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('Channel-nogw0jge5').message('Bob Connected').pn_async(my_publish_callback)
            
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
    def message(self, pubnub, message):
        # Handle new message stored in message.message
        #print(message.message)
        message1= message.message
        if message1 == "Bob Connected":
            return
        #print(message1[0])
        move = ""
        if message1[0] == '{':
            move = json.loads(message1)
            print(move["Transaction"])
        letter = ""
        #print(isinstance(move, dict))
        if message1 == "game over":
            print("game over")
            quit()
        elif isinstance(move, dict):
            #is only a dict if it is a block
            enemyMoveName = move['Transaction'][0]
            enemyMoveMove = move['Transaction'][1]
            if enemyMoveName == 'Alice':
                #check if its an enemy move
                process_enemy_move(enemyMoveMove)
                Tx = ["Alice", enemyMoveMove]
                printtojson(Tx)
                #check if there is anymore in spaces
                if check_hash(move) == False:
                    print("Hash is wrong!")
                    exit()

                if len(spaces) == 0:
                    pubnub.publish().channel('Channel-nogw0jge5').message('game over').pn_async(my_publish_callback)
                    print('game over')
                    quit()
                else:
                    #if game isn't over, pick a new spot and send
                    letter = pick_a_spot(spaces)
                    Tx = [name, letter]
                    block = printtojson(Tx)
                    message = block
                    #print("noko")
                    #print(spaces)
                    pubnub.publish().channel('Channel-nogw0jge5').message(block).pn_async(my_publish_callback)

def check_hash(block):
    #print(132)
    enemyHash = block['Hash']
    #Check if the hash of block is equal to what it should be
    #print(135)
    numOfLastBlock = block['TxID'] - 1
    #print(numOfLastBlock)
    nameOfLastBlockFile = "block" + str(numOfLastBlock) + ".json"
    #print(nameOfLastBlockFile)
    LastBlock = open(nameOfLastBlockFile, "r")
    #print(139)
    prevBlock = LastBlock.read()
    #print(prevBlock)
    hashVerify = hashlib.sha256(prevBlock.encode()).hexdigest()
    if hashVerify == enemyHash:
        return True
    else:
        print("False")
        print(hashVerify)
        print(enemyHash)
        return False

def process_enemy_move(move):
    alice.append(move)
    spaces.remove(move)

def main():

    pnconfig = PNConfiguration()

    pnconfig.subscribe_key = 'sub-c-4a73beb8-6919-4861-bc1f-0059a3c34d1b'
    pnconfig.publish_key = 'pub-c-0e667023-8d63-4cbd-9f26-5c4f58a94c03'
    pnconfig.user_id = "bob"
    pubnub = PubNub(pnconfig)

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels('Channel-nogw0jge5').execute()   


if __name__ == '__main__': 
    main()
