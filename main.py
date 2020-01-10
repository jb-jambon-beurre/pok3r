# 0------------------0
# |      Pok3r       |
# | Maxence et Alban |
# 0------------------0

from tkinter import *
from PIL import Image, ImageTk, ImageFont, ImageDraw
from time import time, sleep

# Classe pour la communication réseau, fichier network.py
from network import Network

# Gestion d'une partie
from game_logic import Card, Partie

class Graphics:
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("Pok3r")
        self.canvas = Canvas(self.window, width = 1000, height = 500)
        self.canvas.pack()
        self.canvas_ids = {}
        
        self.finished = False

        self.window.bind("<KeyPress>", self.processKeys)

        self.betamount = [0, 0]
        self.currentPlayer = 0
        self.partie = None
        
        # Cartes face cachée de la Pioche
        self.draw = [ Card(-1, 0), Card(-1, 0), Card(-1, 0) ]
        orientation = 0
        for card in self.draw:
            card.generate_texture(orientation, face = False)
            orientation -= 5

    def processKeys(self, key):
        c = self.currentPlayer
        
        if self.partie != None:
            if not self.finished:
                if key.char == "+" and self.betamount[c] < self.partie.players[c].getMoney():
                    self.betamount[c] += 10
                elif key.char == "-" and self.betamount[c] > self.partie.minimalBet:
                    self.betamount[c] -= 10
                elif key.char in ("\r", "\n"):
                    self.partie.minimalBet = self.betamount[c]
                    self.partie.bet(self.betamount[c], c)

                    if self.partie.players[c].getMoney() < self.betamount[c]:
                        self.betamount[c] = self.partie.players[c].getMoney()

                    if c == 1:
                        self.partie.draw(True)
                        if len(self.partie.cardsInGame) >= 5:
                            c = self.partie.compare()
                            if c == -1:
                                print("Egalité")
                            elif c == 1:
                                print("Victoire Joueur 1")
                            elif c == 2:
                                print("Victoire Joueur 2")
                            print("Appuyez sur 'q' pour quitter")
                            self.update()
                            self.finished = True
                        self.currentPlayer = 0
                    else:
                        self.currentPlayer += 1

                    if self.partie.players[self.currentPlayer].getMoney() < self.partie.minimalBet:
                        self.betamount[self.currentPlayer] = self.partie.players[self.currentPlayer].getMoney()
                    else:
                        self.betamount[self.currentPlayer] = self.partie.minimalBet
            else:
                if key.char == "q":
                    self.window.destroy()

    def update(self):
        player_n = 0
        for player in self.partie.players:
            player_n += 1
            self.show_hand(player.hand, player_n)

        self.canvas.itemconfig(self.canvas_ids["money1"], text="Money: " + str(self.partie.players[0].getMoney()))
        self.canvas.itemconfig(self.canvas_ids["money2"], text="Money: " + str(self.partie.players[1].getMoney()))
        self.canvas.itemconfig(self.canvas_ids["betamount1"], text="Bet amount: " + str(self.betamount[0]))
        self.canvas.itemconfig(self.canvas_ids["betamount2"], text="Bet amount: " + str(self.betamount[1]))

        self.show_drawed(self.partie.cardsInGame)
        
        try:
            self.window.update()
            self.window.update_idletasks()
        except:
            exit(0)
        
    def start(self, partie):
        partie.start()
        self.partie = partie

        self.betamount[0] = self.betamount[1] = self.partie.minimalBet
        
        self.canvas_ids["money2"] = self.canvas.create_text(500, 40, fill="black", text="")
        self.canvas_ids["money1"] = self.canvas.create_text(500, 460, fill="black", text="")
        self.canvas_ids["betamount2"] = self.canvas.create_text(500, 20, fill="black", text="")
        self.canvas_ids["betamount1"] = self.canvas.create_text(500, 480, fill="black", text="")
        
        while True:
            self.update()
            
    def show_hand(self, hand, player_n = 1):
        h = "h"+str(player_n)
        if h in self.canvas_ids.keys():
            if len(self.canvas_ids[h]) > 0:
                for i in self.canvas_ids[h]:
                    self.canvas.delete(i)
        
        self.canvas_ids[h] = []
                
        r1, r2 = -20, -40
        x1, y1, x2, y2 = 80, 370, 200, 430
        face = True
        
        if player_n == 2:
            r1, r2 = 160, 140
            x1, y1, x2, y2 = 920, 130, 800, 70
            face = False
        
        if self.finished:
            face = True
        
        if len(hand) == 2:
            hand[0].generate_texture(r1, face=face)
            hand[1].generate_texture(r2, face=face)
            self.canvas_ids[h].append(self.canvas.create_image(x1, y1, image=hand[0].tk_image))
            self.canvas_ids[h].append(self.canvas.create_image(x2, y2, image=hand[1].tk_image))

    def show_drawed(self, drawed):
        if "d" in self.canvas_ids.keys():
            if len(self.canvas_ids["d"]) > 0:
                for i in self.canvas_ids["d"]:
                    self.canvas.delete(i)
        self.canvas_ids["d"] = []
        
        for card in drawed:
            card.generate_texture(0, face=True)
        
        self.canvas_ids["d"].append(self.canvas.create_image(220, 250, image=self.draw[0].tk_image))
        self.canvas_ids["d"].append(self.canvas.create_image(220, 250, image=self.draw[1].tk_image))
        self.canvas_ids["d"].append(self.canvas.create_image(220, 250, image=self.draw[2].tk_image))
        
        for x in range(0, len(drawed)):
            self.canvas_ids["d"].append(self.canvas.create_image(x * 110 + 350, 250, image = drawed[x].tk_image))

    def splash(self):
        # Load image
        image = Image.open("jb_splash.png")
        cropped = image.crop((0, 0, 64, 64))
        cropped = cropped.resize((cropped.height * 5, cropped.width * 5))
        tk_image = ImageTk.PhotoImage(cropped)

        # Show base image for 2 seconds
        image_id = self.canvas.create_image(500, 250, image = tk_image)
        lasttime = time()
        
        while time() - lasttime < 1:
            self.window.update()

        lasttime = time()
                
        # Animate image during 1 second
        x = 0
        count = 0
        while count < 50:
            if (time() - lasttime) > (1/50):
                lasttime = time()
                count += 1
                x += 64
                if x >= image.width: x = 0
                cropped = image.crop((x, 0, x + 64, 64))
                cropped = cropped.resize((cropped.height * 5, cropped.width * 5))
                tk_image = ImageTk.PhotoImage(cropped)
                self.canvas.itemconfig(image_id, image=tk_image)
            self.window.update()
        
        # Show base image for 2 seconds
        self.canvas.itemconfig(image_id, image=tk_image)
        lasttime = time()
        
        while time() - lasttime < 1:
            self.window.update()
            
        self.canvas.delete(image_id)
        self.canvas.pack()
        self.window.update()

if __name__ == "__main__":
    game_window = Graphics()
    network = Network()
    
    # Splashscreen
    game_window.splash()
    
    while True:
        partie_actuelle = Partie()
        game_window.start(partie_actuelle)
