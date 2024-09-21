import random
import sys, math , os
import pygame as pg
pg.init()
icon = pg.image.load('icon.ico')
pg.display.set_icon(icon)
pg.mixer.init(44100,-16,2,512)
pg.mixer.music.load('music.mp3')
pg.mixer.music.play(-1)
pg.display.set_caption('Square')
jump = pg.mixer.Sound('jump.mp3')
landing = pg.mixer.Sound('landing.mp3')
screen_size = (1000, 750)
screen = pg.display.set_mode(screen_size)
clock = pg.time.Clock()
touch = False
movement_right = 4
movement_right_number = 0
gravity = 0
power = 0
hold_space = False
hold_key_up = False
hold_key_down = False
jumping = False
reset_timer = 0
set_block = False
set_first_block = True
reset = False
game_over = False
a = 0
score = 0
press_space_boolean = True
mini = 0
mini_2 = 0
high_score = 0
class Block(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global a, block_pos,mini
        self.image = pg.Surface((random.randint(50-1, 200-mini), 50))
        self.image.fill((random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)))
        self.rect = self.image.get_rect(center = block_pos[a])
        self.check_rect_top = pg.Rect(self.rect.x, self.rect.y, self.image.get_width(), 1)
        self.check_rect_bottom = pg.Rect(self.rect.x, self.rect.y + 50, self.image.get_width(), 1)
        self.check_rect_left = pg.Rect(self.rect.x, self.rect.y + 15, 1, 25)
        self.check_rect_right = pg.Rect(self.rect.x - self.image.get_width(), self.rect.y, 1, 50)
        self.check_rect_top_clone = pg.Rect(self.rect.x, self.rect.y-1, self.image.get_width(), 1)
    def update(self):
        global jumping, touch, player, gravity, power, movement_right, reset_timer, hold_space, a,set_block,set_first_block, block_group, score, landing

        if player.colliderect(self.check_rect_left):
            player.x = self.check_rect_left.x - 50
            movement_right = 0
        if player.y - (self.check_rect_top.y -50) >= 0 and player.bottom - self.check_rect_top.y >= 0:
            if player.x + 50 - self.check_rect_top.x >= 0 or player.x - self.check_rect_top.x + self.check_rect_top.width <= 0:
                if self.check_rect_top.colliderect(player):
                    player.y = self.check_rect_top.y - player.height
                    gravity = 0
                    jumping = False
        if self.check_rect_top_clone.colliderect(player):
            self.check_rect_top_clone.y = 2000
            set_block = True
            a += 1
            score += 1
            landing.play()
        if self.check_rect_bottom.colliderect(player):
            player.y = self.check_rect_bottom.y + 1
            gravity = 0.3
def Player_update():
    global jumping, touch, player, gravity, power,game_over
    if jumping:
        player.x += int(movement_right)
    if player.y >= respawn_block.y - player.y - 1:
        if player.x + 50 - respawn_block.x >= 0 or player.x - (respawn_block.x + 100) <= 0:
            if respawn_block.colliderect(player):
                player.y = respawn_block.y - player.height
                gravity = 0
                jumping = False

    if hold_space:
        power += 0.15
        if power >= 17:
            power = 17
    if hold_space == False:
        gravity += 0.3
        power = 0
    if player.y >= 700:
        jumping = False
        player.y = 700
        game_over = True
def Check_top(x):
    global screen
    arrow = pg.image.load('up-arrow.png')
    screen.blit(arrow,(x-10,0))

block_group = pg.sprite.Group()
respawn_block = pg.Rect(0, 500, 100, 45)
player = pg.Rect(20, 50, 50, 50)
power_font = pg.font.Font('8bit_font.ttf', 36)
moving_score = pg.font.Font('8bit_font.ttf',36)
gameover = pg.font.Font('8bit_font.ttf',100)
score_font = pg.font.Font('8bit_font.ttf',80)
high_score_font = pg.font.Font('8bit_font.ttf',32)
press_r = pg.font.Font('8bit_font.ttf',36)
press_space = pg.font.Font('8bit_font.ttf',36)
MVIT = pg.font.Font('8bit_font.ttf',30)

def Hc():
    global score, high_score,f
    f = open('high_score.txt')
    if int(score) > int(f.read()):
        f = open('high_score.txt','w')
        f.write(str(score))
        f = open('high_score.txt')


