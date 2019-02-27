# Amanda Lewis
# Computer Security and privacy
# COSC 3325 - Dr. Shebaro
# Assignment 1

# constant variables for the plain text file and cipher text file
ENCRYPT_PATH = "plaintext.txt"
DECRYPT_PATH = "ciphertext.txt"

#main menu
def main():
    print("Welcome to the Caesar Cipher Encryptor/Decryptor!\n")
    
    # choice represents the menu choice
    choice = 0
    
    # a while loop to repeat the menu until they choose to exit
    while(choice != 4):
        print("What would you like to do?:")
        
        # boolean to make sure they put in a number
        isInt = False
        while(isInt == False):
            try:
                choice = int(input("1 - Encrypt\n2 - Decrypt\n3 - Break\n4 - Exit\n"))
                isInt = True # isInt will only be set to true if they put in a number, not triggering a ValueError
            except ValueError as e:
                print("Error: Value not an integer!")   
            if(choice < 0 or choice > 4):
                print("Invalid choice! What would you like to do?")
                isInt = False
        
        #option 1 is to encrypt the text in plaintext.txt
        if(choice == 1): 
            # set isInt to false until they enter a valid value for n
            isInt = False
            while(isInt == False):
                # try/catch to make sure they enter an int
                try:
                    n = int(input("What would you like the key to be?\n"))
                    isInt = True
                    # if to catch invalid int values
                    if(n > 25 or n < 0):
                        print("Invalid choice! please enter a number between 0 and 25!")
                        isInt = False
                except ValueError as e:
                    print("Error: Value not an integer! ")
                
                
            # finally, if they enter a valid value for n, call encrypt(n)
            encrypt(n)
            
        # option 2 is to decrypt the cipher text in cipehertext.txt
        elif(choice == 2):
            # set isInt to false until they enter a valid value for n
            isInt = False
            while(isInt == False):
                # try/catch to make sure they enter an int
                try:
                    n = int(input("What is the key?\n"))
                    isInt = True
                    # if to catch invalid int values
                    if(n > 25 or n < 0):
                        print("Invalid choice! please enter a number between 0 and 25!")
                        isInt = False
                except ValueError as e:
                    print("Error: Value not an integer! ", e)
                
            # finally, if they enter a valid value for n, call decrypt(n)
            decrypt(n)
        # choice 3 calls breakCode() to attempt to discover the key of ciphertext.txt    
        elif(choice == 3):
            breakCode()
            
    # goodybe message       
    print("\nThank you for using the Caesar Cipher Encryptor/Decryptor!\nGoodbye!")

# encrypt takes an int n which it uses as the key for the caesar cipher
# it writes the contents of plaintext.txt to ciphertext.txt in encrypted form
def encrypt(n):
    
    # letter dictionary has the letters as the key, and the number equivalent as the value
    letterDictionary = getLetterDictionary()
    # number dictionary has the number value as the key and the letter equivalent as the value
    numberDictionary = getNumberDictionary()
    
    # open files to read and write
    fileToRead = open(ENCRYPT_PATH, "r")
    fileToWrite = open(DECRYPT_PATH, "w")
    
    # for loop to read all lines in the file
    for line in fileToRead:
        # for loop to walk thru the characters in each line
        for ch in line:
            # if it is not a letter, leave it alone and just write to the file
            if(ch.isalpha() == False):
                fileToWrite.write(ch)
            # if it is a letter convert to lowercase, then encrypt that letter
            else:
                ch = ch.lower()
                charNum = letterDictionary[ch] # get the number associated with the letter
                encryptNum = (charNum + n) % 26 # add n and mod by 26 to get a number between 0-25
                encryptLetter = numberDictionary[encryptNum]
                fileToWrite.write(encryptLetter)
    # when whole file is encrypted, print a message to the user            
    print(ENCRYPT_PATH , " encrypted!")   
    
    # close files 
    fileToWrite.close(),
    fileToRead.close(),
    
