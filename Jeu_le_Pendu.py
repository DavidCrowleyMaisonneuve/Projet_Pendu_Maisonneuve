import random
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import *
import pygame as pg
from PIL import ImageTk, Image
import os


#dictionnaire des textes
MSG = {"choice":"\nEntrer la difficulté :\n1 - Facile\n 2 - Normal\n  3 - Difficile\n ",
       "error": "\nERREUR; Le choix doit être valide, (1, 2 ou 3) ",
       "choiceALD": "Choissez une autre lettre que vous n'avez pas choisi, merci!",
       "choiceONE":"Le choix doit être une seule lettre",
       "choiceNOTL":"Ceci n'est pas une lettre!",
       "welcome": "Bienvenu au jeu Mon Pendu\n(liste par default à introduire est, 'liste_pendu.txt')",
       "trynow": "\nMaintenant essayer de deviner le mot suivant!",
       "guess" : "\nDeviner une lettre: ",
       "guessed":"\nLettres devinées : ",
       "guess_used":"\n Lettres utilisées :",
       "win": "\nGagnant; le mot est ",
       "winnner": "\nBravo !!! Vous avez GAGNE !!!",
       "notIN": "Cette lettre n'est pas dans le mot, réessayer !",
       "bravo": "Bravo, cette lettre est dans le mot!",
       "loose": "\nDésoler, vous avez perdu !!\n",
       "again": "Voulez-vous rejouer une partie ? (oui ou non) : ",
       "good_guess":"Excellent! Choissez une autre lettre et valider!",
       "game_info": "(Pour quitte le mode plein écran <Escape> et l'activer <F11>)"
                    "\nInformation sur la partie en cours :"}


