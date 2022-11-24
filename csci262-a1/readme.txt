To use the file:
1. ensure you have python3 installed
2. navigate to the directory containing the script
3. place the file containing passwords into the same directory as the script.
4. run the command in command line as follows
"python3 rainbow.py [filename of passwords file]"
if a passwords file has not been entered, it will default to Passwords.txt

Reduction function
------------------------------------
The reduction function is written in lines 7-14 of the program, under the method "reducHash()". 
When the method is invoked, it takes in a hashed value, and a number that is equal to the number of passwords in the passwords file.
The hash value then undergoes modulo, by the size of the password file, which is the total number of passwords contained in Passwords.txt

    The equation is as follows: 
        r = MD5(password) mod sizeOfPasswordFile

    where,
        r = reduction function (result)
        MD5(password) = hash value of the password you intend to reduce.
        sizeOfPasswordFile = total number of passwords in Passwords.txt