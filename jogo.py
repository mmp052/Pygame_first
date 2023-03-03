import pygame
from classes import *

with open('record.txt', 'r') as arquivo:
    conteudo = arquivo.read()

def inicializa():
    pygame.init()
    pygame.key.set_repeat(20)
    w = pygame.display.set_mode((640,480))
    player = Jogador(270, 380, 60, 70, pygame.image.load('nave2.png'),w)
    state = State(conteudo)
    assets = Assets()

    return w, assets, state, player

def atualiza_estado(state, player):
    finaliza = False
    tempo = pygame.time.get_ticks()

    delta_tempo = tempo - state.tempo_acelera
    state.tempo_total = tempo

    delta_t = tempo - state.ultimo_tempo
    delta_t_atualizar = (tempo - state.tempo_atualizar) /1000
    delta_t_frequencia = tempo - state.tempo_frequencia
    
    if delta_t >= 600:
        state.tiros.append(Tiro(player.pos_x, 0, 10, 48, state.tiro_vel, pygame.image.load('tiro.png'),w)) # fazer isso na função atualiza tiros.
        state.ultimo_tempo = tempo
    for tiro in state.tiros:
        tiro.atualiza_posicao(delta_t_atualizar)
        if tiro.saiu_tela():
            tiro.apaga_tiro(state)
        if delta_tempo >= 15000:
            state.tempo_acelera = tempo
            tiro.aumenta_vel(state)
        if tiro.colisao_rect(player):
            if state.tempo_total/1000 > state.record:
                state.record = int(state.tempo_total/1000)
                record = state.record
                with open('record.txt', 'w') as arquivo:
                    arquivo.write(f'{record}')
                print(f'Parabéns, seu novo record é de {record} segundos')
            else:
                record = state.record
                print(f'O record continua sendo de {record} segundos')
            finaliza = True
            break
    if finaliza:
        return False
    state.tempo_atualizar = tempo

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        elif evento.type == pygame.KEYDOWN:
            player.move(evento)
        elif evento.type == pygame.KEYUP:
            player.nao_muda(evento)
    return True
        
def desenha(w: pygame.surface, assets, state, player):
    w.blit(assets.fundo, (0,0))
    player.desenha()
    for tiro in state.tiros:
        assets.blaster.play(0,600)
        tiro.desenha()
    pygame.display.update()

def gameloop(w, assets, state, player):
    assets.som_fundo.set_volume(1)
    assets.blaster.set_volume(0.3)
    assets.som_fundo.play(-1)
    while atualiza_estado(state, player):
        desenha(w, assets, state, player)

def finaliza():
    pygame.quit()

if __name__ == '__main__':
    w, assets, state, player = inicializa()
    gameloop(w, assets, state, player)
    finaliza()