while True:
    f = open('high_score.txt')
    high_score = str(f.read())
    f.close()
    block_pos = [(random.randint(300, 350), random.randint(300, 600)),
                 (random.randint(500, 550), random.randint(300, 600)),
                 (random.randint(750, 960), random.randint(300, 600))]

    power_font_render = power_font.render('Power', hold_space, (0, 0, 0))
    moving_score_render = moving_score.render('Power: '+str(int(movement_right)),True,(0,0,0))
    gameover_render = gameover.render('GAME OVER!',True,(0,0,0))
    score_font_render = score_font.render('Score: '+str(score),True,(255,255,255))
    high_score_font_render = high_score_font.render('high score: ' + str(high_score), True, (255, 255, 255))
    press_r_render = press_r.render("Press 'R' to restart" ,True,(0,0,0))
    press_space_render = press_space.render("Press space to jump!!", True,(0,0,0))
    MVIT_render = MVIT.render('<-- Press UP and DOWN to set Power',True,(0,0,0))
    power_block = pg.Rect(360, 680, power * 15, 25)
    screen.fill((200, 200, 200))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and jumping == False and game_over ==False:
                press_space_boolean = False
                hold_space = True
                power = 0
            if event.key == pg.K_UP and game_over == False and jumping == False:
                hold_key_up = True
            if event.key == pg.K_DOWN and game_over == False and jumping == False:
                hold_key_down = True
            if event.key == pg.K_r:
                if game_over:
                    Hc()
                    game_over = False
                    respawn_block.x = 0
                    respawn_block.y = 500
                    respawn_block.width = 100
                    respawn_block.height = 45
                    block_group.empty()
                    a = 0
                    set_first_block = True
                    reset_timer = 0
                    player.x , player.y, player.width, player.height = 20, 50, 50, 50
                    gravity = 0
                    score = 0
                    movement_right = 4
                    mini = 0
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                hold_key_up = False
            if event.key == pg.K_DOWN:
                hold_key_down = False
            if event.key == pg.K_SPACE and hold_space and game_over == False:
                hold_space = False
                jumping = True
                touch = False
                gravity = -power
                jump.play()

#set block
    if a == 0 and set_first_block and reset_timer == 0:
        set_first_block = False
        block_1 = Block()
        block_group.add(block_1)
    if a == 1 and set_block:
        set_block = False
        block_2 = Block()
        block_group.add(block_2)
    if a == 2 and set_block:
        set_block = False
        block_3 = Block()
        block_group.add(block_3)

    if player.y + 50 < 0:
        Check_top(player.x)



    if hold_space:
        pg.draw.rect(screen, (230, 0, 0), power_block)
        screen.blit(power_font_render, (435, 630))
    screen.blit(moving_score_render,(0,10))
    if hold_key_down:
        movement_right -= 0.1
        if movement_right <= 0:
            movement_right = 0
    if hold_key_up:
        movement_right += 0.1

    player.y += gravity
    Player_update()
    reset_timer += 10
    #print(int(movement_right))
    pg.draw.rect(screen, (0, 0, 0), respawn_block)
    block_group.draw(screen)
    block_group.update()
    if a > 2:
        a = 0
        respawn_block.x , respawn_block.y = block_3.rect.x, block_3.rect.y
        respawn_block.width ,respawn_block.height = block_3.rect.width , block_3.rect.height
        block_group.empty()
        set_first_block = True
        reset = True
# reset time
    reset_timer += 1
    if reset:
        if respawn_block.x > 0 or player.x > 20:
            respawn_block.x -= respawn_block.x/80
            player.x -= player.x/80
        else:
            reset = False
            reset_timer = 0
            if mini <150:
                mini += 10
            if mini_2 <41 and mini >= 150:
                mini_2 += 1

    if game_over:
        screen.blit(gameover_render,(300,340))
        screen.blit(press_r_render,(370,400))
    if press_space_boolean:
        screen.blit(MVIT_render,(250,10))
        screen.blit(press_space_render,(370,700))
    screen.blit(score_font_render,(380,140))
    screen.blit(high_score_font_render,(420,190))
    pg.draw.rect(screen, (0, 200, 0), player)
    pg.display.flip()
    clock.tick(1000)
