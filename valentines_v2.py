import time
import random as r
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pngdec import PNG

# Display Constants
PADDING_Y = 20
PADDING_X = 20
BUTTONS_Y = 200

# Initialize Display
display = PicoGraphics(display =DISPLAY_TUFTY_2040)
png = PNG(display)
# RGB Color code
PINK = display.create_pen(250,218,221)
RED = display.create_pen(178,34,34)
display.set_font('bitmap8')

# Button Initalization
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)

# Global Variables
pg : int = 0
game :HeartGame


# Display Functions
def get_x(text:str,size:int) ->int:
    width,height =display.get_bounds()
    text_width = display.measure_text(text,scale=size)
    if text_width >= width:
        text_x = PADDING_X
    else:
        text_x = int((width- text_width)/2)
    return text_x

def print_mesg(mesg: str, size: int,y_offset:int=0,x_offset:int=0) ->None:
        x =get_x(mesg,size)
        display.text(mesg,x+x_offset,y_offset,290,size)
        
def print_centered_mesgs(y:int,size:int,*mesgs) ->None:
    y_offset = PADDING_Y
    for m in mesgs:
        print_mesg(m,size,y+y_offset)
        y_offset+=size*10
    
def print_button_mesg(mesg:str, button:str) -> None:
    x_offset:int = 0 if button == "b" else -100 if button == "a" else 100
    print_mesg(mesg,2,BUTTONS_Y,x_offset)

def print_big_hearts(hearts: List[Dict[str,int]]) ->None:
    png.open_file("pink_heart_bg.png")
    for h in hearts:
        png.decode(h["x"],h["y"])

def print_small_hearts(hearts:List[Dict[str,int]])->None: 
    png.open_file("small_pink_heart_bg.png")
    for h in hearts:
        png.decode(h["x"],h["y"])

def display_page() ->None:
    # Start writing
    display.set_pen(PINK)
    display.clear()
    display.set_pen(RED)
    
    if pg == 0:
        print_centered_mesgs(0,5,"Happy","Valentine's","Day")
        print_big_hearts([{"x":220,"y":150}])
    elif pg == 1:
        print_centered_mesgs(0,3,"In love...")
    elif pg==2 or pg == 3:
        print_centered_mesgs(0,3,"Sometimes you have to")
        print_centered_mesgs(60,5,"WORK")
        if pg==2:
            print_big_hearts([{"x":140,"y":130}])
        else:
            print_centered_mesgs(140,3,"when you're ready, go to the next page")
            print_small_hearts([{"x":155,"y":130}])
    elif pg ==4:
        print_centered_mesgs(0,7,"Collect","The","Hearts")
        print_small_hearts([{"x": 85,"y":115},
                      {"x":222,"y":115}])
        game.reset()
    elif pg==5:
        game.display_game()
    elif pg==6 or pg==7:
        print_centered_mesgs(0,4,f"You collected {game.get_collection()} hearts")
        if pg == 6:
            print_big_hearts([{"x":220,"y":150}])
        else:
            print_button_mesg("Try Again","a")
            print_button_mesg("What's Next","c")
    elif pg == 8:
        print_centered_mesgs(0,4,"Will you be my","Valentine?")
        print_button_mesg("YES","a")
        print_button_mesg("NO","c")
    elif pg == 9:
        print_centered_mesgs(0,3,"I think you meant to press a different button...")
    elif pg == 10:
        print_centered_mesgs(0,7,"YAY")
        print_centered_mesgs(100,2,"I love you!")
    else:
        print_centered_mesgs(0,10,"FIN")
        print_button_mesg("RESTART","a")
        print_button_mesg("EXIT","c")
        print_small_hearts([{"x":15,"y":10}])
        
    # Update the screen
    display.update()
    

# ---------------------------------------------------------------------------------
class HeartGame:
    START_X = 150
    START_Y = 190
    BOX_WIDTH = 50
    BOX_HEIGHT = 50
    
    def _init_(self):
        self.timer : int = 10
        self.my_hearts : List[Dict[str,int]] = []
        self.box_x :int= START_X
        self.box_y:int = START_Y
        self.collection:int = 0
            
    def pour_hearts(self,num : int) -> None:
        hearts = [{"x":r.randint(20,300),"y":20} for _ in range(num)]
        if self.my_hearts:
            self.my_hearts = self.my_hearts + hearts
        else:
            self.my_hearts = hearts
        print_small_hearts(self.my_hearts)

    def collision_detection(self, x:int,y:int) -> bool:
        if y >= self.START_Y and x > self.box_x and x < self.box_x + self.BOX_WIDTH:
            return True
        return False

    def move_hearts(self) -> None:
        if self.my_hearts:
            removal: List[int] = []
            for i in range(len(self.my_hearts)):
                self.my_hearts[i]["y"] += r.randint(10,50)
                if self.collision_detection(self.my_hearts[i]["x"],self.my_hearts[i]["y"]):
                    removal.append(i)
                    self.collection +=1
                elif self.my_hearts[i]["y"] > 240:
                    removal.append(i)
            for re in removal:
                self.my_hearts.pop(re)
            print_small_hearts(self.my_hearts)

    def draw_box(self) ->None:
        display.rectangle(self.box_x,self.START_Y,self.BOX_WIDTH,self.BOX_HEIGHT)

    def move_box(self,left:bool,x:int=0) -> None:
        if left:
            self.box_x -= x
            if self.box_x < 5:
                self.box_x = 5
        else:
            self.box_x += x
            if self.box_x > 315:
                self.box_x = 315
                
    def reset(self) ->None:
        self.box_x = self.START_X
        self.collection = 0
        self.my_hearts = []
    
    def display_game(self) -> None:
        self.draw_box()
        if self.my_hearts:
            self.move_hearts()
        self.pour_hearts(1)
    
    def play_game(self,move : bool) -> int:
        if self.collection <= 20:
            self.move_box(move,10)
            return 0
        return 1
            
    def get_collection(self) -> int:
        return self.collection
    
# ---------------------------------------------------------------------------------
# Page Change Loop
game = HeartGame()
while True:
    if button_down.is_pressed:
        if pg == 5 or pg == 7 or pg==8:
            continue
        elif pg == 9:
            pg = 8
        else:
            pg+=1
        time.sleep(0.5) 
    elif button_a.is_pressed:
        if pg == 5:
            pg+=game.play_game(True)
        elif pg == 7:
            pg = 4
            time.sleep(0.5) 
        elif pg ==8:
            pg=10
            time.sleep(0.5)
        elif pg >= 11:
            pg = 0
    elif button_c.is_pressed:
        if pg==5:
            pg+= game.play_game(False)
        elif pg == 7 or pg == 8:
            pg +=1
            time.sleep(0.5)
        elif pg >= 11:
            break

    display_page()
