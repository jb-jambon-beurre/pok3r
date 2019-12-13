# 0------------------0
# |      Pok3r       |
# | Maxence et Alban |
# 0------------------0

from tkinter import *
from PIL import Image, ImageTk
from time import time

# Classe pour la communication réseau, fichier network.py
from network import Network

# Gestion d'une partie
from game_logic import Card, Partie, Player
                
class Graphics:
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window, width = 1000, height = 500)
        self.canvas.pack()
        self.canvas_ids = {}
        
        # Cartes de la Pioche
        self.draw = [ Card(1, "pique"), Card(1, "pique"), Card(1, "pique") ]
        orientation = 0
        for card in self.draw:
            card.generate_texture(orientation, face = False)
            orientation -= 5

    def update(self):
        self.window.update()
        self.window.update_idletasks()
        
    def start(self, partie):
        h1 = ( Card(10, "carreaux"), Card(5, "pique") )
        h2 = ( Card(5, "carreaux"), Card(1, "pique") )
        
        d = ( Card(4, "carreaux"), Card(4, "pique"), Card(4, "trèfle"), Card(2, "trèfle"), Card(2, "pique") )
        
        self.show_hand(h1, player_n=1)
        self.show_hand(h2, player_n=2)
        
        self.show_drawed(d)
        
        while True:
            self.window.update()
            
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
        
        if len(hand) == 2:
            hand[0].generate_texture(r1, face=face)
            hand[1].generate_texture(r2, face=face)
            self.canvas_ids[h].append(self.canvas.create_image(x1, y1, image=hand[0].tk_image))
            self.canvas_ids[h].append(self.canvas.create_image(x2, y2, image=hand[1].tk_image))

    def show_drawed(self, drawed, show_draw = True):
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

if __name__ == "__main":
    game_window = Graphics()
    network = Network()
    
    # Splashscreen
    game_window.splash()
    
    while True:
        partie_actuelle = Partie()
        game_window.start(partie_actuelle)

p = Partie()
p.start()
print(str(p) + "\n" + str(p.compare()))