# decrypt takes an int n which it uses to decrypt the caesar cipher
# it writes the contents of ciphertext.txt to plaintext.txt in decrypted form
def decrypt(n):
    
    # letter dictionary has the letters as the key, and the number equivalent as the value
    letterDictionary = getLetterDictionary()
    # number dictionary has the number value as the key and the letter equivalent as the value
    numberDictionary = getNumberDictionary()
    
    # open files to read and write
    fileToRead = open(DECRYPT_PATH, "r")
    fileToWrite = open(ENCRYPT_PATH, "w")
    
    # for loop to read all lines in the file
    for line in fileToRead:
        # for loop to walk thru the characters in each line
        for ch in line:
            # if it is not a letter, leave it alone and just write to the file
            if(ch.isalpha() == False):
                fileToWrite.write(ch)
            # if it is a letter, convert to lowercase and decrypt
            else:
                ch = ch.lower()
                # get the number value of the letter
                charNum = letterDictionary[ch]
                # subtract the key from it and mod by 26 to get a number between 0 and 25
                decryptNum = (charNum - n) % 26
                decryptLetter = numberDictionary[decryptNum]
                fileToWrite.write(decryptLetter)
                
    print(DECRYPT_PATH , " decrypted!")
    
    # close the files
    fileToWrite.close()
    fileToRead.close()
    
def decryptGuess(n):
    
    # letter dictionary has the letters as the key, and the number equivalent as the value
    letterDictionary = getLetterDictionary()
    # number dictionary has the number value as the key and the letter equivalent as the value
    numberDictionary = getNumberDictionary()
    
    # open file to read
    fileToRead = open(DECRYPT_PATH, "r")
    
    # for loop to read all lines in the file
    for line in fileToRead:
        # for loop to walk thru the characters in each line
        for ch in line:
            # if it is not a letter, leave it alone and just print it
            if(ch.isalpha() == False):
                print(ch, end="") # use end="" to get multiple chars on the same line, no newline
            # if it is a letter convert it and print it
            else:
                ch = ch.lower()
                charNum = letterDictionary[ch]
                decryptNum = (charNum - n) % 26
                decryptLetter = numberDictionary[decryptNum]
                print(decryptLetter, end="")
    
    # loop to ask user if it is decrypted            
    yesOrNo = ""
    while(yesOrNo != "y" and yesOrNo != "n"):
        yesOrNo = input("\nIs this decrypted? (Enter y/n): \n")
    
    # return true if they say yes
    if(yesOrNo == "y"):
        retBool = True
    # false if they say no
    else:
        retBool = False
    
    # close file
    fileToRead.close()
    
    return retBool

# this function is designed to try the top key guesses, 
# which are determined by analyzing letter count and trying to match
# top letters in ciphertext.txt to the top letter counts of the 
# english language
def breakCode():
    
    # letter dictionary has the letters as the key, and the number equivalent as the value
    letterDictionary = getLetterDictionary()    
    
    # getTopLetters() will get a list of the top 5 
    # letters found in ciphertext.txt
    topLetterList = getTopLetters()
    # topLetters is a list with the top 5 most common
    # letters found in english language
    topLetters = ["e", "t", "a", "o", "i"]
    
    # boolean to stay in loop until key is found
    keyFound = False
    
    # while loop to search top values for n
    while(keyFound == False): 
        # for loop to go thru top letters in ciphertext.txt
        for i in topLetterList:
            # another for to go thru top letters in eng language
            for j in topLetters:
                # the key guess is derived by taking the number value of a 
                # top letter from ciphertext.txt and subtracting the number
                # values of the top letters in eng language and then mod 26
                # to get a value between 0 and 25
                keyGuess = (letterDictionary[i] - letterDictionary[j]) % 26
                print("\n", keyGuess, " is the key I'm guessing...\n")
                # call decryptGuess() and send in keyGuess
                keyFound = decryptGuess(keyGuess)
                # If the user input says it was decrypted, then break
                if(keyFound == True):
                    key = keyGuess
                    break
            # another break if key was true
            if(keyFound == True):
                break
        # this if stmt/for loop is an exhaustive search in case
        # the top letter algorithm did not turn up the correct key
        if(keyFound == False):
            for l in range(0, 25+1):
                keyFound = decryptGuess(l)
                if(keyFound == True):
                    key = l
                    break
    # finally, use the key that was found to decrypt
    decrypt(key)

