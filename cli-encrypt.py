# import cryptography so that we can encrypt + decrypt things
from cryptography.fernet import Fernet
# use a try except to look for the file if it exists load it if it doesnt make a key load it into a variable and save it to a file
try:
    # use a variable to say what the file name is
    filename = 'key.key'
    # open the file and read whats inside
    with open(filename, 'rb') as do:
        # read the content from the file and save to variable
        key = do.read()
# if that doesnt work
except FileNotFoundError:
    # generate a key and save it to a variable called key
    key = Fernet.generate_key()
    # open the file in write bytes
    file = open('key.key', 'wb')
    # write the key to the file
    file.write(key)
    # close the file
    file.close()
# use the key and save it to a variable again? i dont actrually know what this is doing i just know I have to do it yk?
fer = Fernet(key)

# make a function to encrypt a file
def encryptAFile():
    # ask what file they want to encrypt
    print("what file do you want to encrypt?")
    # get input as a string so that I can easily use it later
    wantedFileToEncrypt = str(input())
    # read the wanted file as read bytes because you cant just read it normally for some reason?
    WantedFile = open(wantedFileToEncrypt, "rb")
    # actually read the content and save it to a file
    fileContents = WantedFile.read()
    # enctrypt the contents of the file
    wantedFileNowEncrypted = fer.encrypt(fileContents)
    # close the file
    WantedFile.close()
    # open the file again but in write bytes this time
    WantedFile = open(wantedFileToEncrypt, "wb")
    # write the encrypted content
    WantedFile.write(wantedFileNowEncrypted)
    # close the file
    WantedFile.close()

# make a function to open the file
def decryptAFile():
    # ask what file they want to decrypt
    print("what file do you want to decrypt?")
    # take input and save it to a file
    wantedFileToDecrypt = str(input())
    # open the file in read mode
    WantedFile = open(wantedFileToDecrypt, "rb")
    # actually read the content of the file
    fileContents = WantedFile.read()
    # decrypt the content of the file and save it to a variable
    wantedFileNowDecrypted = fer.decrypt(fileContents)
    # close the file
    WantedFile.close()
    # open the file in write bytes this time
    WantedFile = open(wantedFileToDecrypt, "wb")
    # write the decrypted content
    WantedFile.write(wantedFileNowDecrypted)
    # close the file
    WantedFile.close()

def whatTheyWantToDo():
    # ask what they would like to do
    print("what would you like to do?")
    # take input and save it as an intager to a variable
    wantToDo = int(input())
    # see if it is equal to 1
    if wantToDo == int(1):
       # if it is encrypt a file
       encryptAFile()
    # if its 2 then
    elif wantToDo == int(2):
       # decrypt a file
       decryptAFile()
    # if its neither that wasnt an option are u stupid?
    else:
       # say that is want an optiuon
       print("wasnt an option")
       # ask them again
       whatTheyWantToDo()
# start the program
whatTheyWantToDo()