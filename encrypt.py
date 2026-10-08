from cryptography.fernet import Fernet, InvalidToken
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# This file is where the secret key lives, very secure right? don't lose it or you will loose everything else, actually are you gonna use this enough to need to not loose it?
KEY_FILE = "key.key"

# Reuse the key if we have one cuz stuff and shit
try:
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    # make a key and save it for next time cuz we need one for the encrypting thing
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

# set up Fernet so we can encrypt and decrypt stuff, not entirely sure what its doing but we need it
fer = Fernet(key)

# these are the colors for the dark mode cuz black text on white is boring
COLORS = {
    "background": "#0b1020",
    "panel": "#111a2e",
    "panel_light": "#18243b",
    "border": "#263550",
    "text": "#e7edff",
    "muted": "#98a8c7",
    "accent": "#7895ff",
    "accent_hover": "#91a8ff",
    "editor": "#0d1629",
}


def openTheFile():
    # get the file name from the box so we know what to open
    file_name = fileNameEntry.get().strip()
    if not file_name:
        messagebox.showwarning("Choose a file", "Enter a file path or use Browse first.")
        return

    try:
        # read the file and decrypt it, gotta use bytes for some reason
        with open(file_name, "rb") as encrypted_file:
            decrypted_content = fer.decrypt(encrypted_file.read()).decode()
    except InvalidToken:
        # maybe this isnt the right key or maybe this isnt encrypted idk
        messagebox.showerror(
            "Could not decrypt file",
            "This file could not be decrypted with the current key. "
            "Check that it is encrypted and that key.key is the matching key.",
        )
        statusText.set("Could not decrypt this file.")
        return
    except UnicodeDecodeError:
        # this box only shows text files, not sure what else it would show
        messagebox.showerror(
            "Unsupported file",
            "The decrypted contents are not valid text and cannot be shown in the editor.",
        )
        statusText.set("This editor supports text files only.")
        return
    except OSError as error:
        # something went wrong opening the file, computers are weird sometimes
        messagebox.showerror("Could not open file", str(error))
        statusText.set("Could not open the selected file.")
        return

    # clear the box and put the readable stuff in there
    fileContentBox.delete("1.0", tk.END)
    fileContentBox.insert(tk.END, decrypted_content)
    statusText.set(f"Decrypted {file_name}")


def saveTheFile():
    # get the file name again in case they changed it or something
    file_name = fileNameEntry.get().strip()
    if not file_name:
        messagebox.showwarning("Choose a file", "Enter a file path or use Browse first.")
        return

    # get the text, end-1c skips the extra newline tkinter puts in for some reason
    content = fileContentBox.get("1.0", "end-1c")
    try:
        # encrypt it and save it to the file, thats the whole point right
        with open(file_name, "wb") as encrypted_file:
            encrypted_file.write(fer.encrypt(content.encode()))
    except OSError as error:
        messagebox.showerror("Could not save file", str(error))
        statusText.set("Could not save the selected file.")
        return

    statusText.set(f"Encrypted and saved {file_name}")


def browseForFile():
    # let them pick a file instead of typing the whole thing
    file_name = filedialog.askopenfilename(title="Choose a text file")
    if file_name:
        fileNameEntry.delete(0, tk.END)
        fileNameEntry.insert(0, file_name)
        fileNameEntry.focus_set()


def openOnEnter(event):
    # pressing enter opens the file cuz thats what enter does i guess
    if event.keysym == "Return":
        openTheFile()


def configureStyles():
    # use this theme so the colors work, apparently the default one ignores us
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    # set the styles for all the bits on the screen
    style.configure(".", font=("TkDefaultFont", 10))
    style.configure("App.TFrame", background=COLORS["background"])
    style.configure("Panel.TFrame", background=COLORS["panel"])
    style.configure(
        "Title.TLabel",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=("TkDefaultFont", 23, "bold"),
    )
    style.configure(
        "Subtitle.TLabel",
        background=COLORS["background"],
        foreground=COLORS["muted"],
        font=("TkDefaultFont", 10),
    )
    style.configure(
        "Section.TLabel",
        background=COLORS["panel"],
        foreground=COLORS["text"],
        font=("TkDefaultFont", 10, "bold"),
    )
    style.configure(
        "Hint.TLabel",
        background=COLORS["panel"],
        foreground=COLORS["muted"],
        font=("TkDefaultFont", 9),
    )
    style.configure(
        "Status.TLabel",
        background=COLORS["panel"],
        foreground=COLORS["muted"],
        font=("TkDefaultFont", 9),
    )
    style.configure(
        "Path.TEntry",
        fieldbackground=COLORS["editor"],
        foreground=COLORS["text"],
        bordercolor=COLORS["border"],
        lightcolor=COLORS["border"],
        darkcolor=COLORS["border"],
        padding=(10, 9),
    )
    # make the main button stand out cuz its the main one
    style.configure(
        "Primary.TButton",
        background=COLORS["accent"],
        foreground="#0b1020",
        borderwidth=0,
        padding=(16, 10),
        font=("TkDefaultFont", 10, "bold"),
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLORS["accent_hover"]), ("pressed", COLORS["accent"])],
    )
    style.configure(
        "Secondary.TButton",
        background=COLORS["panel_light"],
        foreground=COLORS["text"],
        borderwidth=1,
        bordercolor=COLORS["border"],
        padding=(12, 9),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", COLORS["border"]), ("pressed", COLORS["panel_light"])],
    )
    # make the scrollbar match too or it looks weird
    style.configure(
        "Dark.Vertical.TScrollbar",
        background=COLORS["panel_light"],
        troughcolor=COLORS["editor"],
        bordercolor=COLORS["editor"],
        arrowcolor=COLORS["muted"],
    )


