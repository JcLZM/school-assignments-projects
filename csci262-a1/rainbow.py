import hashlib
from operator import itemgetter
import sys

#reduction function
#reduc with string
def reducStr(password, sizeOfPasswordFile):
    #string, int or bigint?
    hash = hashlib.md5(password.encode()).hexdigest()
    
    return int(hash,16) % sizeOfPasswordFile 

def reducHash(hash, sizeOfPasswordFile):
    return int(hash,16) % sizeOfPasswordFile 

#read a file

def fileProcess(file):
    if len(file) == 0:
        file = "Passwords.txt"
        print("No Passwords file entered. Defaulting to Passwords.txt.")
    f = open(file, "r")
    count = 0
    list1 = []
    while True:
        line = f.readline()
        line = line.strip()
        if not line: 
            break
        elif(len(line) == 0):
            break
        else:
            count +=1 
            #SNo, pw, hash, boolean to say whether it is used
            list_temp = [count, line, hashlib.md5(line.encode()).hexdigest(), False]
            list1.append(list_temp)
    f.close()
    return list1, count

def generateRainbowTable(list1, sizeOfPasswordFile):
    #check if boolean is True, if true, skip.
    rainbowTable = []
    for i in list1:
        if i[3] != True:
            #print(i)
            hashvalue = hashlib.md5(i[1].encode()).hexdigest()
            reduction = reducHash(hashvalue, sizeOfPasswordFile)#first reduction
            #print(reduction)
            #print(list[reduction][3])
            #print(list1[reduction][3])
            list1[reduction][3] = True
            reduction2 = reducHash(list1[reduction][2],sizeOfPasswordFile) #second reduction
            #print(reduction2)
            list1[reduction2][3] = True
            reduction3 = reducHash(list1[reduction2][2], sizeOfPasswordFile) #third reduction
            list1[reduction3][3] = True
            reduction4 = reducHash(list1[reduction3][2], sizeOfPasswordFile) #4th
            list1[reduction4][3] = True
            reduction5 = reducHash(list1[reduction4][2], sizeOfPasswordFile) #5th
            list1[reduction5][3] = True
            rainbowTable.append([i[1], list1[reduction5][2]])
            i[3] = True
    #print(rainbowTable)
    return rainbowTable

def takeInputHash():
    value = input("Please enter a hash value: ")
    while len(value) != 32:
        if value == "q":
            break
        value = input("The value you entered is not of the correct length. Please enter a 32 character string, or q to exit\n")
    return value

def checkRainbowTable(hash, table):
    hashFound = False
    foundIndex = -1000000
    for i in table:
        if hash == i[1]:
            #compare against hashes in rainbowtable
            hashFound = True
            foundIndex = i
        if hash < i[1]:
        #hash is sorted, if hash value has gone below the value in rainbowtable, will not be found.
            break
    return hashFound, foundIndex



def main():
    filename = ""
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    print(filename)
    list1, sizeOfPasswordFile = fileProcess(filename)


    #a = reducHash(hashlib.md5("freehold".encode()).hexdigest(), 15)
    #aa = reducStr("mundane", 15)

    #print(a)  #should be 8
    #print(aa)  #should be 6

    rainbowTable = generateRainbowTable(list1, sizeOfPasswordFile)

    """
    #verification
    f = open("noko.txt", "w")
    #print(sizeOfPasswordFile)
    for i in list1:
        f.write(str(i[0])+ " " + str(i[1]) + " " + str(i[2])+ " " + str(i[3]))
        f.write("\n")
    f.close()
    """

    #sort rainbowtable list by hashval
    sortedRainbow = sorted(rainbowTable, key=itemgetter(1))
    print("There are " + str(len(sortedRainbow)) + " items in the rainbow table.")
    f = open("rainbow.txt" , "w")
    for i in sortedRainbow:
        f.write(str(i[0])+ " " + str(i[1]))
        f.write("\n")
    f.close()
    #take input
    input = takeInputHash()

    #check if hash is in rainbowtable
    hashFound = False
    password = ""
    hashFound, index = checkRainbowTable(input, sortedRainbow)
    if hashFound == True:
        print("Value found in RainbowTable", end = "\n\n")
        #print(index)
        password = index[0]
        #print(password)
    else:
        print("Value not found in rainbowTable", end = "\n\n")
    
        


    #test with (found in rainbowTable)
    #6625735202758c173adaee496f6344d5 (fledgling)
    #66e9d91f0fa2b8bf79e42fae019ea4d8 (quadripartite)
    
    #if not found in rainbowTable
    #reduce (5 times)
    hashval = input
    #test with e3af082cc2ec644830a69ddafe5abe31 (reduce twice) (smell)
    #1e7c765a3b0446e6dba13f170c4b53dd (reduce 4 times) (walkie)

    #print(hashval)
    if hashFound == False:
        for i in range (0, 5):
            reduction = reducHash(hashval, sizeOfPasswordFile)
            hashFound, index = checkRainbowTable(list1[reduction][2], sortedRainbow)
            if hashFound == True:
                print("Found after reducing ", end="")
                print(i+1, end="")
                print(" times!")
                password = index[0]
                break
                
                #print(hashval)
            elif hashFound != True:
                hashval = list1[reduction][2]   
    
    if hashFound == True:
        print("The pre-image password is ", end = "")
        print(password, end="")
        print(".")
    else: 
        print("The hash is invalid.")

        

if __name__ == "__main__":
    main()
