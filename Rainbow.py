from Crypto.Hash import MD5 
import sys # Read in from command line
import os # Exit if fail
import re #Regex

# Created by Alexander McKeown @ alexmckeown.net

#  str.encode b'str'
# byte.decode('utf-8) str
#print("Current H = "+ str(int(current_hash,32)))

# Global Var
exclude = [] # indexes to exclude
wordlist = [] # List of words
size = 0 # Size of wordlist
rSize = 0 # Size of Rainbow Table
def acceptable(user_hex):
    result = True  #Bool Value
    
    if(user_hex[:2] == "0x"):
        result = False
        print("Please remove \"0x\" from the hexadecimal")
    
    temp_str = re.sub(r'[^a-f0-9]+', '', user_hex) #Removes everything but numbers from the hex string
    
    if(temp_str != user_hex):
        result = False
        print("Please use valid hexadecmial characters e.g. 0-9 & a-f")


    if(len(temp_str)!= 32):
        result = False
        print("Please ensure that the length is indeed 32 characters")

    if(result == False):
        print("Please input a valid hexadecmial input (32 char of value of 0-9 & a-f)")

    
    return result # If it's false then it hit one of the above if triggers

def preImageFinder(desired_hash, password):
    new_word = 0
    current_hash = password.encode() # Turns str into bytes
    current_hash = MD5.new(current_hash) # Hashes bytes
    current_hash = current_hash.hexdigest() #Turns hash into hex
    counter = 0
    while counter < 4:
        #b) Reduction Function
        new_word = (int(current_hash,16) + counter) % ((size)) # Reduction Function provides an index [int]
        
    
        # Hash New word
        current_hash = wordlist[new_word].encode() # Resulting hash value is recorded as the current hash
        current_hash = MD5.new(current_hash) # Hashes bytes
        current_hash = current_hash.hexdigest() #Turns hash into hex
        counter+=1
        if(current_hash == desired_hash):
            counter+=4
        else: 
            counter+=1
    return wordlist[new_word]

def readFile():
    global wordlist, size # Global Variables Shared accross functions
    try:
        # Read in the possible Passwords & report the number of read in words
        file_in = open(str(sys.argv[1]),"r") #OPEN file
        wordlist = file_in.read().splitlines()  # List of words
        file_in.close() # Close file
        size = len(wordlist) # Word list Size

        print("Success! ",size,"Possible Passwords have been read in")
    except:
        print("Error! File " + str(sys.argv[1]) +" could not be loaded!")
        os._exit(-1) #Exit program

def outputRainbow(rTable):
    global rSize
    file_out = open("Rainbow.txt","w")
    i = 0
    while i < rSize: # rainbow table size
        file_out.write(rTable[0][i] + " : "+ rTable[1][i]+"\n")
        i+=1
    file_out.close() # Close file
    # Report to standard out the number of lines in your rainbow table
    print("Report: ", rSize ," number of lines in the rainbow table")

def bubbleSort(rTable):
    global size
    i = 0
    while i < size: # Wordlist Size
        j = 0
        while j < size-1:
            temp_arr = [[1],[1]]
            if(rTable[1][j] == "NULL" and rTable[1][j+1] != "NULL"):
                temp_arr[1][0] = rTable[1][j] #Hash
                temp_arr[0][0] = rTable[0][j] #Word

                rTable[1][j] = rTable[1][j+1] #Hash
                rTable[0][j] = rTable[0][j+1] #Word

                rTable[1][j+1] = temp_arr[1][0]
                rTable[0][j+1] = temp_arr[0][0]

            elif(rTable[1][j+1] != "NULL" and rTable[1][j] != "NULL"):
                if(rTable[1][j] > rTable[1][j+1]):
                    temp_arr[1][0] = rTable[1][j] #Hash
                    temp_arr[0][0] = rTable[0][j] #Word

                    rTable[1][j] = rTable[1][j+1] #Hash
                    rTable[0][j] = rTable[0][j+1] #Word

                    rTable[1][j+1] = temp_arr[1][0]
                    rTable[0][j+1] = temp_arr[0][0]

            
            j+=1

        i+=1

    return rTable

