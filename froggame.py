import pygame
import sys
import imageio

# 초기화
pygame.init()

#화면 타이틀 설정
pygame.display.set_caption("Frog Game") 

# 화면 크기 설정
screen_width, screen_height = 1000, 680
screen = pygame.display.set_mode((screen_width, screen_height))

# 시계 설정
clock = pygame.time.Clock()

# 중력 설정
gravity = 1

#배경 설정
background_image = pygame.image.load("resource\sky1.png")

# 재시작 버튼 설정
button_font = pygame.font.Font('resource\Maplestory Bold.ttf', 36)
button_text = button_font.render("Restart", True, (0, 0,0))
button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

# 배경음악 파일 로드
pygame.mixer.init()
pygame.mixer.music.load('resource\\bgm.mp3')
pygame.mixer.music.set_volume(0.04)

# 배경음악 재생
pygame.mixer.music.play()

# 효과음 로드
class SoundEffect():
    jump_effect_sound = pygame.mixer.Sound('resource\jumpsound.mp3') 
    jump_effect_sound.set_volume(0.1)
    obstacle_effect_sound = pygame.mixer.Sound('resource\hitsound.mp3')
    obstacle_effect_sound.set_volume(0.1)
    obstacle_effect_sound_count = 0

# 물체 설정
class Player():
    def __init__(self):
        self.imagejump = pygame.image.load("resource\playerjump.png")
        self.imagedefault = pygame.image.load("resource\playerdefault.png")
        self.width, self.height = self.imagedefault.get_width(), self.imagedefault.get_height()
        self.x, self.y = screen_width // 2 - self.width // 2, 300
        self.yvelocity = 0
        self.xvelocity = 0
        #사망 여부
        self.on_death = False
        # 물체가 바닥에 닿았는지 여부 확인 변수
        self.on_ground = False
        #물체가 장애물과 닿았는지 여부 확인 변수
        self.on_obstacle = False
        # 점프를 하는 중인지를 확인하는 변수
        self.keydown = False


# 바닥 설정
class Ground():
    def __init__(self):
        self.image = pygame.image.load("resource\\fullground.png")
        self.image2 = pygame.image.load("resource\soil.png")
        self.image3 = pygame.image.load("resource\soil2.png")
        self.airimage = pygame.image.load("resource\\skyblockground.png")
        self.grounds = []
        self.airgrounds = []

# 장애물 설정
class Obstacles() : 
    def __init__(self):
        self.color = (120,0,205)
        self.obstacles = []

class DeathGround():
    def __init__(self):
        self.image = pygame.image.load("resource\\deathground.png")
        self.deaths = []

# 플레이어 세팅
player1 = Player()

# 게이지 바
class EnergyBar():
    def __init__(self):
        self.image1 = pygame.image.load("resource\\1.png")
        self.image2 = pygame.image.load("resource\\2.png")
        self.image3 = pygame.image.load("resource\\3.png")
        self.image4 = pygame.image.load("resource\\4.png")
        self.image5 = pygame.image.load("resource\\5.png")
        self.image6 = pygame.image.load("resource\\6.png")
        self.image7 = pygame.image.load("resource\\7.png")
        self.image8 = pygame.image.load("resource\8.png")
        self.image9 = pygame.image.load("resource\9.png")

# 여러 개의 바닥 설정
ground1 = Ground()

ground1.grounds = [{'x': -50, 'y': 550, 'width': 1150, 'height': 134},
            {'x': 1200, 'y': 500, 'width': 1150, 'height': 134},
            {'x': 2400, 'y': 550, 'width': 1150, 'height': 134},
            {'x': 3600, 'y': 550, 'width': 1150, 'height': 134},
            {'x': 4750, 'y': 560, 'width': 1150, 'height': 134},
            {'x': 5150, 'y': 560, 'width': 1150, 'height': 134},
            {'x': 6300, 'y': 760, 'width': 1150, 'height': 134},
            {'x': 7800, 'y': 760, 'width': 1150, 'height': 134},            
]
ground1.airgrounds = [
        [{'x': 5000 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 5300 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 5600 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 5900 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 6200 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 7550 + a*50 , 'y': 760, 'width': 50, 'height': 80}for a in range(4)],
        [{'x': 9100 + a*50 , 'y': 675, 'width': 50, 'height': 80}for a in range(7)],
        
] 

