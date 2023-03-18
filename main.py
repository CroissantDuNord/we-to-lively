import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import sv_ttk
import webbrowser
import urllib
import zipfile  
import os
import time
import shutil

# Create the main window
root = tk.Tk()
root.title("Wallpaper Engine to Lively 1.0 [PRE-RELEASE]")

# Open the github of the project
def open_link():
    webbrowser.open("https://github.com/")

# Convert the file
def convert():
    file = fd.askopenfilename() # Ask to user for the file
    with zipfile.ZipFile(file, 'r') as zip_ref: # Unzip the file
        zip_ref.extractall()
    
    file_name, file_extension = os.path.splitext(file) # Get the folder name to extarct the video later
    just_file_name = os.path.basename(file_name)
    mp4_files = [f for f in os.listdir(just_file_name) if f.endswith('.mp4')] # Find video file (background)
    try:
        shutil.copy(just_file_name + "\\" +mp4_files[0], os.curdir)
        shutil.rmtree(just_file_name)
    except:
        tk.messagebox.showerror(title="Invalid File", message="Your file is invalid, Make sure its a video background in the .mp4 format")
    


def download():
    try:
        query = urllib.parse.urlparse(download_input_box.get()).query # Get the ID of the item
        code = urllib.parse.parse_qs(query)['id'][0]
        webbrowser.open("http://steamworkshop.download/download/view/" + str(code)) # Open steamworkshop.download with the id to make the user downlaod the file
    except:
        tk.messagebox.showerror(title="Invalid URL", message="Your url is invalid, check if it contains id=*******\n\nFor example: https://steamcommunity.com/sharedfiles/filedetails/?id=1375619599....")
    
# Create the widgets
text_main = tk.Label(root, text="Wallpaper Engine to Lively [PRE-RELEASE]\n\n1.Copy & Paste the workshop page in the input box and click \"download\"\n2. Open the *.zip file using the \"Convert\" Button\n3. Open livey and enjoy \n\nNOTE: You can only download video & image & gif background", font=("Helvetica 10 bold"))
download_input_box = ttk.Entry(root, width=30)
download_button = ttk.Button(root, text="1. Download", command=download)
convert_button = ttk.Button(root, text="2. Convert", command=convert)
github_image = tk.PhotoImage(file=r"C:\Users\Nathan\Downloads\github-mark-white.png")
github_button = tk.Button(root, image=github_image, width=30, height=30, borderwidth=0, highlightthickness=0, command=open_link)

# Add the widgets to the window
text_main.pack(pady=20)
download_input_box.pack(side="left", padx=10, pady=20)
download_button.pack(side="left", padx=10, pady=20)
github_button.pack(side="right", padx=10, pady=20)
convert_button.pack(side="left", padx=10, pady=20)


sv_ttk.set_theme("dark")
# Run the main loop
root.mainloop()
