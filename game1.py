import arcade
import random
import timeit
import time
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Langcade"


class PairingGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.startbutton = arcade.Sprite("Root2/other/start.png", center_x=700, center_y=360)
        self.vaultbutton = arcade.Sprite("butt/Vault.png",1, center_x=500, center_y=410)
        self.homebutton = arcade.Sprite("butt/b19_red.png",1, center_x=500, center_y=310)
        self.resumebutton = arcade.Sprite("Root2/other/resume2.png", center_x=640, center_y=320)
        self.pausebutton = arcade.Sprite("Root2/other/pause.png", center_x=1100, center_y=650)
        self.background = arcade.Sprite("Root2/other/background.png", center_x=640, center_y=360)
        self.covocabbg = arcade.Sprite("Root2/other/covoc.png", center_x=1055, center_y=290)
        self.winbg = arcade.Sprite("Root2/other/win2.png", center_x=430, center_y=360)
        self.pausebg = arcade.Sprite("Root2/other/pausebg2.png", center_x=640, center_y=360)
        self.timeupbg = arcade.Sprite("Root2/other/timeup2.png", center_x=430, center_y=360)
        self.restartbutton = arcade.Sprite("butt/b25.png", center_x=1210, center_y=650)
        self.restartbutton2 = arcade.Sprite("Root2/other/restart.png", center_x=1100, center_y=650)
        arcade.set_background_color(arcade.color.APRICOT)

    def setup(self):
        self.end = False
        self.restart = False
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
            self.vocab = arcade.Sprite("Root2/vocab/" + str(f) + ".png", scale=0.75, center_x=c[0],
                                       center_y=c[1])
            self.vocablist.append(self.vocab)
            self.vocabindlist.append(f)
        for i in range(6, 11):
            c = self.sprite_position_list[i - 1]
            f = self.file_vallist[i - 6]
            self.trans = arcade.Sprite("Root2/trans/" + str(f) + ".png", scale=0.75, center_x=c[0],
                                       center_y=c[1])
            self.translist.append(self.trans)
            self.transindlist.append(f)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        if (not self.startgame):
            self.startbutton.draw()
            self.homebutton.draw()
            self.vaultbutton.draw()
        if (self.pause):
            self.pausebg.draw()
            self.resumebutton.draw()
        if (self.startgame and not self.pause):
            if (not self.win and self.time > 0):
                arcade.draw_text("Score : " + str(int(self.score)), 20, 700, arcade.color.BLACK, anchor_x="left",
                                 anchor_y="top", font_size=20)
                arcade.draw_text("Time : " + str(int(self.time) + 1), 20, 670, arcade.color.BLACK, anchor_x="left",
                                 anchor_y="top", font_size=20)
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
            if (self.time <= 0 and not self.win):
                self.timeupbg.draw()
                arcade.draw_text("Time's Up\n\nScore : " + str(self.score), 280, 270, font_size=60,
                                 color=arcade.color.RED)
                self.restartbutton2.draw()
            if (self.win):
                self.winbg.draw()
                arcade.draw_text(
                    "You Win\nScore : " + str(self.score) + "\nTime used : " + str(int(self.starttime - self.time + 1)),
                    230, 260, font_size=60, color=arcade.color.GREEN)
                self.restartbutton2.draw()
                self.restartbutton.draw()

    def on_update(self, delta_time):
        self.deselect = False
        if (self.startgame and not self.pause):
            if (len(self.selecteditem) >= 2):
                self.wrongselection = False
                if (self.selecteditem[0] in self.vocablist):
                    if (self.selecteditem[1] in self.translist):
                        if (self.selectedind[0] == self.selectedind[1]):
                            self.collect += 1
                            self.vocabindlist.remove(self.selectedind[0])
                            self.vocablist.remove(self.selecteditem[0])
                            self.vocab = arcade.Sprite(
                                "Root2/vocab/" + str(self.selectedind[1]) + ".png", scale=0.6,
                                center_x=self.colvopo[self.collect - 1][0], center_y=self.colvopo[self.collect - 1][1])
                            self.collectedvocab.append(self.vocab)
                            self.transindlist.remove(self.selectedind[1])
                            self.translist.remove(self.selecteditem[1])
                            self.trans = arcade.Sprite(
                                "Root2/trans/" + str(self.selectedind[1]) + ".png", scale=0.6,
                                center_x=self.coltrpo[self.collect - 1][0], center_y=self.coltrpo[self.collect - 1][1])
                            self.collectedtrans.append(self.trans)
                            self.score += 20
                            Playsound("correct")
                        else:
                            self.wrongselection = True
                            Playsound("wrong")
                            if (self.score > 0):
                                self.score -= 5
                    else:
                        self.wrongselection = True
                        Playsound("wrong")
                        if (self.score > 0):
                            self.score -= 5
                elif (self.selecteditem[0] in self.translist):
                    if (self.selecteditem[1] in self.vocablist):
                        if (self.selectedind[0] == self.selectedind[1]):
                            self.collect += 1
                            self.vocabindlist.remove(self.selectedind[1])
                            self.vocablist.remove(self.selecteditem[1])
                            self.vocab = arcade.Sprite(
                                "Root2/vocab/" + str(self.selectedind[0]) + ".png", scale=0.6,
                                center_x=self.colvopo[self.collect - 1][0], center_y=self.colvopo[self.collect - 1][1])
                            self.collectedvocab.append(self.vocab)
                            self.transindlist.remove(self.selectedind[0])
                            self.translist.remove(self.selecteditem[0])
                            self.trans = arcade.Sprite(
                                "Root2/trans/" + str(self.selectedind[0]) + ".png", scale=0.6,
                                center_x=self.coltrpo[self.collect - 1][0], center_y=self.coltrpo[self.collect - 1][1])
                            self.collectedtrans.append(self.trans)
                            self.score += 20
                            Playsound("correct")
                        else:
                            self.wrongselection = True
                            Playsound("wrong")
                            if (self.score > 0):
                                self.score -= 5

                    else:
                        self.wrongselection = True
                        Playsound("wrong")
                        if (self.score > 0):
                            self.score -= 5
                self.selecteditem = arcade.SpriteList()
                self.selectedind = []
                self.selectedframe = arcade.SpriteList()
                self.selected_position_list = []
            self.vocablist.update()
            self.translist.update()
            if (self.time > 0 and len(self.vocablist) != 0 and len(self.translist) != 0):
                self.time -= delta_time
            else:
                self.vocablist = arcade.SpriteList()
                self.translist = arcade.SpriteList()
                self.wrongselection = "end"
                if self.end ==False:
                    Playsound("yay")
                self.end = True
                if (self.time > 0):
                    self.win = True
        elif (self.pause):
            arcade.pause(0.01)
        if (self.restart):
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        if (button == arcade.MOUSE_BUTTON_LEFT):
            if (self.startgame and not self.pause and self.time > 0 and len(self.vocablist) != 0 and len(
                    self.translist) != 0):
                if (len(self.selecteditem) == 0):
                    for i in range(len(self.vocablist)):
                        cenx = self.vocablist[i].position[0]
                        ceny = self.vocablist[i].position[1]
                        if (x <= cenx + 75 and x >= cenx - 75 and y <= ceny + 75 and y >= ceny - 75):
                            if (cenx, ceny) not in self.selected_position_list:
                                self.selected_position_list.append((cenx, ceny))
                                frame = arcade.Sprite("Root2/other/select.png", scale=2.5,
                                                      center_x=cenx, center_y=ceny)
                                self.selectedframe.append(frame)
                                Playsound("hit_butt")
                                self.selecteditem.append(self.vocablist[i])
                                self.selectedind.append(self.vocabindlist[i])
                    for i in range(len(self.translist)):
                        cenx = self.translist[i].position[0]
                        ceny = self.translist[i].position[1]
                        if (x <= cenx + 75 and x >= cenx - 75 and y <= ceny + 75 and y >= ceny - 75):
                            if (cenx, ceny) not in self.selected_position_list:
                                self.selected_position_list.append((cenx, ceny))
                                frame = arcade.Sprite("Root2/other/select.png", scale=2.5,
                                                      center_x=cenx, center_y=ceny)
                                Playsound("hit_butt")
                                self.selectedframe.append(frame)
                                self.selecteditem.append(self.translist[i])
                                self.selectedind.append(self.transindlist[i])
                else:
                    cenx = self.selecteditem[0].position[0]
                    ceny = self.selecteditem[0].position[1]
                    if (x <= cenx + 75 and x >= cenx - 75 and y <= ceny + 75 and y >= ceny - 75):
                        if (cenx, ceny) in self.selected_position_list:
                            self.selected_position_list = []
                            self.selectedframe = arcade.SpriteList()
                            self.selecteditem = arcade.SpriteList()
                            Playsound("hit_butt")
                            self.deselect = True
                    if (not self.deselect and self.selecteditem[0] in self.translist):
                        for i in range(len(self.vocablist)):
                            cenx = self.vocablist[i].position[0]
                            ceny = self.vocablist[i].position[1]
                            if (x <= cenx + 75 and x >= cenx - 75 and y <= ceny + 75 and y >= ceny - 75):
                                if (cenx, ceny) not in self.selected_position_list:
                                    self.selected_position_list.append((cenx, ceny))
                                    frame = arcade.Sprite("Root2/other/select.png", scale=2.5,
                                                          center_x=cenx, center_y=ceny)
                                    self.selectedframe.append(frame)
                                    self.selecteditem.append(self.vocablist[i])
                                    Playsound("hit_butt")
                                    self.selectedind.append(self.vocabindlist[i])
                                else:
                                    self.selected_position_list = []
                                    self.selectedframe = arcade.SpriteList()
                                    self.selecteditem = arcade.SpriteList()
                                    Playsound("hit_butt")
                    if (not self.deselect and self.selecteditem[0] in self.vocablist):
                        for i in range(len(self.translist)):
                            cenx = self.translist[i].position[0]
                            ceny = self.translist[i].position[1]
                            if (x <= cenx + 75 and x >= cenx - 75 and y <= ceny + 75 and y >= ceny - 75):
                                if (cenx, ceny) not in self.selected_position_list:
                                    self.selected_position_list.append((cenx, ceny))
                                    frame = arcade.Sprite("Root2/other/select.png", scale=2.5,
                                                          center_x=cenx, center_y=ceny)
                                    self.selectedframe.append(frame)
                                    self.selecteditem.append(self.translist[i])
                                    Playsound("hit_butt")
                                    self.selectedind.append(self.transindlist[i])
                                else:
                                    self.selected_position_list = []
                                    self.selectedframe = arcade.SpriteList()
                                    self.selecteditem = arcade.SpriteList()
                                    Playsound("hit_butt")
            if (not self.startgame and not self.end):
                if (x <= 850 and x >= 540 and y <= 460 and y >= 260):
                    self.startgame = True
                    Playsound("enter")
                if (x <= 540 and x >= 440 and y <= 360 and y >= 260):
                    print("Home")
                    Playsound("enter")
                    menu_view = Mainmenu()
                    self.window.show_view(menu_view)
                if (x <= 540 and x >= 440 and y <= 460 and y >= 360):
                    print("vocab1")
                    Playsound("enter")
                    vocab1_view = Vocabulary()
                    vocab1_view.setup()
                    self.window.show_view(vocab1_view)
            elif (self.startgame and not self.end):
                if (x <= 1260 and x >= 1160 and y <= 700 and y >= 600 and not self.pause):
                    Playsound("enter")
                    self.restart = True
                if (x <= 1150 and x >= 1050  and y <= 700 and y >= 600 and not self.pause):
                    Playsound("enter")
                    self.pause = True
                elif (x <= 760 and x >= 520 and y <= 400 and y >= 240 and self.pause):
                    Playsound("enter")
                    self.pause = False
            if (self.end):
                if (x <= 1260 and x >= 1160 and y <= 700 and y >= 600 and not self.pause):
                    Playsound("enter")
                    self.restart = True
                if (x <= 1150 and x >= 1050  and y <= 700 and y >= 600 and not self.pause):
                    Playsound("enter")
                    self.setup()
                    self.startgame = True

    def on_mouse_release(self, x, y, button, modifiers):
        pass


