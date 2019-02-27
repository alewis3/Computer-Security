# Amanda Lewis
# Computer Security and privacy
# COSC 3325 - Dr. Shebaro
# Assignment 2

# this program uses one time pad and rc4 to encrypt messages into hexadecimal bytes

#main menu
def main():
    print("Welcome to the One Time Pad/RC4 encryptor!")
    
    # choice represents the menu choice
    choice = 0
    
    # a while loop to repeat the menu until they choose to exit
    while(choice != 3):
        print("\nWhat would you like to do?:")
        
        # boolean to make sure they put in a number
        valid = False
        while(valid == False):
            try:
                choice = int(input("1 - One Time Pad\n2 - RC4\n3 - Exit\n"))
                valid = True # valid will only be set to true if they put in a number, not triggering a ValueError
            except ValueError as e:
                print("Error: Value not an integer!: ", e)  
            # extra if statement to make sure number is in range 
            if(choice < 0 or choice > 3):
                print("Invalid choice! What would you like to do?")
                valid = False # if number out of range, then set valid to false
        
        #option 1 is to encrypt with oneTimePad
        if(choice == 1): 
            # create ptext and key variable
            ptext = ""
            key = ""
            # while loop around inputs to make sure the ptext length is equal to key length
            while(ptext == "" or len(ptext) != len(key)):
                # only ask for ptext if it is an empty string
                if(ptext == ""):
                    ptext = input("What would you like to encrypt?\n")
                length = len(ptext)
                while(len(ptext) == 0):
                    print("Invalid choice, message cannot be empty!")
                    ptext = input("What would you like to encrypt?\n")

                # ask for a key
                keyPrompt = "What would you like the key to be?\n"
                key = input(keyPrompt)
                # if the lengths do not match, print an error
                if(length != len(key)):
                    print("Invalid choice! Please enter a key that is exactly " , len(ptext) , " characters long!\n")
            # create a list for the ascii values of the key
            keyList = []
            for i in key:
                keyList.append(ord(i)) # convert to ascii values
            # encrypt using oneTimePad
            ctext = oneTimePad(ptext, keyList)
            ptextDecrypted = decodeOneTimePad(ctext, keyList)
            # print encrypted message
            print("\n Original Plain text: " , ptext, "\nCipher text: ", ctext,"\nDecrypted Message: ", ptextDecrypted)
            
        # option 2 is to decrypt the cipher text in cipehertext.txt
        elif(choice == 2):
            # create ptext and key variable
            ptext = ""
            key = ""
            # while loop around inputs to make sure the ptext and key are not empty string
            while((ptext or key) == ""):
                ptext = input("What would you like to encrypt?\n")
                while(len(ptext) == 0):
                    print("Invalid choice, message cannot be empty!")
                    ptext = input("What would you like to encrypt?\n")
                key = input("What would you like the key to be? Please enter a short key!\n")
                while(len(key) < 1):
                    print("Invalid choice, key cannot be empty!")
                    key = input("What would you like the key to be? Please enter a short key!\n")

            # encrypt using rc4, and then one time pad
            longKey = rc4(ptext, key)
            ctext = oneTimePad(ptext, longKey)
            ptextDecrypted = decodeOneTimePad(ctext, longKey)
            # print encrypted message
            print("\n Original Plain text: " , ptext, "\nCipher text: ", ctext, "\nDecrypted Message: ", ptextDecrypted)


            
    # goodbye message       
    print("\nThank you for using the One Time Pad/RC4 Encryptor! \nGoodbye!")
    
# s = ' '.join(format(ord(x), 'b') for x in "Hello")
# t = chr(int(t[:8], 2))

# oneTimePad takes a plaintext message and a key that are the same length
# and encrypts by xoring the ascii values of the letters together
def oneTimePad(ptext, key):
    
    # check if ptext length and key length are the same
    # (they should be, because I check in my main program but just in case)
    if(len(ptext) != len(key)):
        print("Error: key given is different length than message!")
    # if they are the same, do the encryption
    else:
        # create empty ctext string
        ctext = ""
        # create index variable
        index = 0
        # while loop to run until the end of the ptext/key
        while(index < len(ptext)):
            # convert ptext to number using ord() (ascii values)
            ptextNum = ord(ptext[index])
            # get the key index number
            keyNum = key[index]
            # xor the values
            newNum = ptextNum ^ keyNum
            # convert to hexadecimal
            newLetter = hex(newNum)
            # disregard the "0x" (first two characters) and only take the numbers
            if(len(newLetter) == 3):
                ctext += "0" + newLetter[2]
            elif(len(newLetter) == 4):
                ctext += newLetter[2:4]
            # increment the index
            index += 1
        return ctext
    
# decodeOneTimePad will check the decrypted message 
# is the same as the encrypted one    
def decodeOneTimePad(ctext, key):
    
    # create index variable
    index = 0
    # create ptext empty string
    ptext = ""
    # while loop to run while the index is less than length of key
    # (ctext is in hexadecimal and will have two characters to represent a byte)
    while(index < len(key)):
        # get start and end index to splice string
        startIndex = int(2 * index)
        endIndex = int(startIndex + 2)
        # splice string using start and end index
        ctextSplice = ctext[startIndex:endIndex]
        # convert to int with base 16
        ctextNum = int(ctextSplice, 16)
        # get the key number from key list
        keyNum = key[index]
        # xor the numbers together
        newNum = ctextNum ^ keyNum 
        # convert number to letter using chr() (ascii value)
        newLetter = chr(newNum)
        #add letter to ptext
        ptext += newLetter
        # increment index
        index += 1
    
    # return ptext    
    return ptext
        
# rc4 algorithm to create keystream
def rc4(ptext, key):
    # Phase 1
    # initialize the permutation
    
    # create lists s and t
    s = []
    t = []
    # populate lists
    for i in range(0,256):
        s.append(i)
        t.append(charToNum(key[i % len(key)]))
    
    # initialize j
    j = 0
    
    # begin swapping process
    for i in range (0,256):
        j= (j + s[i]+ t[i]) % 256
        swap(s[i], s[j])
    
    # set i and j to 0
    i = 0    
    j = 0
    index = 0
    longKey = []
    # at each step, swap elements in table and select keystream byte
    while(index < len(ptext)):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        swap(s[i], s[j])
        t = (s[i] + s[j]) % 256
        val = s[t]
        # add to long key list
        longKey.append(val)
        index += 1
    
    # return the longkey   
    return longKey
   
# swap() takes two elements and will put 
# i in j's old place, and j in i's old place
def swap(i, j): 
    temp = j
    j = i
    i = temp
 
# charToNum will convert a character into a number
# between 0 and 25 
def charToNum(char):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    num = 0
    # find the letter in the alphabet
    for letter in alphabet:
        if letter == char:
            break
        else:
            num+=1
    return num # return the position it is found at

# numToChar will convert a number to the
# corresponding letter in the alphabet
def numToChar(num):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return alphabet[num] # return letter at that position

main()