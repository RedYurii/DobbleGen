from appJar import gui
from PIL import Image, ImageTk, ImageDraw
from symbol import Symbol
from constants import CARDS_PER_SHEET, CIRCLE_R

def wrap(low, high, value):
    return max(low, min(high, value))

class ui():
    def __init__(self, window_w, window_h, deck):
        self.app = gui('Dobgen', f'{window_w}x{window_h}', stretch='both', sticky='news')
        self.app.setBg("#125878", override=False, tint=False)
        self.app.setFont(size=12, family="Calibri", slant="italic")
        self.window_width = window_w
        self.window_height = window_h
        self.canvas_title = 'canvas'
        self.deck = deck
        self.cur_card_idx = 0
        self.cur_symbol_idx = 0

        self.app.setPadding([5,0])

        self.app.addCanvas(self.canvas_title,0,0,3)
        self.draw_canvas()

        self.center_just_spaces = 70

        ###################################################################
        self.app.setStretch('column')
        self.app.setSticky('nes')
        self.app.addLabel("Card", f"Card: {self.cur_card_idx+1}".center(self.center_just_spaces), 1, 1)

        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.addButton("Prev Card", self.press, 1, 0)

        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.button("Next Card", self.press, 1, 2)
        
        ###################################################################
        self.app.setStretch('column')
        self.app.setSticky('nes')
        self.app.addLabel("Image", f"Image: {self.cur_symbol_idx+1}".center(self.center_just_spaces), 2, 1)
        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.addButton("Prev Image", self.press, 2, 0)

        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.button("Next Image", self.press, 2, 2)

        ###################################################################
        self.app.setStretch('column')
        self.app.setSticky('nes')
        scale_str = str(round(self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].scale, 2))
        self.app.addLabel("Scale", f"Scale: {scale_str}".center(self.center_just_spaces), 3, 1)
        
        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.addButton("Chonkier", self.press, 3, 0)

        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.button("Smoler", self.press, 3, 2)#, stretch='column', sticky='nsw')

        ###################################################################
        self.app.setStretch('column')
        self.app.setSticky('nes')
        self.app.addLabel("Angle", f"Angle: {self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].angle}".center(self.center_just_spaces), 4, 1)

        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.addButton("Rotate left", self.press, 4, 0)# stretch='column', sticky='nes')

        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.button("Rotate right", self.press, 4, 2)#, stretch='column', sticky='nsw')

        ###################################################################
        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.addButton("Move Left", self.press, 5, 0, 1)# stretch='column', sticky='nes')

        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.button("Move Right", self.press, 5, 2, 1)#, stretch='column', sticky='nsw')

        ###################################################################
        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.addButton("Move Down", self.press, 6, 0, 1)# stretch='column', sticky='nes')

        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.button("Move Up", self.press, 6, 2, 1)#, stretch='column', sticky='nsw')

        ###################################################################
        self.app.setStretch('column')
        self.app.setSticky('nesw')
        self.app.button("Export", self.app.stop, 7, 0, 3)#, stretch='column', sticky='nsw')


    def run(self):
        self.app.go()
 

    def draw_canvas(self): 
        self.app.clearCanvas(self.canvas_title)
        circle_x = int((self.window_width )/2 - CIRCLE_R/2) #
        circle_y = 0   

        self.app.addCanvasCircle(self.canvas_title, circle_x, circle_y, CIRCLE_R, fill='white')

        #these are base coords (circle center)
        anchor_x = circle_x + int(CIRCLE_R/2)
        anchor_y = int(self.window_width/2)

        for s in self.deck.get_card(self.cur_card_idx):
            new_x = anchor_x + int(s.offset_x/2)
            new_y = anchor_y + int(s.offset_y/2) - int(s.get_size()[1]/4)

            image_to_draw = s.image.resize((int(s.get_size()[0]/2), int(s.get_size()[1]/2)))
            photo = ImageTk.PhotoImage(image_to_draw)
            self.app.addCanvasImage(self.canvas_title, new_x, new_y, photo)


    def update_img_scale(self, scale = 1.0, mode=False):
        if mode == 'inc':
            self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].scale += 0.1
        elif mode == 'dec':
            self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].scale -= 0.1

        scale_str = str(round(self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].scale, 2))
        self.app.setLabel('Scale', f"Scale: {scale_str}".center(self.center_just_spaces))
        self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].update()
        

    def update_img_angle(self, angle = 1.0, mode=False):
        if mode == 'left':
            self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].angle += 5
        elif mode == 'right':
            self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].angle -= 5

        self.app.setLabel('Angle', f"Angle: {self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].angle}".center(self.center_just_spaces))
        self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].update()

    
    def press(self, btn):
        if btn == "Chonkier":
            self.update_img_scale(mode = 'inc')      
        elif btn == "Smoler":
            self.update_img_scale(mode = 'dec')
        elif btn == "Rotate left":
            self.update_img_angle(mode = 'left')
        elif btn == "Rotate right":
            self.update_img_angle(mode = 'right')
        elif btn == "Next Image":           
            self.cur_symbol_idx = wrap(0, CARDS_PER_SHEET-1, self.cur_symbol_idx+1)
            self.app.setLabel('Image', f"Image: {self.cur_symbol_idx+1}".center(self.center_just_spaces))
        elif btn == "Prev Image":
            self.cur_symbol_idx = wrap(0, CARDS_PER_SHEET-1, self.cur_symbol_idx-1)
            self.app.setLabel('Image', f"Image: {self.cur_symbol_idx+1}".center(self.center_just_spaces))
        elif btn == "Next Card":
            self.cur_card_idx = wrap(0, self.deck.get_cards_per_deck()-1, self.cur_card_idx+1)
            self.app.setLabel('Card', f"Card: {self.cur_card_idx+1}".center(self.center_just_spaces))
        elif btn == "Prev Card":
            self.cur_card_idx = wrap(0, self.deck.get_cards_per_deck()-1, self.cur_card_idx-1)
            self.app.setLabel('Card', f"Card: {self.cur_card_idx+1}".center(self.center_just_spaces))
        elif btn == "Move Left":
            self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].offset_x -= 5
        elif btn == "Move Right":
            self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].offset_x += 5
        elif btn == "Move Up":
            self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].offset_y -= 5
        elif btn == "Move Down":
            self.deck.get_card(self.cur_card_idx)[self.cur_symbol_idx].offset_y += 5

        self.draw_canvas()