class Vocabulary(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.APRICOT)

        self.vocablist = None
        self.translist = None
        self.firstpage = None
        self.lastpage = None
        self.bg = arcade.SpriteList()
        self.left = arcade.SpriteList()
        self.right = arcade.SpriteList()
        background = arcade.Sprite("Root2/other/shelf2.png", center_x=640, center_y=360)
        leftbutton = arcade.Sprite("Root2/other/left.png",.75, center_x=520, center_y=40)
        rightbutton = arcade.Sprite("Root2/other/right.png",.75, center_x=680, center_y=40)
        self.bg.append(background)
        self.left.append(leftbutton)
        self.right.append(rightbutton)
        self.pageind = 1
        self.firstvocabnum = 1
        self.lastvocabnum = 70
        self.lastpageind = self.lastvocabnum // 3
        if (self.lastvocabnum % 3 != 0):
            self.lastpageind += 1
        self.pagechange = None

    def setup(self):
        self.pagechange = False
        if (self.pageind == 1):
            self.firstpage = True
        elif (self.pageind == self.lastpageind):
            self.lastpage = True
        else:
            self.firstpage = False
            self.lastpage = False
        self.vocablist = arcade.SpriteList()
        self.translist = arcade.SpriteList()
        if (not self.lastpage):
            for i in range(self.firstvocabnum, self.firstvocabnum + 3):
                self.vocab = arcade.Sprite("Root2/vocab/" + str(i) + ".png", center_x=510,
                                           center_y=485 - (157 * (i - self.firstvocabnum)))
                self.vocablist.append(self.vocab)
            for j in range(self.firstvocabnum, self.firstvocabnum + 3):
                self.trans = arcade.Sprite("Root2/trans/" + str(j) + ".png", center_x=760,
                                           center_y=485 - (157 * (j - self.firstvocabnum)))
                self.translist.append(self.trans)
        else:
            for i in range(self.firstvocabnum, self.lastvocabnum + 1):
                self.vocab = arcade.Sprite("Root2/vocab/" + str(i) + ".png", center_x=510,
                                           center_y=485 - (157 * (i - self.firstvocabnum)))
                self.vocablist.append(self.vocab)
            for j in range(self.firstvocabnum, self.lastvocabnum + 1):
                self.trans = arcade.Sprite("Root2/trans/" + str(j) + ".png", center_x=760,
                                           center_y=485 - (157 * (j - self.firstvocabnum)))
                self.translist.append(self.trans)

    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
        self.vocablist.draw()
        self.translist.draw()
        if (self.firstpage):
            self.right.draw()
        elif (self.lastpage):
            self.left.draw()
        else:
            self.left.draw()
            self.right.draw()
        arcade.draw_text(str(self.pageind), 600, 41, color=arcade.color.BLACK, font_size=47, anchor_x="center",anchor_y="center", font_name='plex')
        arcade.draw_text(str(self.pageind), 600, 44, color=arcade.color.WHITE, font_size=45,anchor_x="center",anchor_y="center", font_name='plex')

    def on_update(self, delta_time):
        if (self.pagechange):
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        if (button == arcade.MOUSE_BUTTON_LEFT):
            if y >= 1.5 and y <= 76.5:
                if (not self.lastpage and x >= 642.5 and x <= 717.5):
                    self.pageind += 1
                    self.firstvocabnum += 3
                    self.pagechange = True
                    Playsound("UI_butt")
                if (not self.firstpage and x >= 482.5 and x <= 557.5 ):
                    self.pageind -= 1
                    self.firstvocabnum -= 3
                    self.pagechange = True
                    Playsound("UI_butt")
                if x>= 314 and x<= 390:
                    menu_view = Mainmenu()
                    self.window.show_view(menu_view)
                    Playsound("enter")
                if x >= 814 and x <= 964:
                    game1_view = PairingGame()
                    game1_view.setup()
                    self.window.show_view(game1_view)
                    Playsound("enter")

    def on_key_press(self, symbol, modifiers):
        if (symbol == arcade.key.LEFT and not self.firstpage):
            self.pageind -= 1
            self.firstvocabnum -= 3
            self.pagechange = True
            Playsound("UI_butt")
        if (symbol == arcade.key.RIGHT and not self.lastpage):
            self.pageind += 1
            self.firstvocabnum += 3
            self.pagechange = True
            Playsound("UI_butt")
