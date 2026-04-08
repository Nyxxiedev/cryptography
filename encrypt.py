# import cryptography so that we can encrypt + decrypt things
from cryptography.fernet import Fernet
# import all of tkinter
from tkinter import *
# use a try except to look for the file if it exists load it if it doesnt make a key load it into a variable and save it to a file
try:
    # use a variable to say what the file name is
    filename = 'key.key'
    # open the file and read whats inside
    with open(filename, 'rb') as do:
        # save the contents to a file
        key = do.read()
# if that doesnt work
except FileNotFoundError:
    # generate a key and save it to a variable called key
    key = Fernet.generate_key()
    # open the file in write bytes
    file = open('key.key', 'wb')
    # write the key to the file
    file.write(key)
    # cl;ose the file
    file.close()
# use the key and save it to a variable again? i dont actrually know what this is doing i just know I have to do it yk?
fer = Fernet(key)
# create a function so that the button will use this
def openTheFile():
    # get the contents out of the fileName entry
    fileName = fileNameEntry.get()
    # open the file in read byte mode (I think thats what its called)
    with open(fileName, 'rb') as f:
        # read the content of the file and save it to a really longly named variable
        fileContentWhileEncrypted = f.read()
        # decrypt the information out of that variable and save it to another longly named variable
        fileContentNotEncryptedButInBytes = fer.decrypt(fileContentWhileEncrypted)
        # take that variable from before and decode it so that it doesnt have b'' around it (idk why it does that either)
        fileContentNotEncrypted = fileContentNotEncryptedButInBytes.decode()
        # delete all content from the file content text box
        fileContentBox.delete("1.0", "end")
        # put the content of the file in the newly empty file content box
        fileContentBox.insert(END,fileContentNotEncrypted)
# make a function for the button so that it will work
def saveTheFile():
    # get the content of the fileName entry again instead of a global thing cause what if they want to make a new file?
    fileName = fileNameEntry.get()
    # get the content from the fileContentBox
    fileContent = fileContentBox.get('1.0', 'end-1c')
    # open the file in Write bytes mode
    with open(fileName, 'wb') as f:
        # encode the file because we decoded it before idk
        fileContentNowNotEncryptedInBytes = fileContent.encode()
        # actually encrypt the file
        fileContentNowEncrypted = fer.encrypt(fileContentNowNotEncryptedInBytes)
        # write that down write that down
        f.write(fileContentNowEncrypted)
# make the main screen
root = Tk()
# change the geometry so that it is the size that we want it
root.geometry("400x400")
# name the screen
root.title("File Encryption Tool")
# add a label that says the same thing as the screen name because they cant read that part also put it into a different font as the rest of the things cause i said so
titleForTheScreen = Label(root, text="File Encryption Tool", font=("MS Serif",20))
# put that on the screen
titleForTheScreen.grid(columnspan=3,column=0, row=0)
# make a button to open the file
loadFileButton = Button (root, text="open", command=openTheFile)
# put the on the screen
loadFileButton.grid(column=1, row=1)
# make a button to save the file
loadFileButton = Button (root, text="save", command=saveTheFile)
# put that on the screen
loadFileButton.grid(column=2, row=1)
# make an entry so that they can put the file name there so that we know what file to open
fileNameEntry = Entry(root, width=12)
# put that on the screen
fileNameEntry.grid(column=0, row=1)
# make a big text box for the file content to go into
fileContentBox = Text(root, width=30, height=10, bg='darkgray')
# put that on the screen
fileContentBox.grid(columnspan=4, row=2)
# the main loop so that the screen doesnt dissapear
root.mainloop()