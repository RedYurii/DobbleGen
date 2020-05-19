import random
from PIL import Image

from symbol import Symbol
from constants import CIRCLE_R, PLANE_ORDER

class Deck:
    def __init__(self):
        self.cards_per_deck = PLANE_ORDER**2 + PLANE_ORDER + 1
        self.symbols_per_deck = PLANE_ORDER**2 + PLANE_ORDER + 1
        self.symbols_per_card = PLANE_ORDER + 1

        self.images = [Image.open(rf"resources/img_{i}.png") for i in range(0, self.symbols_per_deck)]
        #self.symbols = [Symbol(i) for i in range(0, self.symbols_per_deck)]
        self.cards = list()
        self.index = 0

        base_xoffsets = list()
        base_yoffsets = list()

        #generate x/y offsets
        step_y = int(CIRCLE_R/2)
        for i in range(self.symbols_per_card):   
            if i<2:
                base_yoffsets.append(-step_y)
                base_xoffsets.append((-1+((i%2)*2) )* int(3*CIRCLE_R/8))
            elif i>3:
                base_yoffsets.append(step_y)
                base_xoffsets.append((-1+((i%2)*2)) * int(3*CIRCLE_R/8))
            else:
                base_yoffsets.append(0)
                base_xoffsets.append((-1+((i%2)*2)) * int(5*CIRCLE_R/8))

        #dooble generator algorithm
        for i in range(PLANE_ORDER+1):
            #Add new card with first symbol
            self.cards.append([Symbol(self.images[0], base_xoffsets[0], base_yoffsets[0])])

            #Add n+1 symbols on the card (e.g. 8 symbols)
            for j in range(PLANE_ORDER):
                next_idx = (j+1)+(i*PLANE_ORDER)
                self.cards[i].append(Symbol(self.images[next_idx], base_xoffsets[j+1], base_yoffsets[j+1]))

        #Add n sets of n cards 
        for k in range(2, PLANE_ORDER+2):
            for i in range(PLANE_ORDER):
                #Append a new card with 1 symbol
                self.cards.append([Symbol(self.images[k-1], base_xoffsets[0], base_yoffsets[0])])
                #Add n symbols on the card (e.g. 7 symbols)
                for j in range(0, PLANE_ORDER):
                    next_idx  = PLANE_ORDER + 2 + i + (k+1)*j
                    while next_idx >=  PLANE_ORDER + 2 + (j+1)*PLANE_ORDER:
                        next_idx = next_idx - PLANE_ORDER 
                    self.cards[len(self.cards)-1].append(Symbol(self.images[next_idx-1], base_xoffsets[j+1], base_yoffsets[j+1]))
   
        
    def get_cards_per_deck(self):
        return self.cards_per_deck


    def get_card(self, idx):
        ''' Returns list of n symbols'''
        return self.cards[idx]


    def paste_next_card(self, base_img, anchor_x, anchor_y):
        if self.index < self.cards_per_deck:
            for s in self.cards[self.index]:
                s.paste(base_img, anchor_x, anchor_y)
        self.index += 1

            

    