class Vocabulary2(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.APRICOT)

        self.vocablist = None
        self.translist = None
        self.firstpage = None
        self.lastpage = None
        self.bg = arcade.SpriteList()
        self.left = arcade.SpriteList()
        self.right = arcade.SpriteList()
        background = arcade.Sprite("Root2/other/shelf2.png", center_x=640, center_y=360)
        leftbutton = arcade.Sprite("Root2/other/left.png",.75, center_x=520, center_y=40)
        rightbutton = arcade.Sprite("Root2/other/right.png",.75, center_x=680, center_y=40)
        self.bg.append(background)
        self.left.append(leftbutton)
        self.right.append(rightbutton)
        self.pageind = 1
        self.firstvocabnum = 0
        self.lastvocabnum = 39
        self.lastpageind = (self.lastvocabnum+1) // 3
        if ((self.lastvocabnum+1) % 3 != 0):
            self.lastpageind += 1
        self.pagechange = None

    def setup(self):
        self.pagechange = False
        if (self.pageind == 1):
            self.firstpage = True
        elif (self.pageind == self.lastpageind):
            self.lastpage = True
        else:
            self.firstpage = False
            self.lastpage = False
        self.vocablist = arcade.SpriteList()
        self.translist = arcade.SpriteList()
        if (not self.lastpage):
            for i in range(self.firstvocabnum, self.firstvocabnum + 3):
                self.vocab = arcade.Sprite("Pictures/" + str(i) + ".png",.7, center_x=510,
                                           center_y=485 - (157 * (i - self.firstvocabnum)))
                self.vocablist.append(self.vocab)
            for j in range(self.firstvocabnum, self.firstvocabnum + 3):
                self.trans = arcade.Sprite("Picture_trans/" + str(j) + ".png", center_x=760,
                                           center_y=485 - (157 * (j - self.firstvocabnum)))
                self.translist.append(self.trans)
        else:
            for i in range(self.firstvocabnum, self.lastvocabnum + 1):
                self.vocab = arcade.Sprite("Pictures/" + str(i) + ".png",.7, center_x=510,
                                           center_y=485 - (157 * (i - self.firstvocabnum)))
                self.vocablist.append(self.vocab)
            for j in range(self.firstvocabnum, self.lastvocabnum + 1):
                self.trans = arcade.Sprite("Picture_trans/" + str(j) + ".png", center_x=760,
                                           center_y=485 - (157 * (j - self.firstvocabnum)))
                self.translist.append(self.trans)

    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
        self.vocablist.draw()
        self.translist.draw()
        if (self.firstpage):
            self.right.draw()
        elif (self.lastpage):
            self.left.draw()
        else:
            self.left.draw()
            self.right.draw()
        arcade.draw_text(str(self.pageind), 600, 41, color=arcade.color.BLACK, font_size=47, anchor_x="center",anchor_y="center", font_name='plex')
        arcade.draw_text(str(self.pageind), 600, 44, color=arcade.color.WHITE, font_size=45,anchor_x="center",anchor_y="center", font_name='plex')

    def on_update(self, delta_time):
        if (self.pagechange):
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        if (button == arcade.MOUSE_BUTTON_LEFT):
            if y >= 1.5 and y <= 76.5:
                if (not self.lastpage and x >= 642.5 and x <= 717.5):
                    self.pageind += 1
                    self.firstvocabnum += 3
                    self.pagechange = True
                    Playsound("UI_butt")
                if (not self.firstpage and x >= 482.5 and x <= 557.5 ):
                    self.pageind -= 1
                    self.firstvocabnum -= 3
                    self.pagechange = True
                    Playsound("UI_butt")
                if x>= 314 and x<= 390:
                    menu_view = Mainmenu()
                    Playsound("enter")
                    self.window.show_view(menu_view)
                if x >= 814 and x <= 964:
                    game2_view = TypeGame()
                    game2_view.Startnewgame()
                    Playsound("enter")
                    self.window.show_view(game2_view)

    def on_key_press(self, symbol, modifiers):
        if (symbol == arcade.key.LEFT and not self.firstpage):
            self.pageind -= 1
            self.firstvocabnum -= 3
            self.pagechange = True
            Playsound("UI_butt")
        if (symbol == arcade.key.RIGHT and not self.lastpage):
            self.pageind += 1
            self.firstvocabnum += 3
            self.pagechange = True
            Playsound("UI_butt")