def generateRainbow(rTable):
    global size, rSize 
    i = 0
    while i < len(rTable[0]):
        if(i not in exclude):
            #a) Apply Hash Function
            current_hash = rTable[0][i].encode() # Turns str into bytes
            current_hash = MD5.new(current_hash) # Hashes bytes
            current_hash = current_hash.hexdigest() #Turns hash into hex

            exclude.append(i) #MARKED as used
            j = 0
            # perform reduction function 4 + 1 times
            while j < 5:
                #b) Reduction Function & c)
                new_word = (int(current_hash,16) + j) % ((size)) # Reduction Function provides an index [int]
                
                #MARK new word as used
                exclude.append(new_word)
                # Hash New word
                current_hash = rTable[0][new_word].encode() # Resulting hash value is recorded as the current hash
                current_hash = MD5.new(current_hash) # Hashes bytes
                current_hash = current_hash.hexdigest() #Turns hash into hex
                
                j+=1
                # d) Store the final hash next to the original word
                if(j == 5):
                    rTable[1][i] = current_hash
                    rSize +=1 # Get the size of the rainbow table
        i+=1
    return rTable

def main(): 
    # --- Read in the list of possible passwords --- 
    readFile()
    global wordlist, exclude, size, rSize # Global Variables Shared accross functions

    # [0] Words Row | [1] Hashes Row
    rTable = [["NULL"]*size]*2 # We know that the rTable <= wordlist
    rTable[0] = wordlist  # Add word list into the left matrix

    # --- Hash & Reduce Function ---
    rTable = generateRainbow(rTable)

    # --- Sort the rainbow table based on the hash values ---
    rTable = bubbleSort(rTable)

    # --- Ouput the list of words and corresponding hashes to a Rainbow.txt ---
    outputRainbow(rTable)

    # Get User input
    user_hex = ""
    while acceptable(user_hex) == False: 
        user_hex = input("Enter a hash value in hexadecmial format: ")

    # 1. Check if the hash value is in the rainbow table
    if(user_hex in rTable[1]):
        i = 0    
        while i < rSize:
            if(rTable[1][i] == user_hex): #Match hash
                new_word = 0
                current_hash = rTable[0][i].encode('utf-8') # Turns str into bytes
                current_hash = MD5.new(current_hash) # Hashes bytes
                current_hash = current_hash.hexdigest() #Turns hash into hex

                counter = 0
                while counter < 5:
                    #b) Reduction Function
                    new_word = (int(current_hash,16) + counter) % ((size)) # Reduction Function provides an index [int]
                    
                    # Hash New word
                    current_hash = wordlist[new_word].encode('utf-8') # Resulting hash value is recorded as the current hash
                    current_hash = MD5.new(current_hash) # Hashes bytes
                    current_hash = current_hash.hexdigest() #Turns hash into hex

                    counter+=1
                        
                i = rSize
            i+=1
        
        password = wordlist[new_word]
        print("Password is : ",password)
    else:
        i = 0
        password = "NULL"    
        while i < rSize:
            new_word = 0
            current_hash = rTable[0][i].encode('utf-8') # Turns str into bytes
            current_hash = MD5.new(current_hash) # Hashes bytes
            current_hash = current_hash.hexdigest() #Turns hash into hex

            counter = 0
            while counter < 5:
                #b) Reduction Function
                new_word = (int(current_hash,16) + counter) % ((size)) # Reduction Function provides an index [int]
                
                # Hash New word
                current_hash = wordlist[new_word].encode('utf-8') # Resulting hash value is recorded as the current hash
                current_hash = MD5.new(current_hash) # Hashes bytes
                current_hash = current_hash.hexdigest() #Turns hash into hex

                counter+=1 
                if(current_hash == user_hex):
                    counter = 5
                    i += rSize        
                    password = wordlist[new_word]

                    
            i+=1
        if(password != "NULL"):
            print("Password is : ",password)
        else:
            print(user_hex, "does not exist on the rainbow table")
      


main() #Execute above code