# make the window, this is where all the stuff goes
root = tk.Tk()
root.title("File Encryption")
root.geometry("760x640")
root.minsize(560, 500)
root.configure(background=COLORS["background"])
configureStyles()

# let the window grow when you make it bigger, dont know why it needs this
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

header = ttk.Frame(root, style="App.TFrame", padding=(32, 30, 32, 20))
header.grid(row=0, column=0, sticky="ew")
header.columnconfigure(0, weight=1)

# add the title and the little bit of text underneath it
ttk.Label(header, text="File Encryption", style="Title.TLabel").grid(
    row=0, column=0, sticky="w"
)
ttk.Label(
    header,
    text="Encrypt and decrypt text files with your local Fernet key.",
    style="Subtitle.TLabel",
).grid(row=1, column=0, sticky="w", pady=(6, 0))

panel = ttk.Frame(root, style="Panel.TFrame", padding=22)
panel.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 32))
panel.columnconfigure(0, weight=1)
# let the text box get bigger too cuz thats probably useful
panel.rowconfigure(3, weight=1)

ttk.Label(panel, text="FILE", style="Section.TLabel").grid(
    row=0, column=0, sticky="w", pady=(0, 9)
)

pathRow = ttk.Frame(panel, style="Panel.TFrame")
pathRow.grid(row=1, column=0, sticky="ew")
pathRow.columnconfigure(0, weight=1)

fileNameEntry = ttk.Entry(pathRow, style="Path.TEntry")
fileNameEntry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
# make enter open the file too because buttons arent the only way to do things
fileNameEntry.bind("<Return>", openOnEnter)
ttk.Button(
    pathRow, text="Browse", style="Secondary.TButton", command=browseForFile
).grid(row=0, column=1)

actions = ttk.Frame(panel, style="Panel.TFrame")
actions.grid(row=2, column=0, sticky="ew", pady=(18, 18))
# add buttons for opening and saving the file, hopefully obvious which is which
ttk.Button(
    actions, text="Open & Decrypt", style="Secondary.TButton", command=openTheFile
).pack(side="left")
ttk.Button(
    actions, text="Encrypt & Save", style="Primary.TButton", command=saveTheFile
).pack(side="left", padx=(10, 0))

editorFrame = ttk.Frame(panel, style="Panel.TFrame")
editorFrame.grid(row=3, column=0, sticky="nsew")
editorFrame.columnconfigure(0, weight=1)
editorFrame.rowconfigure(0, weight=1)

# make the big text box and give it the dark colors like the rest
fileContentBox = tk.Text(
    editorFrame,
    wrap="word",
    undo=True,
    background=COLORS["editor"],
    foreground=COLORS["text"],
    insertbackground=COLORS["text"],
    selectbackground=COLORS["accent"],
    selectforeground=COLORS["text"],
    relief="flat",
    borderwidth=0,
    padx=14,
    pady=14,
    font=("TkFixedFont", 11),
)
fileContentBox.grid(row=0, column=0, sticky="nsew")
# add a scrollbar so you can get to the bottom of a long file
scrollbar = ttk.Scrollbar(
    editorFrame,
    orient="vertical",
    command=fileContentBox.yview,
    style="Dark.Vertical.TScrollbar",
)
scrollbar.grid(row=0, column=1, sticky="ns")
fileContentBox.configure(yscrollcommand=scrollbar.set)

footer = ttk.Frame(panel, style="Panel.TFrame")
footer.grid(row=4, column=0, sticky="ew", pady=(14, 0))
footer.columnconfigure(0, weight=1)
statusText = tk.StringVar(value="Ready | choose a file to get started.")
# show what the app is doing down here
ttk.Label(footer, textvariable=statusText, style="Status.TLabel").grid(
    row=0, column=0, sticky="w"
)
ttk.Label(
    footer,
    text="Keep key.key safe it is required to decrypt your files.",
    style="Hint.TLabel",
).grid(row=1, column=0, sticky="w", pady=(5, 0))

# keep the window open so it doesnt just disappear
root.mainloop()