class TypeGuide:
    def __init__(self,size,width_p_char,screen_w):
        self.size = size
        self.width_p_char = width_p_char;
        self.screen_w = screen_w
        self.startx=0
        self.starty=100
        self.now_word = ""
        self.target = ""

    def drawnew(self,word,Hints):
        self.Hint = Hints
        self.target = word
        all_l = self.width_p_char*len(word)
        self.startx = self.screen_w/2 - all_l/2
        txt = ""
        txt2 = ""
        for i in range(len(word)):
            if word[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                txt += " _"
                if i not in self.Hint:
                    txt2 += "  "
                else:
                    txt2 += f" {word[i]}"
            else:
                txt += f" {word[i]}"
                if word[i] != "-":
                    txt2 += f" {word[i]}"
                else:
                    txt2 += "  "
        arcade.draw_text(txt, self.startx, 50, arcade.color.YELLOW, 40, font_name='plex')
        arcade.draw_text(txt2, self.startx, 60, arcade.color.YELLOW, 40, font_name='plex')

    def gettxt(self,key):
        if(key == 65288 and len(self.now_word) != 0):
            pos = len(self.now_word)//2
            if pos+1 in self.Hint and len(self.now_word) > 2:
                self.now_word = self.now_word[0:len(self.now_word) - 4]
            else:
                self.now_word = self.now_word[0:len(self.now_word)-2]
        elif(key != 65288 and len(self.now_word) < 2*len(self.target) and chr(key-32) in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            pos = len(self.now_word)//2
            if self.target[pos] == ' ' or self.target[pos] == '-' or pos in self.Hint:
                self.now_word += "  "
            self.now_word += chr(key-32)+" "
class TypeGame(arcade.View):

    def __init__(self):
        super().__init__()
        self.startbutton = arcade.Sprite("Root2/other/start.png", center_x=700, center_y=360)
        self.vaultbutton = arcade.Sprite("butt/Vault.png",1, center_x=500, center_y=410)
        self.homebutton = arcade.Sprite("butt/b19_red.png",1, center_x=500, center_y=310)
        arcade.set_background_color(arcade.color.WHITE)
        #setting up processes
        self.TG = TypeGuide(5, 61, SCREEN_WIDTH)
        self.Dict = {0:"BAG",1:"BILL",2:"BOTTLE",3:"BOWL",4:"BROCCOLI",5:"CAN",6:"CARTON",7:"CHEF",8:"CUP",9:"DISH",10:"GLASS",11:"JAR",12:"MENU",13:"MILK",14:"MUG",15:"PACKET",16:"POTATOES",17:"SALMON",18:"STRAWBERRY",19:"TIP",
                         20:"APPLE",21:"WALKING BOOTS",22:"BUTTER",23:"BANANA",24:"CHICKEN",25:"CHEESE",26:"EGGS",27:"FRUIT JUICE",28:"GARLIC",29:"JEANS",30:"JACKET",31:"PEPPERS",32:"PEAR",33:"PRINTER",34:"SWEATER",35:"TRAINERS",36:"T-SHIRT",37:"TELEVISION",38:"WASHBASIN",39:"WARDROBE",}
        self.allwords = {}
        self.background = arcade.load_texture("bg.png")
        self.guide = arcade.load_texture("Goodwords/Enterword.png")
        self.top_x = 640
        self.top_y = 620
        self.pausebutt = arcade.load_texture("butt/b22.png")
        self.pausemenu = arcade.load_texture("paused.png")
        self.losepanel = arcade.load_texture("centerpanel.png")
        self.hintindex = []
    def Startnewgame(self):
        self.allwords = self.Dict.copy()
        r = random.randrange(len(self.allwords))
        self.R = list(self.allwords.keys())[r]
        self.theword = self.allwords[r]
        self.TG.now_word = ""
        self.start_time = timeit.default_timer()
        self.timetaken = 0
        self.Timer = 60-self.timetaken
        self.good_wordList = arcade.SpriteList()
        self.point = 0
        self.doDrawGood = False
        self.state = "Prestart"
        self.time1= timeit.default_timer()
        self.time2= timeit.default_timer()
        self.skipped_words = 0
        self.correct_words = 0
        self.wrong_words = 0
        self.hintindex = []
        isOK = False
        while isOK is False:
            isOK = self.Randoma()

    def Randoma(self):
        hintcount = len(list(self.theword))//3
        dont = [' ','_']
        for F in range(hintcount):
            a = random.randrange(len(list(self.theword)))
            for A in range(len(self.hintindex)):
                if a == self.hintindex[A]+1 or a == self.hintindex[A]-1 :
                    return False
                if a<len(list(self.theword))-1:
                    if list(self.theword)[a+1] in dont:
                        return  False
                if a > 0:
                    if list(self.theword)[a-1] in dont:
                        return  False
            self.hintindex.append(a)
        return  True
    def Generatenewword(self,iswin):
        self.good_wordList = arcade.SpriteList()
        self.TG.now_word = ""
        if len(self.allwords) <= 2:
            self.allwords = self.Dict.copy()
            print("words over")
        if iswin == 1:
            Playsound("correct")
            self.point +=3
            print("correct removed ",self.allwords[self.R]);
            del self.allwords[self.R]
            self.correct_words += 1
            rand = random.randrange(4)
            word = arcade.AnimatedTimeSprite(scale=0.5,center_x=640,center_y=205)
            word.textures = []
            word.textures.append(arcade.load_texture(f"Goodwords/good_{rand}_1.png"))
            word.textures.append(arcade.load_texture(f"Goodwords/good_{rand}_2.png"))
            word.scale = 1
            word.cur_texture_index = 0
            self.good_wordList.append(word)
        elif iswin==0:
            Playsound("wrong")
            self.point -= 2
            print("wrong removed ",self.allwords[self.R]);
            self.wrong_words += 1
            del self.allwords[self.R]
            rand = random.randrange(3)
            word = arcade.AnimatedTimeSprite(scale=0.5,center_x=640,center_y=205)
            word.textures = []
            word.textures.append(arcade.load_texture(f"Badwords/bad_{rand}_1.png"))
            word.textures.append(arcade.load_texture(f"Badwords/bad_{rand}_2.png"))
            word.scale = 1
            word.cur_texture_index = 0
            self.good_wordList.append(word)
        elif iswin == 2:
            self.point -= 1
            Playsound("wrong")
            print("skipped removed ",self.allwords[self.R]);
            del self.allwords[self.R]
            self.skipped_words += 1
            word = arcade.AnimatedTimeSprite(scale=0.5, center_x=640, center_y=202)
            word.textures = []
            word.textures.append(arcade.load_texture("Badwords/Skip_1.png"))
            word.textures.append(arcade.load_texture("Badwords/Skip_2.png"))
            word.textures.append(arcade.load_texture("Badwords/Skip_3.png"))
            word.scale = 1
            word.cur_texture_index = 0
            self.good_wordList.append(word)
        r = random.randrange(len(self.allwords))
        self.R = list(self.allwords.keys())[r]
        print("new word is ", self.Dict[self.R]);
        self.theword = self.allwords.__getitem__(self.R)
        self.hintindex = []
        isOK = False
        while isOK is False:
            isOK = self.Randoma()
        self.time1 = timeit.default_timer()
        self.doDrawGood = True

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        if self.state != "Prestart":
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                1280, 260,
                                                arcade.load_texture("fram1.png"))
            arcade.draw_lrwh_rectangle_textured(1160, 600,
                                                100, 100,
                                                self.pausebutt)
            if self.doDrawGood == False:
                arcade.draw_lrwh_rectangle_textured(330, 162,620,80,texture=self.guide)
            self.TG.drawnew(self.theword,self.hintindex)
            arcade.draw_text(f" {self.TG.now_word}", self.TG.startx,  60, arcade.color.YELLOW, 40, font_name='plex')
            arcade.draw_circle_filled(self.top_x,self.top_y,60,arcade.color.WHITE)
            arcade.draw_circle_outline(self.top_x, self.top_y, 60, arcade.color.BLACK,12)
            arcade.draw_text(str(self.Timer),self.top_x,self.top_y-5,arcade.color.BLACK,64,200,"center",anchor_x="center",
                             anchor_y="center")
            if self.time2 > .2 and len(self.good_wordList) != 0:
                self.good_wordList.draw()
                if self.time2 > 1.6:
                    self.doDrawGood = False
            arcade.draw_lrwh_rectangle_textured(500, 250,300, 300,arcade.load_texture(f"Pictures/{self.R}.png"))
        if self.state == "Pause":
            arcade.draw_lrwh_rectangle_textured(535, 85,
                                                210, 550,
                                                self.pausemenu)
        if self.state == "Lose":
            arcade.draw_lrwh_rectangle_textured(211.5, 80,
                                                857, 560,
                                                self.losepanel)
            arcade.draw_text(str(self.wrong_words), 481.5,312, arcade.color.RED, 40, 200, "center",
                             anchor_x="center",
                             anchor_y="center")
            arcade.draw_text(str(self.correct_words), 481.5, 435, arcade.color.GREEN, 40, 200, "center",
                             anchor_x="center",
                             anchor_y="center")
            arcade.draw_text(str(self.skipped_words), 481.5, 375, arcade.color.WHITE, 40, 200, "center",
                             anchor_x="center",
                             anchor_y="center")
            arcade.draw_text(str(self.point), 581.5, 180, arcade.color.ELECTRIC_CYAN, 100, 200, "center",
                             anchor_x="center",
                             anchor_y="center")
        if self.state == "Prestart":
            self.startbutton.draw()
            self.vaultbutton.draw()
            self.homebutton.draw()

    def on_key_press(self,key,modfiers):
        if self.state == "Start":
            Playsound("hit_butt")
            self.TG.gettxt(key)
        if key == 65293 and self.doDrawGood == False and self.state == "Start":
            iswin = 2
            if len(self.TG.now_word)/2 >= len(self.theword)-len(self.hintindex):
                w = self.TG.now_word.split(' ')
                coll = ""
                for Wor in w:
                    if Wor in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        coll += Wor
                w2 = list(self.theword)
                coll2 = ""
                for Wor2 in range(len(w2)):
                    if w2[Wor2] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and Wor2 not in self.hintindex:
                        coll2 += w2[Wor2]
                if coll == coll2:
                    iswin = 1
                else:
                    iswin = 0
                print(coll," and ",coll2)
            self.Generatenewword(iswin)

    def on_update(self, delta_time):
        if self.state == "Start":
            self.timetaken = timeit.default_timer()-self.start_time
            self.Timer = 60-int(self.timetaken)
        if self.Timer <= 0:
            self.Timer = 0
            if self.state != "Lose":
                Playsound("yay")
            self.state = "Lose"
        if self.doDrawGood == True:
            self.time2 = timeit.default_timer()-self.time1
        else:
            self.time2 = 0
        if self.time2 > .1 and len(self.good_wordList) != 0:
            self.good_wordList.update()
            self.good_wordList.update_animation()

    def on_mouse_press(self, x, y, button, modifiers):
        if (button == arcade.MOUSE_BUTTON_LEFT):
            if self.state == "Start":
                if (x,y) >= (1160,600) and (x,y) <= (1260,700):
                    Playsound("UI_butt")
                    self.state = "Pause"
            if self.state == "Prestart":
                if (x <= 850 and x >= 540 and y <= 460 and y >= 260):
                    self.state = "Start"
                    Playsound("enter")
                if (x <= 540 and x >= 440 and y <= 360 and y >= 260):
                    print("Home")
                    Playsound("enter")
                    menu_view = Mainmenu()
                    self.window.show_view(menu_view)
                if (x <= 540 and x >= 440 and y <= 460 and y >= 360):
                    print("vocab2")
                    Playsound("enter")
                    vocab2_view = Vocabulary2()
                    vocab2_view.setup()
                    self.window.show_view(vocab2_view)

            if self.state == "Pause":
                if x >= 540 and x<=740:
                    if y >= 485 and y <= 585:
                        Playsound("UI_butt")
                        self.state = "Start"
                    if y >= 370 and y <= 470:
                        self.Startnewgame()
                        Playsound("enter")
                    if y >= 260 and y <= 360:
                        print("vocab2")
                        Playsound("enter")
                        vocab2_view = Vocabulary2()
                        vocab2_view.setup()
                        self.window.show_view(vocab2_view)
                    if y >= 145 and y <= 245:
                        print("Home")
                        Playsound("enter")
                        menu_view = Mainmenu()
                        self.window.show_view(menu_view)
            if self.state == "Lose":
                if y >= 155 and y<=245:
                    if x >= 701.5 and x <= 801.5:
                        Playsound("enter")
                        self.Startnewgame()
                    if x >= 811.5 and x <= 911.5:
                        print("vocab2")
                        Playsound("enter")
                        vocab2_view = Vocabulary2()
                        vocab2_view.setup()
                        self.window.show_view(vocab2_view)
                    if x >= 911.5 and x <= 1021.5:
                        print("Home")
                        Playsound("enter")
                        menu_view = Mainmenu()
                        self.window.show_view(menu_view)

class Mainmenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("mainmenu.png")
    def on_mouse_press(self, x, y, button, modifiers):
        if (button == arcade.MOUSE_BUTTON_LEFT):
            if x>= 463 and x<=687:
                if y>=202 and y<=311:
                    print("game1")
                    Playsound("enter")
                    game1_view = PairingGame()
                    game1_view.setup()
                    self.window.show_view(game1_view)
                if y>= 83 and y <= 191:
                    print("game2")
                    Playsound("enter")
                    game2_view = TypeGame()
                    game2_view.Startnewgame()
                    self.window.show_view(game2_view)
            if x>= 696 and x<= 807:
                if y>=202 and y<=311:
                    print("vocab1")
                    Playsound("enter")
                    vocab1_view = Vocabulary()
                    vocab1_view.setup()
                    self.window.show_view(vocab1_view)
                if y>= 83 and y <= 191:
                    print("vocab2")
                    Playsound("enter")
                    vocab2_view = Vocabulary2()
                    vocab2_view.setup()
                    self.window.show_view(vocab2_view)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

def Playsound(name):
    a = arcade.load_sound(f"Sounds/{name}.wav")
    a.play(.2)
def main():
    a = arcade.load_sound("Sounds/menumusic.wav")
    a.play(.075)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_location(10,40)
    window.total_score = 0
    menu_view = Mainmenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()