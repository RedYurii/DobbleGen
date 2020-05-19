from PIL import Image, ImageDraw
from deck import Deck
from constants import A4_HEIGHT, A4_WIDTH, CIRCLE_R, CARDS_PER_SHEET, PLANE_ORDER
from gui import ui
#TODO: add json/yml file for settings (symbols pos, scale, rotation etc)
#consider UI

#create deck (hide generate algorithm insie)
deck = Deck()
#deck.show()
print("deck gen OK")

editor_ux = ui(CIRCLE_R+100, CIRCLE_R+240, deck)
print("UI created")

editor_ux.run()

print("TODO: print cards to A4 sheets")


#print (generate sheets and save as pngs)
sheets_number = deck.get_cards_per_deck()//CARDS_PER_SHEET + 1

for sheet_idx in range(0, sheets_number):
    img = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), color = 'white')
    draw = ImageDraw.Draw(img)    
    for y in range(1,6):
        if y%2 == 0:
            continue
        center_y = int(y*A4_HEIGHT/6)

        for x in range(1,4):
            if x%2 == 0:
                continue

            center_x = int(x*A4_WIDTH/4)
            draw.ellipse((center_x - CIRCLE_R, center_y - CIRCLE_R, center_x + CIRCLE_R, center_y + CIRCLE_R), fill = 'white', outline ='black')
            deck.paste_next_card(img, center_x, center_y) 
            
    img.save(f'output/A4_{sheet_idx}.png')

    