# 여러 개의 장애물 설정
obstacle1 = Obstacles()

obstacle1.obstacles = [
    {'x': 1200, 'y': 485, 'width': 300, 'height': 15},
    {'x': 2000, 'y': 485, 'width': 300, 'height': 15},
    {'x': 3000, 'y': 535, 'width': 300, 'height': 15},
    {'x': 3900, 'y': 549, 'width': 100, 'height': 15},
    {'x': 4150, 'y': 549, 'width': 100, 'height': 15},
    {'x': 4400, 'y': 549, 'width': 100, 'height': 15},
    {'x': 4750, 'y': 540, 'width': 1550, 'height': 20},
    {'x': 5100, 'y': 461, 'width': 200, 'height': 100},
    {'x': 5400, 'y': 461, 'width': 200, 'height': 100},
    {'x': 5700, 'y': 461, 'width': 200, 'height': 100},
    {'x': 6000, 'y': 461, 'width': 200, 'height': 100},
    {'x': 5330, 'y': -730, 'width': 40, 'height': 1000},
    {'x': 5630, 'y': -730, 'width': 40, 'height': 1000},
    {'x': 5930, 'y': -730, 'width': 40, 'height': 1000},
    {'x': 6230, 'y': -730, 'width': 40, 'height': 1000}, 
    {'x': 8230, 'y': -730, 'width': 350, 'height':15},
    
    #{'x': 0, 'y': 700, 'width' : 100000, 'height' : 100} 
]

# 죽음 발판 설정
deathGround = DeathGround()

deathGround.deaths = [
    {'x' : a*3000, 'y' : 1000, 'width' : 3000, 'height': 500} for a in range(100)
    
]

# 결승 지점 설정
on_finish = False
finish = [{'x' : 9600, 'y' : 0, 'width' : 1000, 'height' : 680}]

# 화살표 설정
arrow_color = (0, 0, 255)  # 파란색
arrow_head_x1 = 600
arrow_head_x2 = 600
arrow_head_x3 = 620
arrow_head_y = (20,60,40)
arrow_body_color = (0,0,255)
arrow_body_width = 100
arrow_body_height = 2
arrow_body_x = 500
arrow_body_y = 30

# 게이지 바 설정
energybar = EnergyBar()

#텍스트 위치 설정
text_x = screen_width // 2

# 글꼴 설정
font = pygame.font.Font('resource\Maplestory Bold.ttf', 36)

# 텍스트 렌더링
text = font.render("Press Space Bar for charging force to jump!", True, (0,0,0))  # 텍스트, 안티앨리어싱 사용 여부, 글자색
text_rect = text.get_rect(center=(text_x, 180))  # 화면 중앙에 위치
istext = True


#소리 효과 설정
soundeffect = SoundEffect()




# 스페이스바 누른 순간의 시간
jump_start_time = 0
jump_end_time = 0
energy = 0
chargedEnergy = 0

# gif 넣기
'''gif_frames = imageio.get_reader("sky1.gif")
frame = 0
a = 0'''



# 글꼴 설정
font1 = pygame.font.Font('resource\Maplestory Bold.ttf', 60) 

