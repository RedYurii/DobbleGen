import random
import yaml

from constants import A4_HEIGHT, A4_WIDTH, CIRCLE_R

class Symbol():
        def __init__(self, orig_image, offset_x, offset_y):
            self.orig_image = orig_image
            self.offset_x = offset_x
            self.offset_y = offset_y
            self.scale = 1.0
            self.angle = 0
            self.update()


        def update(self):
            self.image = self.orig_image
            self.image = self.image.convert('RGBA')

            #change size
            max_x = CIRCLE_R/2
            max_y = CIRCLE_R/2
            mod = 1
            x = self.image.size[0]
            y = self.image.size[1]
            mod = max_x/x
            mod = max_y/y if max_y/y < mod else mod

            self.width = int(x*mod*self.scale)
            self.height = int(y*mod*self.scale)

            self.image = self.image.rotate(self.angle, expand=True)
            self.image = self.image.resize((int(self.width*self.scale), int(self.height*self.scale)))

        def get_size(self):
            return self.image.size

        def paste(self, base_img, anchor_x, anchor_y):
            x = anchor_x + self.offset_x - int(self.width/2)
            y = anchor_y + self.offset_y - int(self.height/2)
            base_img.paste(self.image, (x, y), self.image.convert('RGBA'))

