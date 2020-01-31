# Gestion des parties

from PIL import Image, ImageTk, ImageFont, ImageDraw
import random as r
from functools import reduce

class Card:
    def __init__(self, number, family):
        self.number = number
        self.family = family

    def generate_texture(self, rotation = 0, face = True):
        if face:
            if self.family == 0: # Pique
                self.base = Image.open("card_face_pique.png")
            elif self.family == 1: # Trèfle
                self.base = Image.open("card_face_trefle.png")
            elif self.family == 2: # Carreaux
                self.base = Image.open("card_face_carreaux.png")
            elif self.family == 3: # Coeur
                self.base = Image.open("card_face_coeur.png")
            else:
                return

            self.font = ImageFont.truetype("LemonMilkbold.otf", 20)

            draw = ImageDraw.Draw(self.base)
            draw.text((18,5), self.number_str(), fill=(0,0,0,255), font=self.font)
        else:
            self.base = Image.open("card_back.png")

        self.edited = self.base.resize((100, 140)).rotate(rotation, expand=1)
        self.tk_image = ImageTk.PhotoImage(self.edited)

    def full_cards_list():
        ll = []
        for family in range(0, 4):
            for value in range(2, 15):
                ll.append(Card(value, family))
        return ll

    def number_str(self):
        if self.number == 11:
            return "J"
        elif self.number == 12:
            return "Q"
        elif self.number == 13:
            return "K"
        elif self.number == 14:
            return "A"
        elif self.number > 13 or self.number < 1:
            return "?"
        else:
            return str(self.number)

    def __str__(self):
        family = self.family
        if   family == 0: # pique
            family = "\u2660"
        elif family == 1: # trèfle
            family = "\u2663"
        elif family == 2: # carreaux
            family = "\u2666"
        elif family == 3: # coeur
            family = "\u2665"

        return self.number_str() + str(family)

class Coin:
    def __init__(self):
        self.base = Image.open("coin.png")
        self.frame = 0

    def generate_next_texture(self, moneyAmount = 0):
        x = self.frame * 64
        self.edited = self.base.crop((x, 0, 64, 64)).resize((100, 100))
        self.tk_image = ImageTk.PhotoImage(self.edited)

        self.frame = (self.frame + 1) % 46

class Player:
    startingMoney = 1000
    names = ["Jackouille la fripouille", "___xXx__daRk_KikouLolDu92__xXx___", "Pigeon", "Coq", "Mouton", "Alban", "Maxence", "Megaman", "Yvette", "Verrue puante", "Asticot velu"]
    def __init__(self):
        self.money = self.startingMoney
        self.name = self.randomName()
        self.hand = []

    def __str__(self):
        return (self.getName() + " : " +
                " | Card 1 : " + str(self.hand[0]) +
                " | Card 2 : " + str(self.hand[1]) +
                " | Money : " + str(self.money))

    def randomName(self): #string
        r.shuffle(self.names)
        return self.names[0]

    def getName(self): #string
        return self.name

    def newCard(self, card):
        self.hand.append(card)

    def getMoney(self): #int
        return self.money

    def moneyChange(self, amount):
        self.money += amount

    def getHand(self): #list of cards
        return self.hand