# function that takes a letter and counts the number 
# of times it appears in ciphertext.txt
def countLetter(letter):
    
    count = 0
    fileToRead = open(DECRYPT_PATH, "r")
    
    for line in fileToRead:
        for ch in line:
            if(ch == letter):
                count = count + 1
                    
    fileToRead.close()
    return count

# function that will return a dictionary of all the letters in 
# ciphertext.txt with value of their letter counts
def getLetterCounts():
    
    letterCount = {}
    letterDictionary = getLetterDictionary()
    
    # run thru all letters in letterDictionary
    for key in letterDictionary:
        # send in each letter to countLetter
        count = countLetter(key)
        # assign key/value pairs in dictionary
        letterCount[key] = count

    return letterCount

# this function will analyze the result of getLetterCounts()
# and return the 5 highest letter counts in ciphertext.txt
def getTopLetters():
    
    letterCount = getLetterCounts()
    
    # variables to store max letter counts
    max1 = 0
    max2 = 0
    max3 = 0
    max4 = 0
    max5 = 0
    
    # variables to keep track of which letters 
    # have the top letter counts
    letter1 = ""
    letter2 = ""
    letter3 = ""
    letter4 = ""
    letter5 = ""
    
    # for loop to walk thru all the letters in letterCount
    for key in letterCount:
        # get the count for a particular letter
        count = letterCount[key]
        # if the count is higher than max 1
        if(count > max1):
            
            # these next 4 if statements are to switch the contents of 
            # max1 all the way to max4 down a slot if they are not just 0
            if(max1 != 0):
                if(max2 != 0):
                    if(max3 != 0):
                        if(max4 != 0):
                            max5 = max4
                            letter5 = letter4
                        max4 = max3
                        letter4 = letter3
                    max3 = max2
                    letter3 = letter2
                max2 = max1
                letter2 = letter1
                
            # assign letter1 to be key and max1 to be count
            letter1 = key
            max1 = count
        
        # if the count is not as high as max1 but still above max2    
        elif(count > max2):
            
            # these next 3 if statements are to switch the contents of 
            # max2 all the way to max4 down a slot if they are not just 0
            if(max2 != 0):
                if(max3 != 0):
                    if(max4 != 0):
                        max5 = max4
                        letter5 = letter4
                    max4 = max3
                    letter4 = letter3
                max3 = max2
                letter3 = letter2
            
            # assign letter2 to be key and max2 to be count
            letter2 = key
            max2 = count
            
        # if count is not as high as max2 but still above max3
        elif(count > max3):
            
            # these next 2 if statements are to switch the contents of 
            # max3 all the way to max4 down a slot if they are not just 0
            if(max3 != 0):
                if(max4 != 0):
                    max5 = max4
                    letter5 = letter4
                max4 = max3
                letter4 = letter3
            
            # assign letter3 to be key and max3 to be count
            letter3 = key
            max3 = count
            
        # if count is not as high as max3 but still above max4
        elif(count > max4):
            
            # this if statement is to switch the contents of max4
            # down a slot if max4 is not just 0
            if(max4 != 0):
                max5 = max4
                letter5 = letter4
                
            # assign letter4 to be key and max4 to be count
            letter4 = key
            max4 = count
            
        # if count is not as large as max1-4 but still above max5
        elif(count > max5):
            # assign letter5 to be key and max5 to be count
            letter5 = key
            max5 = count
    
    # create a list with the top letters, in order
    letterList = [letter1, letter2, letter3, letter4, letter5]
    return letterList

# this function returns a dictionary of key value pairs where the key is 
# the letter and the value is a number value, 0-25
def getLetterDictionary():
    
    letterDictionary = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j":9 , "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}
    return letterDictionary

# this function returns a dictionary of key value pairs with the number (0-25)
# as the key and the associated letter as the value
def getNumberDictionary():
    
    numberDictionary = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h",8:"i",9:"j",10:"k",11:"l",12:"m",13:"n",14:"o",15:"p",16:"q",17:"r",18:"s",19:"t",20:"u",21:"v",22:"w",23:"x",24:"y",25:"z"}
    return numberDictionary

# run main
main()