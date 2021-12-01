
import arcade
import random

Screen_Width=1280
Screen_Height=720

class PairingGame(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title,resizable=True)
        self.set_location(10,40)

        arcade.set_background_color(arcade.color.APRICOT)


    def setup(self):
        self.end=False
        self.restart=False
        self.score = 0
        self.starttime = 60
        self.collect = 0
        self.time = self.starttime
        self.vocablist = arcade.SpriteList()
        self.translist = arcade.SpriteList()
        self.file_vallist = []
        self.vocabindlist = []
        self.transindlist = []
        self.selectedframe = arcade.SpriteList()
        self.selected_position_list = []
        self.selecteditem = arcade.SpriteList()
        self.selectedind = []
        self.collectedvocab = arcade.SpriteList()
        self.colvopo = [(990, 450), (990, 380), (990, 290), (990, 200), (990, 110)]
        self.collectedtrans = arcade.SpriteList()
        self.coltrpo = [(1120, 450), (1120, 380), (1120, 290), (1120, 200), (1120, 110)]
        self.wrongselection = "what"
        self.triggertime = 0
        self.deselect = False
        self.win = False
        self.startgame = False
        self.pause = False
        self.startbutton = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/start.png", center_x=640, center_y=360)
        self.resumebutton = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/resume2.png", center_x=640, center_y=320)
        self.pausebutton = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/pause.png", center_x=1210, center_y=650)
        self.background = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/background.png", center_x=640, center_y=360)
        self.covocabbg = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/covoc.png", center_x=1055, center_y=290)
        self.winbg = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/win2.png", center_x=430, center_y=360)
        self.pausebg = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/pausebg2.png", center_x=640, center_y=360)
        self.timeupbg = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/timeup2.png", center_x=430, center_y=360)
        self.restartbutton = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/restart.png", center_x=1100, center_y=650)
        self.restartbutton2 = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/restart.png", center_x=1210, center_y=650)
        for i in range(5):
            file_val = random.randrange(1, 70)
            while True:
                if file_val not in self.file_vallist:
                    self.file_vallist.append(file_val)
                    break
                else:
                    file_val = random.randrange(1, 70)
        self.sprite_position_list = [[230, 485], [430, 485], [630, 485], [125, 305], [325, 305], [525, 305], [725, 305],
                                     [230, 125], [430, 125], [630, 125]]
        random.shuffle(self.sprite_position_list)
        for i in range(1, 6):
            c = self.sprite_position_list[i - 1]
            f = self.file_vallist[i - 1]
            self.vocab = arcade.Sprite("C:/Users/CRP/Desktop/Game/vocab/" + str(f) + ".png", scale=0.75, center_x=c[0],
                                       center_y=c[1])
            self.vocablist.append(self.vocab)
            self.vocabindlist.append(f)
        for i in range(6, 11):
            c = self.sprite_position_list[i - 1]
            f = self.file_vallist[i - 6]
            self.trans = arcade.Sprite("C:/Users/CRP/Desktop/Game/trans/" + str(f) + ".png", scale=0.75, center_x=c[0],
                                       center_y=c[1])
            self.translist.append(self.trans)
            self.transindlist.append(f)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        if(not self.startgame):
            self.startbutton.draw()
        if (self.pause):
            self.pausebg.draw()
            self.resumebutton.draw()
        if(self.startgame and not self.pause):
            if(not self.win and self.time>0):
                arcade.draw_text("Score : "+str(int(self.score)),20,700,arcade.color.BLACK,anchor_x="left",anchor_y="top",font_size=20)
                arcade.draw_text("Time : "+str(int(self.time)+1),20,670,arcade.color.BLACK,anchor_x="left",anchor_y="top",font_size=20)
                self.pausebutton.draw()
                self.restartbutton.draw()
                if (len(self.selectedframe) != 0):
                    self.selectedframe.draw()
                if (self.wrongselection == True and self.score > 0):
                    arcade.draw_text("Wrong!!! -5", 480, 600, font_size=60, color=arcade.color.RED_PURPLE)
                if (self.wrongselection == True and self.score == 0):
                    arcade.draw_text("Wrong!!!", 480, 600, font_size=60, color=arcade.color.RED_PURPLE)
                if (self.wrongselection == False):
                    arcade.draw_text("Correct :D +20", 430, 600, font_size=60, color=arcade.color.GREEN)
            self.covocabbg.draw()
            if (len(self.collectedvocab) != 0):
                self.collectedvocab.draw()
            if (len(self.collectedtrans) != 0):
                self.collectedtrans.draw()
            self.vocablist.draw()
            self.translist.draw()
            if(self.time<=0 and not self.win):
                self.timeupbg.draw()
                arcade.draw_text("Time's Up\n\nScore : "+str(self.score),280,270,font_size=60,color=arcade.color.RED)
                self.restartbutton2.draw()
            if(self.win):
                self.winbg.draw()
                arcade.draw_text(
                    "You Win\nScore : " + str(self.score) + "\nTime used : " + str(int(self.starttime - self.time + 1)),
                    230, 260, font_size=60, color=arcade.color.GREEN)
                self.restartbutton2.draw()

    def on_update(self, delta_time):
        self.deselect=False
        if(self.startgame and not self.pause):
            if(len(self.selecteditem)>=2):
                self.wrongselection = False
                if(self.selecteditem[0] in self.vocablist):
                    if(self.selecteditem[1] in self.translist):
                        if(self.selectedind[0]==self.selectedind[1]):
                            self.collect+=1
                            self.vocabindlist.remove(self.selectedind[0])
                            self.vocablist.remove(self.selecteditem[0])
                            self.vocab = arcade.Sprite(
                                "C:/Users/CRP/Desktop/Game/vocab/" + str(self.selectedind[1]) + ".png", scale=0.6,
                                center_x=self.colvopo[self.collect - 1][0], center_y=self.colvopo[self.collect - 1][1])
                            self.collectedvocab.append(self.vocab)
                            self.transindlist.remove(self.selectedind[1])
                            self.translist.remove(self.selecteditem[1])
                            self.trans = arcade.Sprite(
                                "C:/Users/CRP/Desktop/Game/trans/" + str(self.selectedind[1]) + ".png", scale=0.6,
                                center_x=self.coltrpo[self.collect - 1][0], center_y=self.coltrpo[self.collect - 1][1])
                            self.collectedtrans.append(self.trans)
                            self.score+=20
                        else:
                            self.wrongselection=True
                            if(self.score>0):
                                self.score-=5
                    else:
                        self.wrongselection = True
                        if (self.score > 0):
                            self.score -= 5
                elif(self.selecteditem[0] in self.translist):
                    if(self.selecteditem[1] in self.vocablist):
                        if(self.selectedind[0]==self.selectedind[1]):
                            self.collect += 1
                            self.vocabindlist.remove(self.selectedind[1])
                            self.vocablist.remove(self.selecteditem[1])
                            self.vocab = arcade.Sprite(
                                "C:/Users/CRP/Desktop/Game/vocab/" + str(self.selectedind[0]) + ".png", scale=0.6,
                                center_x=self.colvopo[self.collect - 1][0], center_y=self.colvopo[self.collect - 1][1])
                            self.collectedvocab.append(self.vocab)
                            self.transindlist.remove(self.selectedind[0])
                            self.translist.remove(self.selecteditem[0])
                            self.trans = arcade.Sprite(
                                "C:/Users/CRP/Desktop/Game/trans/" + str(self.selectedind[0]) + ".png", scale=0.6,
                                center_x=self.coltrpo[self.collect - 1][0], center_y=self.coltrpo[self.collect - 1][1])
                            self.collectedtrans.append(self.trans)
                            self.score+=20
                        else:
                            self.wrongselection=True
                            if (self.score > 0):
                                self.score -= 5
                    else:
                        self.wrongselection = True
                        if (self.score > 0):
                            self.score -= 5
                self.selecteditem=arcade.SpriteList()
                self.selectedind=[]
                self.selectedframe=arcade.SpriteList()
                self.selected_position_list=[]
            self.vocablist.update()
            self.translist.update()
            if(self.time>0 and len(self.vocablist)!=0 and len(self.translist)!=0):
                self.time-=delta_time
            else:
                self.vocablist=arcade.SpriteList()
                self.translist=arcade.SpriteList()
                self.wrongselection="end"
                self.end=True
                if(self.time>0):
                    self.win=True
        elif(self.pause):
            arcade.pause(0.01)
        if(self.restart):
            Game1.setup()

    def on_mouse_press(self,x,y,button,modifiers):
        if (button == arcade.MOUSE_BUTTON_LEFT):
            if(self.startgame and not self.pause and self.time>0 and len(self.vocablist)!=0 and len(self.translist)!=0):
                if(len(self.selecteditem)==0):
                    for i in range(len(self.vocablist)):
                        cenx=self.vocablist[i].position[0]
                        ceny=self.vocablist[i].position[1]
                        if(x<=cenx+75 and x>=cenx-75 and y<=ceny+75 and y>=ceny-75):
                            if (cenx,ceny) not in self.selected_position_list:
                                self.selected_position_list.append((cenx,ceny))
                                frame = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/select.png", scale=2.5,
                                                      center_x=cenx, center_y=ceny)
                                self.selectedframe.append(frame)
                                self.selecteditem.append(self.vocablist[i])
                                self.selectedind.append(self.vocabindlist[i])
                    for i in range(len(self.translist)):
                        cenx=self.translist[i].position[0]
                        ceny=self.translist[i].position[1]
                        if(x<=cenx+75 and x>=cenx-75 and y<=ceny+75 and y>=ceny-75):
                            if (cenx,ceny) not in self.selected_position_list:
                                self.selected_position_list.append((cenx,ceny))
                                frame = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/select.png", scale=2.5,
                                                      center_x=cenx, center_y=ceny)
                                self.selectedframe.append(frame)
                                self.selecteditem.append(self.translist[i])
                                self.selectedind.append(self.transindlist[i])
                else:
                    cenx=self.selecteditem[0].position[0]
                    ceny=self.selecteditem[0].position[1]
                    if (x <= cenx + 75 and x >= cenx - 75 and y <= ceny + 75 and y >= ceny - 75):
                        if (cenx, ceny) in self.selected_position_list:
                            self.selected_position_list = []
                            self.selectedframe = arcade.SpriteList()
                            self.selecteditem = arcade.SpriteList()
                            self.deselect=True
                    if(not self.deselect and self.selecteditem[0] in self.translist):
                        for i in range(len(self.vocablist)):
                            cenx = self.vocablist[i].position[0]
                            ceny = self.vocablist[i].position[1]
                            if (x <= cenx + 75 and x >= cenx - 75 and y <= ceny + 75 and y >= ceny - 75):
                                if (cenx, ceny) not in self.selected_position_list:
                                    self.selected_position_list.append((cenx, ceny))
                                    frame = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/select.png", scale=2.5,
                                                          center_x=cenx, center_y=ceny)
                                    self.selectedframe.append(frame)
                                    self.selecteditem.append(self.vocablist[i])
                                    self.selectedind.append(self.vocabindlist[i])
                                else:
                                    self.selected_position_list = []
                                    self.selectedframe = arcade.SpriteList()
                                    self.selecteditem = arcade.SpriteList()
                    if(not self.deselect and self.selecteditem[0] in self.vocablist):
                        for i in range(len(self.translist)):
                            cenx = self.translist[i].position[0]
                            ceny = self.translist[i].position[1]
                            if (x <= cenx + 75 and x >= cenx - 75 and y <= ceny + 75 and y >= ceny - 75):
                                if (cenx, ceny) not in self.selected_position_list:
                                    self.selected_position_list.append((cenx, ceny))
                                    frame = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/select.png", scale=2.5,
                                                          center_x=cenx, center_y=ceny)
                                    self.selectedframe.append(frame)
                                    self.selecteditem.append(self.translist[i])
                                    self.selectedind.append(self.transindlist[i])
                                else:
                                    self.selected_position_list = []
                                    self.selectedframe = arcade.SpriteList()
                                    self.selecteditem = arcade.SpriteList()
            if(not self.startgame and not self.end):
                if(x<=790 and x>=490 and y<=460 and y>=260):
                    self.startgame=True
            elif(self.startgame and not self.end):
                if(x <= 1150 and x >= 1050 and y <= 700 and y >= 600 and not self.pause):
                    self.restart = True
                if (x <= 1260 and x >= 1160 and y <= 700 and y >= 600 and not self.pause):
                    self.pause = True
                elif (x <= 760 and x >= 520 and y <= 400 and y >= 240 and self.pause):
                    self.pause = False
            if(self.end):
                if(x <= 1260 and x >= 1160 and y <= 700 and y >= 600 and not self.pause):
                    self.restart=True

    def on_mouse_release(self, x, y, button,modifiers):
        pass