class Partie:
    minimalBet = 0
    players = []
    cardsInGame = []
    cardsLeft = []

    def __init__(self, nbPlayers = 2, minimalBet = 10):
        #self.cardsLeft = Card.full_cards_list()
        #r.shuffle(self.cardsLeft)
        self.cardsLeft = [
            Card(9,3),  #Joueur 1
            Card(8,3),

            Card(14,2), #Joueur 2
            Card(14,2),

            Card(7,3),  #Tapis
            Card(6,3),
            Card(5,3),
            Card(7,0),
            Card(2,0),

            Card(9,3)   #Placeholder
        ]

        self.minimalBet = minimalBet

        for i in range(0, nbPlayers):
            self.players.append(Player()) #Generé dans cette classe


    def __str__(self):
        ttr = "Players in the game : \n"
        for player in self.players :
            ttr += (str(player) + "\n")
        ttr += "Cards in game : "
        for card in self.cardsInGame :
            ttr += (str(card) + " | ")
        return ttr

    def getNumberOfCardsInGame(self):
        return len(self.cardsInGame)

    def start(self):
        self.draw(False, 2, 0) #Draw Player 1 Cards
        self.draw(False, 2, 1) #Draw Player 2 Cards
        self.draw(True, (3))     #Draw Game Cards

    def bet(self, betAmount, playerIndex):
        self.players[playerIndex].moneyChange(-betAmount)

    def draw(self, isForGame, amount = 1, playerIndex = 0):
        if(len(self.cardsLeft) <= 0):
            return system.write("Error : The deck isn't supposed to be empty !", "ERROR")
        else :
            for i in range(0, amount):
                if(isForGame == False) :
                    self.players[playerIndex].newCard(self.cardsLeft.pop(0))
                        #print(self.players[playerIndex].hand[i].number, self.players[playerIndex].hand[i].family)
                elif(isForGame == True) :
                    self.cardsInGame.append(self.cardsLeft[0])
                    self.cardsLeft.pop(0)

    def compare(self):
        if(self.check(0)[0] > self.check(1)[0]):
            print("Victoire joueur 1 car meilleur type de main")
            return 1
        elif(self.check(0)[0] < self.check(1)[0]):
            print("Victoire joueur 2 car meilleur type de main")
            return 2
        elif(self.pScore(0) > self.pScore(1)):
            print("Victoire joueur 1 car meilleur main contre le même type de main")
            return 1
        elif(self.pScore(0) < self.pScore(1)):
            print("Victoire joueur 2 car meilleur main contre le même type de main")
            return 2
        else:
            print("Egalité")
            return -1

    def pScore(self, playerIndex):
        cards = self.players[playerIndex].getHand() + self.cardsInGame
        ps = 0
        values = [c.number for c in cards]
        for c in values:
            for i in range(2, 15):
                j = 0
                if c == i:
                    j+=1

                ps += 10**i * j
        return ps

    def sort(self, cards):
        c = sorted(cards, key=lambda card: card.number)
        return c

    def check(self, playerIndex):
        cardsToCheck = self.players[playerIndex].getHand() + self.cardsInGame
        playerIndex += 1
        cardsToCheck = self.sort(cardsToCheck)
        #if self.checkQuinteFlushRoyale(cardsToCheck)[0]:#BUG
        #    print("Quinte Flush Royale" + " " + str(playerIndex))
        #    return (10,self.checkQuinteFlushRoyale(cardsToCheck)[1])
        if self.checkQuinteFlush(cardsToCheck)[0]:#
            print("Quinte Flush" + " " + str(playerIndex))
            return (9,self.checkQuinteFlush(cardsToCheck)[1])
        elif self.checkCarre(cardsToCheck)[0]:#
            print("Carre" + " " + str(playerIndex))
            return (8,self.checkCarre(cardsToCheck)[1])
        elif self.checkFull(cardsToCheck)[0]:#
            print("Full" + " " + str(playerIndex))
            return (7,self.checkFull(cardsToCheck)[1])
        elif self.checkCouleur(cardsToCheck)[0]:#
            print("Couleur" + " " + str(playerIndex))
            n = reduce(lambda a,b: a+b, self.checkCouleur(cardsToCheck)[1])
            c = Card(n,1)
            return (6,c)
        elif self.checkSuite(cardsToCheck)[0]:#
            print("Suite" + " " + str(playerIndex))
            n = reduce(lambda a,b: a+b, self.checkSuite(cardsToCheck)[1])
            c = Card(n,1)
            return (5,c)
        elif self.checkBrelan(cardsToCheck)[0]:#
            print("Brelan" + " " + str(playerIndex))
            return (4,self.checkBrelan(cardsToCheck)[1])
        elif self.checkDoublePaire(cardsToCheck)[0]:#
            print("Double Paire" + " " + str(playerIndex))
            return (3,self.checkDoublePaire(cardsToCheck)[1])
        elif self.checkPaire(cardsToCheck)[0]:#
            print("Paire" + " " + str(playerIndex))
            return (2,self.checkPaire(cardsToCheck)[1])
        else:
            print("Carte la plus haute" + " " + str(playerIndex))
            highestN = 0
            for n in cardsToCheck:
                highestN = max(n.number, highestN)
            return (1, Card(highestN,1))#

    def checkQuinteFlushRoyale(self, cards):
        if(self.checkQuinteFlush(cards)[0]):
            values = self.checkQuinteFlush()[1].sort()
            if(values[0] == "J"):
                return (True, Card(0,1))
            else:
                return (False, None)
        else:
            return (False, None)
    
    def checkQuinteFlush(self, cards):
        #CouleurSetup
        couleurs = [c.family for c in cards]
        mostFrequentFamily = self.mostFrequent(couleurs)
        count = 0
        for n in couleurs:
            if n == mostFrequentFamily:
                count += 1
        #SuiteSetup
        p=0
        last = 0
        values = list(set([c.number for c in cards]))
        print(values)
        for element in values:
            if last != 0:
                if element - last == 1:
                    p += 1
            last = element
        #End
        if count >= 5 and p >= 5:
          flushCards = []
          for card in cards:
              if card.family == mostFrequentFamily:
                  flushCards.append(card.number)
          flushCards.sort()
          flushCards = flushCards[::-1][:5]
          return (True, flushCards)
        else:
          return (False, None)

    def checkCarre(self, cards):
        values = [c.number for c in cards]
        mostFrequentValue = self.mostFrequent(values)
        count = 0
        for n in values:
            if n == mostFrequentValue:
                count += 1
        if count == 4:
            return (True, Card(mostFrequentValue,1))
        else:
            return (False, None)

    def checkFull(self, cards):
        values = [c.number for c in cards]
        ###
        cardsToPop = []
        mostFrequentValue = self.mostFrequent(values)
        count = 0

        for i in range(0, len(values)-1):
            if values[i] == mostFrequentValue:
                count += 1
                cardsToPop.append(i)
        indexes = [i for i in cardsToPop]
        for index in sorted(indexes, reverse=True):
            values.pop(index)
        ###
        secondMostFrequentValue = self.mostFrequent(values)
        count2 = 0

        for n in values:
            if n == secondMostFrequentValue:
                count2 += 1
        ###
        if count == 3 and count2 == 2:
            return (True, Card(mostFrequentValue + secondMostFrequentValue, 1))
        else:
            return (False, None)

    def checkCouleur(self, cards):
        couleurs = [c.family for c in cards]
        mostFrequentFamily = self.mostFrequent(couleurs)
        count = 0
        for n in couleurs:
            if n == mostFrequentFamily:
                count += 1
        if count >= 5:
          flushCards = []
          for card in cards:
              if card.family == mostFrequentFamily:
                  flushCards.append(card.number)
          flushCards.sort()
          flushCards = flushCards[::-1][:5]
          return (True, flushCards)
        else:
          return (False, None)

    def checkSuite(self, cards):
        n=0
        last = 0
        values = set([c.number for c in cards])
        values = list(values)
        print(values)
        for i in values:
            if last != 0:
                if i - last == 1:
                    n += 1
                last = i
            else :
                last = i
        if n >= 5:
            return (True, values[:5])
        else :
            return (False, None)

    def checkBrelan(self, cards):
        values = [c.number for c in cards]
        mostFrequentValue = self.mostFrequent(values)
        count = 0
        for n in values:
            if n == mostFrequentValue:
                count += 1
        if count == 3:
            return (True, Card(mostFrequentValue,1))
        else:
            return (False, None)

    def checkDoublePaire(self, cards):
        values = [c.number for c in cards]
        ###
        cardsToPop = []
        mostFrequentValue = self.mostFrequent(values)
        count = 0

        for i in range(0, len(values)-1):
            if values[i] == mostFrequentValue:
                count += 1
                cardsToPop.append(i)
        indexes = [i for i in cardsToPop]
        for index in sorted(indexes, reverse=True):
            values.pop(index)
        ###
        secondMostFrequentValue = self.mostFrequent(values)
        count2 = 0

        for n in values:
            if n == secondMostFrequentValue:
                count2 += 1
        ###
        if count == 2 and count2 == 2:
            return (True, Card(mostFrequentValue + secondMostFrequentValue, 1))
        else:
            return (False, None)

    def checkPaire(self, cards):
        values = [c.number for c in cards]
        mostFrequentValue = self.mostFrequent(values)
        count = 0
        for n in values:
            if n == mostFrequentValue:
                count += 1
        if count == 2:
            return (True, Card(mostFrequentValue,1))
        else:
            return False, (None)

    def mostFrequent(self, List):
        counter = 0
        num = List[0]
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i
        return num