# 클리어 텍스트 렌더링
text1 = font1.render("Clear!!!", True, (0,0,0))  # 텍스트, 안티앨리어싱 사용 여부, 글자색
text_rect1 = text1.get_rect(center=(screen_width // 2, 250))  # 화면 중앙에 위치

# 게임 시작 전 화면 ----------------------------------------------------------------------------------------------------------

#게임 시작 버튼 및 텍스트
prebutton_font = pygame.font.Font('resource\Maplestory Bold.ttf', 60)
prebutton_text = prebutton_font.render("Play", True, (0,0,0))
prebutton_rect = prebutton_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

# 시작 전 화면 배경
preimage = pygame.image.load('resource\preback.png')



main = False

while True:
    #조건 설정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                main = True
                

    screen.blit(preimage,(0,0))

    # 화면에 텍스트 표시
    if(main==False):
        pretext = font1.render("JumFrog", True, (0,0,0))
        pretext_rect = pretext.get_rect(center=(screen_width // 2, 200))
        screen.blit(pretext, pretext_rect)
    
    # 재시작 버튼 표시
    pygame.draw.rect(screen, (255, 255, 255), prebutton_rect)
    screen.blit(prebutton_text, prebutton_rect.topleft)

    pygame.display.flip()  # 화면 업데이트

    # 프레임 설정
    clock.tick(60)
    if(main):
        break

    



# 게임 메인 루프---------------------------------------
while True:
    
    if(player1.on_death): #죽은 상태이면
        # 마우스 클릭 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and player1.on_death:
                if button_rect.collidepoint(event.pos):
                    
                    player1.on_death = False
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        # 게임 종료 화면에 텍스트 표시
        text = font.render("Game Over", True, (0,0,0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

        # 재시작 버튼 표시
        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        screen.blit(button_text, button_rect.topleft)

        pygame.display.flip()  # 화면 업데이트
        obstacle1.obstacles = [
    {'x': 1200, 'y': 485, 'width': 300, 'height': 15},
    {'x': 2000, 'y': 485, 'width': 300, 'height': 15},
    {'x': 3000, 'y': 535, 'width': 300, 'height': 15},
    {'x': 3900, 'y': 549, 'width': 100, 'height': 15},
    {'x': 4150, 'y': 549, 'width': 100, 'height': 15},
    {'x': 4400, 'y': 549, 'width': 100, 'height': 15},
    {'x': 4750, 'y': 540, 'width': 1550, 'height': 20},
    {'x': 5100, 'y': 461, 'width': 200, 'height': 100},
    {'x': 5400, 'y': 461, 'width': 200, 'height': 100},
    {'x': 5700, 'y': 461, 'width': 200, 'height': 100},
    {'x': 6000, 'y': 461, 'width': 200, 'height': 100},
    {'x': 5330, 'y': -730, 'width': 40, 'height': 1000},
    {'x': 5630, 'y': -730, 'width': 40, 'height': 1000},
    {'x': 5930, 'y': -730, 'width': 40, 'height': 1000},
    {'x': 6230, 'y': -730, 'width': 40, 'height': 1000}, 
    {'x': 8230, 'y': -730, 'width': 350, 'height':15},]
        
        ground1.grounds = [{'x': -50, 'y': 550, 'width': 1150, 'height': 134},
            {'x': 1200, 'y': 500, 'width': 1150, 'height': 134},
            {'x': 2400, 'y': 550, 'width': 1150, 'height': 134},
            {'x': 3600, 'y': 550, 'width': 1150, 'height': 134},
            {'x': 4750, 'y': 560, 'width': 1150, 'height': 134},
            {'x': 5150, 'y': 560, 'width': 1150, 'height': 134},
            {'x': 6300, 'y': 760, 'width': 1150, 'height': 134},
            {'x': 7800, 'y': 760, 'width': 1150, 'height': 134},            
]
        ground1.airgrounds = [
        [{'x': 5000 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 5300 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 5600 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 5900 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 6200 + a*50 , 'y': 460, 'width': 50, 'height': 80}for a in range(2)],
        [{'x': 7550 + a*50 , 'y': 760, 'width': 50, 'height': 80}for a in range(4)],
        [{'x': 9100 + a*50 , 'y': 675, 'width': 50, 'height': 80}for a in range(7)],]

        deathGround.deaths = [
    {'x' : a*3000, 'y' : 1000, 'width' : 3000, 'height': 500} for a in range(100)
    
]
        # 화살표 설정
        arrow_color = (0, 0, 255)  # 파란색
        arrow_head_x1 = 600
        arrow_head_x2 = 600
        arrow_head_x3 = 620
        arrow_head_y = (20,60,40)
        arrow_body_color = (0,0,255)
        arrow_body_width = 100
        arrow_body_height = 2
        arrow_body_x = 500
        arrow_body_y = 30

        # 결승 지점 설정
        on_finish = False
        finish = [{'x' : 9600, 'y' : 0, 'width' : 1000, 'height' : 680}]
        

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
            # 스페이스바 충전 시작
                if event.key == pygame.K_SPACE:
                
                    jump_start_time = pygame.time.get_ticks()
                    player1.keydown = True
                    energy = pygame.time.get_ticks()
                
            if player1.keydown:
                chargedEnergy = pygame.time.get_ticks() - energy

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                # 스페이스바를 떼는 순간의 시간
                jump_end_time = pygame.time.get_ticks()
                player1.keydown = False
                energy = 0
                chargedEnergy = 0
            
                # 바닥에 닿아 있을 때만 점프 처리
                if player1.on_ground:
                # 스페이스바를 누른 시간에 따라 점프 강도를 결정
                    jump_duration = jump_end_time - jump_start_time
                
                    player1.xvelocity = (jump_duration+300) /100   # 점프 강도 조정
                    if jump_duration <300:
                        player1.xvelocity = 6  #일정 시간 미만이면 특정 속도로 움직이도록 하여 편법 방지
                    elif jump_duration > 1200:
                        player1.xvelocity = 15
                        istext = False
                    else:
                        istext = False

                    player1.yvelocity = -(jump_duration+300) / 75  # 점프 강도 조정
                
                    if jump_duration <300:
                        player1.yvelocity = -8
                    elif jump_duration >1200:
                        player1.yvelocity = -20
                    soundeffect.jump_effect_sound.play()
                    
        # 중력에 따른 가속도 적용
        player1.yvelocity += gravity

        # 물체의 위치 업데이트
        player1.y += player1.yvelocity
        player1.x += player1.xvelocity

        # 물체가 바닥에 닿으면 멈추기
        player1.on_ground = False
        for ground in ground1.grounds:
            if player1.y + player1.height >= ground['y'] and player1.y <= ground['y'] + ground['height']:    #rect가 겹치는 조건 이용
                if player1.x + player1.width >= ground['x'] and player1.x <= ground['x'] + ground['width']:
                    player1.y = ground['y'] - player1.height
                    player1.xvelocity = 0  # 물체가 바닥에 닿으면 속도 초기화
                    player1.yvelocity = 0
                    player1.on_ground = True  # 바닥에 닿았음을 표시
                    break
    
        # 공중 발판 관련
        for ground2 in ground1.airgrounds:
            for ground in ground2:
                if player1.y + player1.height >= ground['y'] and player1.y <= ground['y'] + ground['height']:    #rect가 겹치는 조건 이용
                    if player1.x + player1.width >= ground['x'] and player1.x <= ground['x'] + ground['width']:
                        player1.y = ground['y'] - player1.height
                        player1.xvelocity = 0  # 물체가 바닥에 닿으면 속도 초기화
                        player1.yvelocity = 0
                        player1.on_ground = True  # 바닥에 닿았음을 표시
                        break
    
        #물체가 장애물과 닿으면 뒤로 밀어내기
        player1.on_obstacle = False
        for obstacle in obstacle1.obstacles:
            if player1.y + player1.height >= obstacle['y'] and player1.y <= obstacle['y'] + obstacle['height']: #rect가 겹치는 조건 이용
                if player1.x + player1.width >= obstacle['x'] and player1.x <= obstacle['x'] + obstacle['width']:
                
                    player1.xvelocity = -15 # 물체가 장애물에 닿으면 속도 초기화
                    player1.yvelocity = -10
                    player1.on_obstacle = True  # 장애물에 닿았음을 표시
                    soundeffect.obstacle_effect_sound.play()
                    break

        #물체가 밑으로 떨어지면 사망
        player1.on_death = False
        for obstacle in deathGround.deaths:
            if player1.y + player1.height >= obstacle['y'] and player1.y <= obstacle['y'] + obstacle['height']: #rect가 겹치는 조건 이용
                if player1.x + player1.width >= obstacle['x'] and player1.x <= obstacle['x'] + obstacle['width']:
                    player1.on_death = True

        #결승선 통과
        for obstacle in finish:
            #rect가 겹치는 조건 이용, 애초에 y값은 절대적으로 설정할 예정이라 무조건 통과함. 굳이 조건 안해줌.
            if player1.x + player1.width >= obstacle['x'] and player1.x <= obstacle['x'] + obstacle['width']:
                on_finish = True
                gravity = 0
                player1.xvelocity =0
                player1.yvelocity = 0

        # 물체가 600에 오면 화면을 위로 스크롤
        if player1.y > 600 :    #object가 가는게 아니라 맵이 움직임.
            player1.y = 600
            for ground in ground1.grounds:
                ground['y'] -= player1.yvelocity  # 바닥도 같이 이동
            for ground2 in ground1.airgrounds:
                for ground in ground2:
                    ground['y'] -= player1.yvelocity
            for obstacle in obstacle1.obstacles:
                obstacle['y'] -= player1.yvelocity
            for obstacle in deathGround.deaths:
                obstacle['y'] -= player1.yvelocity  

        # 물체가 250에 오면 화면을 고정
        if player1.x > 250 or player1.x <250:
            player1.x = 250
            for ground in ground1.grounds:  #object가 가는게 아니라 맵이 움직임.
                ground['x'] -= player1.xvelocity
            for ground2 in ground1.airgrounds:
                for ground in ground2: 
                    ground['x'] -= player1.xvelocity
            for obstacle in obstacle1.obstacles:
                obstacle['x'] -= player1.xvelocity
            for obstacle in deathGround.deaths:
                obstacle['x'] -= player1.xvelocity
            for finish1 in finish:
                finish1['x'] -= player1.xvelocity # 결승선은 y값 안바꾸고 x만 바꿔주기
            arrow_body_x -= player1.xvelocity
            arrow_head_x1 -= player1.xvelocity
            arrow_head_x2 -= player1.xvelocity
            arrow_head_x3 -= player1.xvelocity

 
        #물체는 250에서 움직일 뿐, 맵이 움직이는 것
        
        screen.fill((255, 255, 255))  # 화면을 흰색으로 지우기
        screen.blit(background_image,(0,-120)) # 배경 그리기

        if(player1.on_ground):
            screen.blit(player1.imagedefault, (player1.x, player1.y)) # 이미지 그리기
        else:
            screen.blit(player1.imagejump, (player1.x, player1.y)) # 이미지 그리기


        # 바닥 그리기
        for ground in ground1.grounds:
            screen.blit(ground1.image,(ground['x'],ground['y']))
            screen.blit(ground1.image2,(ground['x'],ground['y']+130))
            screen.blit(ground1.image3,(ground['x'],ground['y']+164))
    
        for ground2 in ground1.airgrounds:
            for ground in ground2:
                screen.blit(ground1.airimage,(ground['x'],ground['y']))
        
        # 죽는 발판 그리기
        for death in deathGround.deaths:
            screen.blit(deathGround.image,(death['x'],death['y']))


        #장애물 그리기
    
        for obstacle in obstacle1.obstacles:
            pygame.draw.rect(screen, obstacle1.color, (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))

        # 텍스트 표시
        if(istext):
            screen.blit(text, text_rect)

        if on_finish:
            screen.blit(text1, text_rect1)

        # 게이지 바 그리기
        if chargedEnergy<300:
            screen.blit(energybar.image1, (300,640))
        elif chargedEnergy<428:
            screen.blit(energybar.image2, (300,640))
        elif chargedEnergy<557:
            screen.blit(energybar.image3, (300,640))
        elif chargedEnergy<685:
           screen.blit(energybar.image4, (300,640))
        elif chargedEnergy<814:
            screen.blit(energybar.image5, (300,640))
        elif chargedEnergy<932:
            screen.blit(energybar.image6, (300,640))
        elif chargedEnergy<1061:
            screen.blit(energybar.image7, (300,640))
        elif chargedEnergy < 1200:
            screen.blit(energybar.image8, (300,640))
        else:
            screen.blit(energybar.image9, (300,640))
    
        #방향 알려주는 화살표 그리기
        pygame.draw.polygon(screen, arrow_color, [(arrow_head_x1,arrow_head_y[0]),(arrow_head_x2,arrow_head_y[1]),(arrow_head_x3,arrow_head_y[2])])
        pygame.draw.rect(screen,arrow_body_color,(arrow_body_x,arrow_body_y,arrow_body_width,20))



        pygame.display.flip()  # 화면 업데이트

        # 프레임 설정
        clock.tick(60)