class Vocabulary(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title,resizable=True)
        self.set_location(10,40)

        arcade.set_background_color(arcade.color.APRICOT)

        self.vocablist=None
        self.translist=None
        self.firstpage=None
        self.lastpage=None
        self.pageind=1
        self.firstvocabnum=1
        self.lastvocabnum=70
        self.lastpageind=self.lastvocabnum//3
        if(self.lastvocabnum%3!=0):
            self.lastpageind+=1
        self.pagechange=None

    def setup(self):
        self.background = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/shelf.png",center_x=640,center_y=360)
        self.leftbutton = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/left.png",center_x=180,center_y=360)
        self.rightbutton = arcade.Sprite("C:/Users/CRP/Desktop/Game/other/right.png",center_x=1100,center_y=360)
        self.pagechange=False
        if(self.pageind==1):
            self.firstpage=True
        elif(self.pageind==self.lastpageind):
            self.lastpage=True
        else:
            self.firstpage=False
            self.lastpage=False
        self.vocablist=arcade.SpriteList()
        self.translist=arcade.SpriteList()
        if (not self.lastpage):
            for i in range(self.firstvocabnum,self.firstvocabnum+3):
                self.vocab=arcade.Sprite("C:/Users/CRP/Desktop/Game/vocab/" + str(i) + ".png",center_x=510,center_y=485-(157*(i-self.firstvocabnum)))
                self.vocablist.append(self.vocab)
            for j in range(self.firstvocabnum,self.firstvocabnum+3):
                self.trans = arcade.Sprite("C:/Users/CRP/Desktop/Game/trans/" + str(j) + ".png", center_x=760,
                                       center_y=485 - (157 * (j - self.firstvocabnum)))
                self.translist.append(self.trans)
        else:
            for i in range(self.firstvocabnum,self.lastvocabnum+1):
                self.vocab=arcade.Sprite("C:/Users/CRP/Desktop/Game/vocab/" + str(i) + ".png",center_x=510,center_y=485-(157*(i-self.firstvocabnum)))
                self.vocablist.append(self.vocab)
            for j in range(self.firstvocabnum,self.lastvocabnum+1):
                self.trans = arcade.Sprite("C:/Users/CRP/Desktop/Game/trans/" + str(j) + ".png", center_x=760,
                                       center_y=485 - (157 * (j - self.firstvocabnum)))
                self.translist.append(self.trans)
    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        self.vocablist.draw()
        self.translist.draw()
        if(self.firstpage):
            self.rightbutton.draw()
        elif(self.lastpage):
            self.leftbutton.draw()
        else:
            self.leftbutton.draw()
            self.rightbutton.draw()
        arcade.draw_text("Page " + str(self.pageind), 500, 580, color=arcade.color.WHITE, font_size=72)
        
    def on_update(self, delta_time):
        if(self.pagechange):
            VocabPage.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        if(button==arcade.MOUSE_BUTTON_LEFT):
            if(not self.lastpage and x>=1050 and x<=1150 and y>=310 and y<=410):
                self.pageind+=1
                self.firstvocabnum+=3
                self.pagechange=True
            if(not self.firstpage and x>=130 and x<=230 and y>=310 and y<=410):
                self.pageind-=1
                self.firstvocabnum-=3
                self.pagechange=True

    def on_key_press(self, symbol, modifiers):
        if(symbol==arcade.key.LEFT and not self.firstpage):
            self.pageind -= 1
            self.firstvocabnum -= 3
            self.pagechange = True
        if(symbol==arcade.key.RIGHT and not self.lastpage):
            self.pageind += 1
            self.firstvocabnum += 3
            self.pagechange = True


#Game1 = PairingGame(Screen_Width, Screen_Height, "Pairing Vocabularies")
#Game1.setup()
VocabPage=Vocabulary(Screen_Width,Screen_Height,"Vocabulary Book")
VocabPage.setup()
arcade.run()