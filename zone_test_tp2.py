import random
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import *
import pygame as pg
from PIL import ImageTk, Image
import os
#
# root= Tk()
#
# winning_window = Toplevel(root)
# winning_window.title("Mon Pendu")
# winning_window.geometry("900x900")
#
# canvas = Canvas(winning_window, width=200, height=200)
# canvas.grid(row = 1, column = 1)
# img = PhotoImage(file = "Image/Le_pendu.png")
# canvas["width"]= img.width()
# canvas["height"]=img.height()
# canvas.create_image(20,20, anchor = "nw", image = img)
#
# quit=ttk.Button(winning_window, text='Quitter', command=lambda: (winning_window.destroy(), print('Ça marche')))
# quit.grid(row=3, column=1, sticky="ew")
#
# root.mainloop()


# from winsound import *
# PlaySound("sound/gaming_music.wav", SND_LOOP)

# import pygame
# pygame.mixer.init()
# pygame.mixer.music.load("sound/gaming_music.wav")
# pygame.mixer.music.play(loops=0)
#
# import tkinter as tk
# from PIL import Image, ImageTk
#
# def on_resize(event):
#     # resize the background image to the size of label
#     image = bgimg.resize((event.width, event.height), Image.ANTIALIAS)
#     # update the image of the label
#     l.image = ImageTk.PhotoImage(image)
#     l.config(image=l.image)
#
# root = tk.Tk()
# root.geometry('800x600')
#
# bgimg = Image.open('Image/western_backgroud.jpg') # load the background image
# l = tk.Label(root)
# l.place(x=0, y=0, relwidth=1, relheight=1) # make label l to fit the parent window always
# l.bind('<Configure>', on_resize) # on_resize will be executed whenever label l is resized
#
# tk.Label(root, text='Something').grid(row=0)
# e1 = tk.Entry(root)
# e1.grid(row=0, column=1)
#
# root.mainloop()
# list_words = []
# with open('Énoncé.txt', "r", encoding="UTF-8") as f:
#     for words in f:
#         for i in words.split():
#             if i.isalpha():
#                 list_words.append(i)
#
#         # for i in range(len(w)):
#         #         if w[i].isalpha():
#         #             list_words.append(words)
#
# print(list_words)
root = Tk()
words = []
my_filetypes = [('all files', '.*'), ('PNG image files', '.png')]
text_root = tk.Label(root, width= 500, height = 500, text = words)
text_root.grid(row = 1, column = 1, sticky='news')


def open_list():
    myfile = filedialog.askopenfilename(parent=root,
                                        initialdir=os.getcwd(),
                                        title="Please select a file:",
                                        filetypes=my_filetypes)
    return myfile

def input_list(file, words_list):
    try:
        with open(file.get(), "r", encoding="UTF-8") as f:
            for words in f:
                for i in words.split():
                    if i.isalpha():
                        words_list.append(i)
    except Exception:
        print("Maudit une HORREUR")

button = tk.Button(root, text="Ouvrir", command= open_list())
button.grid(row=2, column=1)