class Pendu_Tkinter_game():

    def __init__(self):
        pg.mixer.init()

        self.disclaimer = open("Énoncé.txt","r", encoding="UTF-8").readlines()
        self.guess_letters = []
        self.secret_word = "_"
        self.unveil_word = [c if c in self.guess_letters else "_" for c in self.secret_word]
        self.victory = 0
        self.try_left = None
        self.bg_default ='light goldenrod'
        self.font_default = ('Comic Sans MS', 15, 'bold')

        self.root = Tk()
        self.root.title("Jeu : Mon Pendu", )
        self.root.geometry("800x800")
        self.main_window(self.root)

    def main_window(self, root):
        main_frame = Frame(root)
        main_frame.pack(fill = BOTH, expand = 1)
        left_canvas = Canvas(main_frame)
        left_canvas.pack(side = LEFT, fill = BOTH, expand = 1)
        vsb = ttk.Scrollbar(main_frame, orient = VERTICAL, command = left_canvas.yview)
        vsb.pack(side = RIGHT, fill = Y)
        left_canvas.configure(yscrollcommand = vsb)
        left_canvas.bind('<Configure>', lambda e: left_canvas.configure(scrollregion = left_canvas.bbox("all")))
        scnd_frame = Frame(left_canvas)
        left_canvas.create_window((0,0), window = scnd_frame, anchor = 'nw')

        enonce_label = Label(scnd_frame, background ="white", text ="".join(self.disclaimer),font = ('Verdana',10), justify = LEFT)
        enonce_label.grid(row = 0, column =0)

        button_go = tk.Button(root,bg = 'green', fg = 'white', text="Continuer",
                                   command = lambda: self.open_game_window())
        button_go.pack(fill = X )

        button_quit = tk.Button(root,bg = 'red',fg = 'white', text='Quitter', command = self.quit)
        button_quit.pack(fill = X )

    def open_game_window(self):
        self.music_play("sound/good_bad_ugly.mp3", -1)

        game_window = Toplevel(self.root)
        game_window.title("Mon Pendu")
        game_window.geometry("700x950")
        game_window.configure(background = self.bg_default)

        self.set_img_Label(game_window,"Image/western_backgroud.jpg", 700 , 600)

        title_game = tk.Label(game_window, bg = self.bg_default, text ="MON PENDU",
                              font = ('Comic Sans MS', 20, 'bold'))
        title_game.grid(row = 2, column = 1)

        quit = tk.Button(game_window,bg = 'red',fg = 'white',text='Quitter',
                         command = lambda : (game_window.destroy(),pg.mixer.music.unload()))
        quit.grid(row = 4, column = 1, sticky = "se")

        self.choice_window(game_window, MSG["choice"], self.set_difficulty, 1)

    def set_img_Label(self,window, img_file, x , y):

        self.img = ImageTk.PhotoImage(Image.open(img_file).resize((x, y), Image.ANTIALIAS))
        game_canvas = Canvas(window, width = self.img.width(), height = self.img.height(), bg = self.bg_default)
        game_canvas.grid(row = 1, column = 1)
        game_canvas.create_image(0, 0, anchor=NW, image=self.img)

    def choice_window(self, current_window_game, message, do_something, choice = None, entry_msg= None):

        choice_frame = tk.LabelFrame(current_window_game, font = self.font_default,
                                     text= message, relief = GROOVE, bg = self.bg_default)
        choice_frame.grid(row = 2, column = 1, sticky="ew")

        choice_entry = tk.Label(choice_frame, text = "Votre choix :" ,bg = 'deep sky blue', fg = "black",
                                font = self.font_default)
        choice_entry.grid(row = 2, column = 1, sticky="sw")
        space = tk.Label(choice_frame, width = 10, height = 3, bg = self.bg_default)
        space.grid(row = 1, column = 1)

        entry_text = StringVar()
        self.user_entry = tk.Entry(choice_frame, width=20,font = self.font_default,  textvariable = entry_text)
        self.user_entry.grid(row=2, column=2, sticky="sw", ipady=1)
        if choice == 1:
            entry_text.trace("w", lambda *args: self.char_limiter(entry_text))
        else:
            self.user_entry.insert(tk.END, entry_msg)

        validate = tk.Button(choice_frame, text="Valider", bg = 'Forest green', fg = "White",
                             font = ('Comic Sans MS', 15, 'bold'),
                             command = lambda: (do_something(entry_text, choice_frame, current_window_game)))
        validate.grid(row = 2, column = 3, sticky = "w")

    def char_limiter(self,zone):
        if len(zone.get()) > 0:
            zone.set(zone.get()[-1])

    def set_difficulty(self, choice, current_game_frame, mainframe):
                self.difficulty = 0
                if choice.get() =="":
                       pass
                elif choice.get() == '1':
                    self.difficulty = 10
                elif choice.get() == "2" :
                    self.difficulty = 6
                elif choice.get() == "3" :
                    self.difficulty = 4
                else:
                    print(MSG["error"])
                    x = ttk.Label(current_game_frame, text = MSG["error"])
                    x.grid(row = 2, column = 1, sticky = "w")

                if choice.get() in ['1','2','3']:
                    self.game_mylist(mainframe, current_game_frame)

    def game_mylist(self, current_win_label, game_frame):
        game_frame.destroy()
        self.words = []
        liste_default = 'liste_pendu.txt'
        ouvrir_list = tk.Button(current_win_label, text ='<Ou ouvrir une liste>', font = self.font_default,
                                bg = 'pale green' , command= lambda : self.open_list(current_win_label))
        ouvrir_list.grid(row = 3, column = 1, sticky = 'ew')

        self.choice_window(current_win_label, (MSG["welcome"]), self.input_list,choice=2, entry_msg = liste_default)

    def open_list(self, current_game_window):
                self.my_filetypes=[('all files', '.*'), ('PNG image files', '.png')]
                valeur = filedialog.askopenfilename(parent = current_game_window,
                                            initialdir = os.getcwd(),
                                            title="Please select a file:",
                                            filetypes = self.my_filetypes)
                self.user_entry.delete(0, 'end')
                self.user_entry.insert(tk.END, valeur)

    def input_list(self, file, current_game_window, mainframe):
        try:
            with open(file.get(), "r", encoding="UTF-8") as f:
                for words in f:
                    for i in words.split():
                        if i.isalpha():
                            self.words.append(i)
        except Exception:
            erreur = ttk.Label(current_game_window, text="\nCe fichier est inexistant dans l'emplacement actuelle.\n")
            erreur.grid(row=4, column=1, sticky="w")

        if self.words != []:
            mainframe.destroy()
            self.lets_play_window()

    def lets_play_window(self):
        self.guess_letters = []
        self.token = 0
        self.secret_word = random.choice(self.words).lower().strip()

        game_window = Toplevel(self.root)
        game_window.title("Mon Pendu")
        game_window.geometry("1200x600")
        game_window.configure(background= self.bg_default)
        game_window.attributes('-fullscreen', True)
        game_window.bind("<F11>",
                         lambda event: game_window.attributes("-fullscreen",
                                    not game_window.attributes("-fullscreen")))
        game_window.bind("<Escape>",
                         lambda event: game_window.attributes("-fullscreen",False))

        self.set_img_Label(game_window, "Image/western_backgroud.jpg", 500, 400)

        title_game = ttk.Label(game_window, font = ('Comic Sans MS', 20, 'bold'), text = "\nMON PENDU")
        title_game.configure(background = self.bg_default)
        title_game.grid(row = 0, column = 1)

        game_input_frame = tk.LabelFrame(game_window, text = MSG["trynow"], relief = GROOVE, bg= self.bg_default)
        game_input_frame.grid(row = 3, column = 1, sticky = "news")

        game_info_frame = tk.LabelFrame(game_window, text = MSG["game_info"],
                                        font = self.font_default, bg = self.bg_default, relief = GROOVE)
        game_info_frame.grid(row = 4, column = 1, sticky = "news")
        self.game_info_label = tk.Label(game_info_frame, font = self.font_default,
                                            text = f"\nNombre d'essai restant : {self.difficulty - self.token}\n"
                                                   f"Nombre de victoire accumulé : {self.victory}",
                                            bg = self.bg_default, justify = LEFT)
        self.game_info_label.grid(row = 1, column = 1, sticky = "news")

        volume_slider_s = ttk.Style()
        volume_slider_s.configure('Volume.Horizontal.TScale', foreground = 'Forest green', background = 'sandy brown')
        game_volume_frame = tk.LabelFrame(game_window, text= "Volume", font = self.font_default, bg = 'sandy brown')
        game_volume_frame.grid(row = 5, column = 1,  sticky = "news")
        self.game_volume = ttk.Scale(game_volume_frame, from_= 0, to= 1, value = 1, orient = HORIZONTAL,
                                     style = 'Volume.Horizontal.TScale', length = 300,
                                     command = self.set_volume)
        self.game_volume.pack(pady = 10 , padx = 10)
        game_volume_frame.configure(background = 'sandy brown')

        self.choice_window(game_window, MSG["guess"], self.set_letter_pict, 1)

        again = tk.Button(game_window, text='Une autre partie ?', bg = 'Forest green', fg = "White",
                             font = ('Comic Sans MS', 15, 'bold'), command = lambda: self.play_again(game_window))
        again.grid(row = 6, column = 1, sticky = "sw")

        quit=tk.Button(game_window, bg = 'red',fg = 'white', text='Quitter',font = ('Comic Sans MS', 10, 'bold'),
                       command = lambda: (game_window.destroy(),pg.mixer.music.unload()))
        quit.grid(row = 7, column = 1, sticky = "se")

        self.music_play("sound/gaming_music.wav", -1)

    def pendu_show(self, game_window):
        self.set_value = 700 * (self.token /self.difficulty)
        self.pendu_pict = ImageTk.PhotoImage(Image.open("Image/Le_pendu.png"))
        pendu_canvas = Canvas(game_window, bg = self.bg_default, width = 600 , height = self.set_value)
        pendu_canvas.grid(row = 1, column = 2, rowspan = 4)
        pendu_canvas.create_image(0, 0, anchor = NW, image = self.pendu_pict)

    def set_volume(self, x):
        pg.mixer.music.set_volume(self.game_volume.get())

    def set_letter_pict(self, guess, gameframe, mainframe):
        guess = guess.get()
        if len(guess) == 1 and guess not in self.guess_letters and guess.isalpha():
            self.guess_letters.append(guess)
            self.draw_letter(mainframe)
            good_guess = tk.Label(gameframe,text = MSG["good_guess"],bg = self.bg_default, font = self.font_default)
            good_guess.grid(row = 3, column = 1, columnspan = 3, sticky = "ew")
            self.check_win(mainframe)
            if guess not in self.secret_word :
                good_guess = tk.Label(gameframe, text=MSG["notIN"], bg = self.bg_default, font = self.font_default)
                good_guess.grid(row = 3, column = 1, columnspan = 3, sticky = "ew")
                self.token += 1
                self.game_info_label.config(text=f"\nNombre d'essai restant : {self.difficulty - self.token}\n"
                                                 f"Nombre de victoire accumulé : {self.victory}")
                self.pendu_show(mainframe)
                self.check_looser(mainframe)
        elif guess in self.guess_letters:
            erreur = tk.Label(gameframe, text = MSG["choiceALD"] ,bg = self.bg_default, font = self.font_default)
            erreur.grid(row = 3, column = 1,columnspan = 3, sticky = "ew")
            print(MSG["guessed"] + ".".join(self.guess_letters))
        else:
            erreur2 = tk.Label(gameframe, text = MSG["choiceNOTL"],bg = self.bg_default, font = self.font_default)
            erreur2.grid(row = 3, column = 1, columnspan = 3, sticky = "ew")

    def check_win(self, gameframe):
        if "_" not in self.unveil_word:
            self.victory += 1

            winning_window = Toplevel(self.root)
            winning_window.title("Mon Pendu")

            canvas = Canvas(winning_window, width=200, height=200, bg = self.bg_default)
            canvas.grid(row = 1, column = 1)
            self.win_img = PhotoImage(file = "Image/winning_smile.png")
            canvas["width"]= self.win_img.width()
            canvas["height"]= self.win_img.height()
            canvas.create_image(0,0 , anchor = 'nw', image = self.win_img)

            winner = tk.Label(winning_window, text = MSG["winnner"] + f"\nLe mot est : {self.secret_word}", bg =self.bg_default,
                             font = self.font_default)
            winner.grid(row = 0, column = 1, sticky = 'ew')

            again =tk.Button(winning_window,text='Une autre partie ?', bg = 'Forest green', fg = "White",
                                            font = ('Comic Sans MS', 15, 'bold'),
                                            command=lambda: self.play_again(gameframe, winning_window))
            again.grid(row=3, column=1, sticky="ew")

            quit=tk.Button(winning_window, bg = 'red',fg = 'white', text='Quitter',font = ('Comic Sans MS', 10, 'bold'),
                            command=lambda: (winning_window.destroy(), gameframe.destroy(), pg.mixer.music.unload()))
            quit.grid(row=4, column=1, sticky="ew")

            self.music_play("sound/victory_music.wav")

    def check_looser(self, gameframe):
        if self.token == self.difficulty:
            looser_window=Toplevel(self.root)
            looser_window.title("Mon Pendu")

            canvas=Canvas(looser_window, width=200, height=200, bg = self.bg_default)
            canvas.grid(row=1, column=1)
            loose_img = Image.open("Image/Le_pendu.png")
            resized = loose_img.resize((500,688), Image.ANTIALIAS)
            self.loose_img =ImageTk.PhotoImage(resized)
            canvas["width"] = self.loose_img.width()
            canvas["height"] = self.loose_img.height()
            canvas.create_image(0, 0, anchor="nw", image = self.loose_img)

            winner=tk.Label(looser_window, text=MSG["loose"] + f"\nLe mot est : {self.secret_word}",
                                           bg =self.bg_default, font = self.font_default)
            winner.grid(row=0, column=1, sticky='ew')

            again=tk.Button(looser_window, text='Une autre partie ?', bg = 'Forest green', fg = "White",
                                           font = ('Comic Sans MS', 15, 'bold'),
                                           command=lambda: self.play_again(gameframe,looser_window))
            again.grid(row=3, column=1, sticky="ew")

            quit=tk.Button(looser_window, bg = 'red',fg = 'white', text='Quitter',font = ('Comic Sans MS', 10, 'bold'),
                            command=lambda: (looser_window.destroy(), gameframe.destroy(), pg.mixer.music.unload()))
            quit.grid(row=4, column=1, sticky="ew")

            self.music_play("sound/cowboy_music.mp3")

    def music_play(self, sound, loop=0):
        pg.mixer.music.unload()
        pg.mixer.music.load(sound)
        pg.mixer.music.play(loops=loop)

    def play_again(self, game_window, current_window = None):
        self.lets_play_window()
        game_window.destroy()
        if current_window != None:
            current_window.destroy()

    def draw_letter(self, game_window):
        self.unveil_word=[c if c in self.guess_letters else "_" for c in self.secret_word]
        canvas_letter_guess = Canvas(game_window, width=600, height=100, bg= self.bg_default,bd = 0, relief = RAISED)
        canvas_letter_guess.grid(row = 5, column = 2, sticky = "n")
        canvas_letter_guess.create_text(20, 30, anchor = W, font =('Comic Sans MS', 17, 'bold'),
                                        text= MSG["guess_used"] + ".".join(self.guess_letters) + '\n' +
                                              MSG["guessed"] + " ".join(self.unveil_word))

    def quit(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    pendu = Pendu_Tkinter_game()
    pendu.run()