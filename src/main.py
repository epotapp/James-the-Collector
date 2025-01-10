import pygame
from random import randint
from datetime import datetime, timedelta
 
class Collector:
    def __init__(self):
        pygame.init()
 
        self.width = 640
        self.height = 480
        
        self.load_images()
        self.new_game()
        
        self.window = pygame.display.set_mode((self.width, self.height))
        self.game_font = pygame.font.SysFont('Arial', 24)
        self.clock = pygame.time.Clock()
 
        pygame.display.set_caption('James the Collector')
 
        self.main_loop()
 
    def load_images(self):
        self.images = []
        for name in ['robot', 'coin', 'monster']:
            self.images.append(pygame.image.load(name + '.png'))
    
    def new_game(self):
        Jabba.gameover = False
        Coin.gold = 0
 
        self.start = datetime.now()
        self.finish = self.start + timedelta(minutes=2)
 
        self.left = 10
        self.right = self.width - self.images[0].get_width() - 10
        self.bottom = self.height - self.images[0].get_height() - 10
        self.borders = [self.left, self.right, self.bottom]
 
        self.robx = self.width/2-self.images[0].get_width()/2
        self.roby = self.bottom
 
        self.james = Robot(self.images[0], self.robx, self.roby, self.left, self.right, self.bottom)
        
        self.left_end = -48000
        self.right_end = 48000
        coins_amount_eachgun = 56
        jabbas_amount = 14
 
        self.coin_gun_topl = []
        self.coin_gun_topr = []
        self.coin_gun_botl = []
        self.coin_gun_botr = []
 
        for i in range(coins_amount_eachgun):
            coin = Coin(self.images[1], randint(self.left_end, self.left-100), 60-self.images[1].get_height(), 0, self.borders)
            self.coin_gun_topl.append(coin)
        for i in range(coins_amount_eachgun):
            coin = Coin(self.images[1], randint(self.width+100, self.right_end), 120-self.images[1].get_height(), 1, self.borders)
            self.coin_gun_topr.append(coin)
        for i in range(coins_amount_eachgun):
            coin = Coin(self.images[1], randint(self.left_end, self.left-100), 221-self.images[1].get_height(), 2, self.borders)
            self.coin_gun_botl.append(coin)
        for i in range(coins_amount_eachgun):
            coin = Coin(self.images[1], randint(self.width+100, self.right_end), 270-self.images[1].get_height(), 3, self.borders)
            self.coin_gun_botr.append(coin)
 
        self.jabba_gun_topl = []
        self.jabba_gun_topr = []
        self.jabba_gun_botl = []
        self.jabba_gun_botr = []
 
        for i in range(jabbas_amount):
            jabba = Jabba(self.images[2], randint(self.left_end, self.left-100), 60-self.images[2].get_height(), 0, self.left, self.right, self.bottom)
            self.jabba_gun_topl.append(jabba)
        for i in range(jabbas_amount):
            jabba = Jabba(self.images[2], randint(self.width+100, self.right_end), 120-self.images[2].get_height(), 1, self.left, self.right, self.bottom)
            self.jabba_gun_topr.append(jabba)
        for i in range(jabbas_amount):
            jabba = Jabba(self.images[2], randint(self.left_end, self.left-100), 221-self.images[2].get_height(), 2, self.left, self.right, self.bottom)
            self.jabba_gun_botl.append(jabba)
        for i in range(jabbas_amount):
            jabba = Jabba(self.images[2], randint(self.width+100, self.right_end), 270-self.images[2].get_height(), 3, self.left, self.right, self.bottom)
            self.jabba_gun_botr.append(jabba)
 
 
    def main_loop(self):
        while True:
            self.draw_window()
            self.check_events()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_F2:
                    self.new_game()
 
                if event.key == pygame.K_LEFT:
                    self.james.move_left = True
                if event.key == pygame.K_RIGHT:
                    self.james.move_right = True
                if event.key == pygame.K_SPACE:
                    self.james.jump = True
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.james.move_left = False
                if event.key == pygame.K_RIGHT:
                    self.james.move_right = False
                if event.key == pygame.K_SPACE:
                    self.james.jump = False
    
    def draw_window(self):
        now = datetime.now()
 
        if not Jabba.gameover and self.finish > now:
            self.render(self.finish - now)
            
            self.james.draw(self.window)
            self.james.move(self.james.move_left, self.james.move_right)
    
            self.coins_render(self.james.report())
            self.jabba_render(self.james.report())
        elif self.finish >= now:
            self.gameover()
        else:
            self.gameover()
        
        pygame.display.flip()
        self.clock.tick(60)
 
    def render(self, rest: timedelta):
        if Coin.gold < 25:
            level = self.game_font.render('Level 1: Forest', True, (255, 255, 255))
            self.window.fill((51, 196, 255))
            pygame.draw.rect(self.window, (177, 255, 111), (0, self.height/2+90, self.width, self.height/2-90))
        elif Coin.gold >= 25 and Coin.gold < 50:
            level = self.game_font.render('Level 2: Beach', True, (255, 255, 255))
            self.window.fill((0, 115, 255))
            pygame.draw.rect(self.window, (234, 255, 165), (0, self.height/2+90, self.width, self.height/2-90))
        elif Coin.gold >= 50 and Coin.gold < 100:
            level = self.game_font.render('Level 3: Snowy forest', True, (255, 255, 255))
            self.window.fill((196, 210, 229))
            pygame.draw.rect(self.window, (19, 159, 165), (0, self.height/2+90, self.width, self.height/2-90))
        elif Coin.gold >= 100 and Coin.gold < 150:
            level = self.game_font.render('Level 4: Sunset', True, (255, 255, 255))
            self.window.fill((255, 97, 27))
            pygame.draw.rect(self.window, (255, 229, 111), (0, self.height/2+90, self.width, self.height/2-90))
        else:
            level = self.game_font.render('Extra level: Glamourous', True, (255, 255, 255))
            self.window.fill((131, 83, 255))
            pygame.draw.rect(self.window, (255, 30, 180), (0, self.height/2+90, self.width, self.height/2-90))
 
        pygame.draw.rect(self.window, (45, 190, 0), (0, self.height-14, self.width, 4))
        pygame.draw.rect(self.window, (170, 100, 0), (0, self.height-10, self.width, 10))
 
        pygame.draw.rect(self.window, (45, 190, 0), (0, 61, 150, 4))
        pygame.draw.rect(self.window, (170, 100, 0), (0, 65, 150, 10))
        pygame.draw.rect(self.window, (45, 190, 0), (0, 222, 75, 4))
        pygame.draw.rect(self.window, (170, 100, 0), (0, 226, 75, 10))
 
        pygame.draw.rect(self.window, (45, 190, 0), (self.width-150, 121, 150, 4))
        pygame.draw.rect(self.window, (170, 100, 0), (self.width-150, 125, 150, 10))
        pygame.draw.rect(self.window, (45, 190, 0), (self.width-75, 271, 75, 4))
        pygame.draw.rect(self.window, (170, 100, 0), (self.width-75, 275, 75, 10))
 
        if Coin.gold >= 50 and Coin.gold < 100:
            pygame.draw.rect(self.window, (218, 248, 255), (0, self.height-14, self.width, 4))
            pygame.draw.rect(self.window, (218, 248, 255), (0, 61, 150, 4))
            pygame.draw.rect(self.window, (218, 248, 255), (0, 222, 75, 4))
            pygame.draw.rect(self.window, (218, 248, 255), (self.width-150, 121, 150, 4))
            pygame.draw.rect(self.window, (218, 248, 255), (self.width-75, 271, 75, 4))
 
        game_text = self.game_font.render('Gold: ' + str(Coin.gold), True, (255, 255, 255))
        self.window.blit(game_text, (self.width-140, 20))
 
        if rest.seconds%60 >= 10:
            time_text = str(rest.seconds//60) + ':' + str(rest.seconds%60)
        else:
            time_text = str(rest.seconds//60) + ':0' + str(rest.seconds%60)
        amount = self.game_font.render('Time left ' + time_text, True, (255, 255, 255))
        self.window.blit(amount, (40, 20))
        self.window.blit(level, (self.width/2-100, 20) )
    
    def coins_render(self, edges):
        for coin in self.coin_gun_topl:
            coin.move(edges)
            coin.draw(self.window)
            if coin.cought():
                self.coin_gun_topl.remove(coin)
                Coin.gold += 1
        for coin in self.coin_gun_topr:
            coin.move(edges)
            coin.draw(self.window)
            if coin.cought():
                self.coin_gun_topr.remove(coin)
                Coin.gold += 1
        for coin in self.coin_gun_botl:
            coin.move(edges)
            coin.draw(self.window)
            if coin.cought():
                self.coin_gun_botl.remove(coin)
                Coin.gold += 1
        for coin in self.coin_gun_botr:
            coin.move(edges)
            coin.draw(self.window)
            if coin.cought():
                self.coin_gun_botr.remove(coin)
                Coin.gold += 1
 
    def jabba_render(self, edges):
        for jabba in self.jabba_gun_topl:
            jabba.move(edges)
            jabba.draw(self.window)
        for jabba in self.jabba_gun_topr:
            jabba.move(edges)
            jabba.draw(self.window)
        for jabba in self.jabba_gun_botl:
            jabba.move(edges)
            jabba.draw(self.window)
        for jabba in self.jabba_gun_botr:
            jabba.move(edges)
            jabba.draw(self.window)
    
    def gameover(self):
        self.window.fill((145, 240, 160))
 
        game_text = self.game_font.render('Game over, gold collected: ' + str(Coin.gold), True, (255, 60, 100))
        start = self.game_font.render('Start new game: [F2]', True, (255, 60, 100))
        end = self.game_font.render('To exit press:  [ESC]', True, (255, 60, 100))
        self.window.blit(game_text, (self.width/2-182, self.height/2-100))
        self.window.blit(start, (self.width/2-140, self.height/2-50))
        self.window.blit(end, (self.width/2-140, self.height/2))
 
 
class Robot:
    def __init__(self, image, robx: int, roby: int, left: int, right: int, bottom: int):
        self.image = image
        self.left = left
        self.right = right
        self.bottom = bottom
 
        self.robx = robx
        self.roby = roby
        self.speed = 10
        self.move_left = False
        self.move_right = False
        self.jump = False
        self.falling = False
    
    def draw(self, window):
        window.blit(self.image, (self.robx, self.roby))
    
    def move(self, to_left: bool, to_right: bool):
        if self.falling == True:
            self.jump = False
 
        if to_left and self.robx > self.left:
            self.robx -= self.speed
        if to_right and self.robx < self.right:
            self.robx += self.speed
        
        if self.jump == True and self.roby > self.bottom-150:
            self.roby -= 10
            if to_left and self.robx > self.left:
                self.robx -= 3
            if to_right and self.robx < self.right:
                self.robx += 3
        if self.jump == False and self.roby < self.bottom:
            self.roby += 10
 
        if self.roby == self.bottom-150 or self.robx == self.left|self.right:
            self.falling = True
            self.jump = False
        if self.roby == self.bottom:
            self.falling = False
 
    def report(self):
        left_edge = self.robx-10
        right_edge = self.robx+self.image.get_width()+10
        top_edge = self.roby
        bot_edge = self.roby + self.image.get_height()
 
        return left_edge, right_edge, top_edge, bot_edge
 
class Coin:
    gold = 0
 
    def __init__(self, image: str, x: int, y: int, pos: int, borders: list):
        self.image = image
        self.left = borders[0]
        self.right = borders[1]
        self.bottom = borders[2]
        self.coin_pos = pos
 
        self.coin_x = x
        self.coin_y = y
        self.move_x = 6
        self.coin_falling_speed = 0
        self.coin_got = False      
        self.falling = False
 
    def draw(self, window):
        if not self.cought():
            window.blit(self.image, (self.coin_x, self.coin_y))
    
    def move(self, edges):
        if self.coin_pos in [0, 2]:
            self.coin_x += self.move_x
        if self.coin_pos in [1, 3]:
            self.coin_x -= self.move_x
 
        if self.coin_pos == 0 and self.coin_x >= 105:
            self.coin_falling_speed += 0.12
            self.move_x -= 0.04
            self.coin_y += self.coin_falling_speed
 
        if self.coin_pos == 1 and self.coin_x <= self.right-90:
            self.coin_falling_speed += 0.12
            self.move_x -= 0.04
            self.coin_y += self.coin_falling_speed
 
        if self.coin_pos == 2 and self.coin_x >= 35:
            self.coin_falling_speed += 0.12
            self.move_x -= 0.04
            self.coin_y += self.coin_falling_speed
 
        if self.coin_pos == 3 and self.coin_x <= self.right-20:
            self.coin_falling_speed += 0.12
            self.move_x -= 0.04
            self.coin_y += self.coin_falling_speed
           
        if self.coin_x > edges[0] and self.coin_x < edges[1] and self.coin_y > edges[2] - 30 and self.coin_y < edges[3]:
            self.coin_got = True
    
    def cought(self):
        if self.coin_got == True:
            return True
        else:
            return False
        
class Jabba:
    gameover = False
 
    def __init__(self, image: str, x: int, y: int, pos: int, left: int, right: int, bottom: int):
        self.image = image
        self.left = left
        self.right = right
        self.bottom = bottom
 
        self.j_x = x
        self.j_y = y
        self.j_move = 4
        self.j_falling_speed = 0
        self.j_pos = pos
        self.j_toright = False
        self.j_toleft = False
        self.j_got = False            
 
    def draw(self, window):
        window.blit(self.image, (self.j_x, self.j_y))
    
    def move(self, edges):
        rob_mid = (edges[0] + edges[1])/ 2
 
        if self.j_pos in [0, 2] and self.j_y < self.bottom:
            self.j_x += self.j_move
        if self.j_pos in [1, 3] and self.j_y < self.bottom:
            self.j_x -= self.j_move
 
        if self.j_pos == 0 and self.j_x >= 105 and self.j_y < self.bottom:
            self.j_falling_speed += 0.24
            self.j_x -= 0.07
            self.j_y += self.j_falling_speed
 
        if self.j_pos == 1 and self.j_x <= self.right-90 and self.j_y < self.bottom:
            self.j_falling_speed += 0.24
            self.j_x -= 0.07
            self.j_y += self.j_falling_speed
 
        if self.j_pos == 2 and self.j_x >= 35 and self.j_y < self.bottom:
            self.j_falling_speed += 0.16
            self.j_x -= 0.07
            self.j_y += self.j_falling_speed
 
        if self.j_pos == 3 and self.j_x <= self.right-20 and self.j_y < self.bottom:
            self.j_falling_speed += 0.16
            self.j_x -= 0.07
            self.j_y += self.j_falling_speed
        
        if self.j_y >= self.bottom and self.j_falling_speed > 0:
            self.j_falling_speed = 0
            if self.j_x < rob_mid:
                self.j_toright = True
            if self.j_x > rob_mid:
                self.j_toleft = True
        
        if self.j_toright:
            self.j_x += self.j_move
        if self.j_toleft:
            self.j_x -= self.j_move
 
        self.j_midx = self.j_x+self.image.get_width()/2
        self.j_midy = self.j_y+self.image.get_height()/2
                   
        if self.j_midx > edges[0] and self.j_midx < edges[1] and self.j_midy > edges[2]+5 and self.j_midy < edges[3]:
            Jabba.gameover = True
 
if __name__ == "__main__":
    Collector()