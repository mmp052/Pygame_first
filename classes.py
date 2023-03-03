import pygame
class State:
    def __init__(self,conteudo):
        self.record = int(conteudo)
        self.tempo_frequencia =  0
        self.tempo_acelera = 0
        self.tempo_total = 0
        self.ultimo_tempo = 0
        self.tempo_atualizar = 0
        self.tiros = []
        self.tiro_vel = 300
        self.tiros_fora_tela = 0
        # self.player_pos_x = 270
        # self.player_pos_y = 380

class Assets:
    def __init__(self):
        self.fundo = pygame.image.load('fundo.jpg')
        self.blaster = pygame.mixer.Sound('som_blaster.mp3')
        self.som_fundo = pygame.mixer.Sound('som_fundo.mp3')

class Tiro:
    def __init__(self, pos_x, pos_y, width, height, vel, imagem, window):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.vel = vel
        self.imagem = imagem
        self.window = window

    def atualiza_posicao(self,dt):
        self.pos_y+= self.vel * dt
    
    def desenha(self):
        self.window.blit(self.imagem, (self.pos_x, self.pos_y))

    def colisao_rect(self, obj):
        colisao = False
        if (obj.pos_x <= self.pos_x + self.width <= obj.pos_x + obj.width or self.pos_x <= obj.pos_x + obj.width <= self.pos_x + self.width) and (obj.pos_y <= self.pos_y + self.height <= obj.pos_y + obj.height or self.pos_y <= obj.pos_y + obj.height <= self.pos_y + self.height):
            colisao = True
        return colisao
    
    def saiu_tela(self):
        return self.pos_y > 480

    def apaga_tiro(self, state):
        del state.tiros[0]

    def aumenta_vel(self,state):
        state.tiro_vel+=100

class Jogador:
    def __init__(self, pos_x, pos_y, width, height, imagem, window, vira = False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.imagem = imagem
        self.window = window
        self.vira = vira
        self.keys = {'right':False, 'up':False, 'left':False, 'down':False}
        self.vel_x = 0
        self.vel_y = 0

    def move(self,evento):
        #print(evento)
        if evento.key == pygame.K_d:
            self.keys['right'] = True
            self.vira = 'direita'
            self.vel_x+=1
        if evento.key == pygame.K_w:
            self.keys['up'] = True
            self.vel_y-=1
        if evento.key == pygame.K_s:
            self.keys['down'] = True
            self.vel_y+=1
        if evento.key == pygame.K_a:
            self.keys['left'] = True
            self.vira = 'esquerda'
            self.vel_x-=1

        if self.keys['right']:
            if self.pos_x < 540:
                self.pos_x+=self.vel_x
        if self.keys['up']:
            if self.pos_y > 0:
                self.pos_y+=self.vel_y
        if self.keys['down']:
            if self.pos_y < 480 - self.height:
                self.pos_y+=self.vel_y
        if self.keys['left']:
            if self.pos_x > 0:
                self.pos_x+=self.vel_x
        
        
    
    def nao_muda(self,evento):
        if evento.key == pygame.K_d:
            self.keys['right'] = False
            self.vira = False
            self.vel_x = 0
        if evento.key == pygame.K_w:
            self.keys['up'] = False
            self.vel_y = 0
        if evento.key == pygame.K_s:
            self.keys['down'] = False
            self.vel_y = 0
        if evento.key == pygame.K_a:
            self.keys['left'] = False
            self.vira = False
            self.vel_x = 0

    def desenha(self):
        if self.vira == 'esquerda':
            self.window.blit(pygame.transform.rotate(self.imagem, 30), (self.pos_x, self.pos_y))
        elif self.vira == 'direita':
            self.window.blit(pygame.transform.rotate(self.imagem, -30), (self.pos_x, self.pos_y))
        else:
            self.window.blit(self.imagem, (self.pos_x, self.pos_y))
