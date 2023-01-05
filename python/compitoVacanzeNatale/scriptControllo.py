import math
import os
import pygame
import numpy as np
import sys
from pygame.locals import *
from random import randint

WIDTH = 1577
HEIGHT = 682
TITLE = 'Basketball 3 v 3'
FPS = 60

SIZE_BALL = (40, 40)
COORD_CANESTRO_1 = (250, 105)
COORD_CANESTRO_2 = (WIDTH - 250 - SIZE_BALL[0], 95)  # y : 202, z: HEIGHT - 307
FERRO_1_CANESTRO_2 = (COORD_CANESTRO_2[0] - 25, COORD_CANESTRO_2[1])
FERRO_2_CANESTRO_2 = (COORD_CANESTRO_2[0] + 25, COORD_CANESTRO_2[1])
Y_RIM_FERRO = 75 + SIZE_BALL[1]

X_CAMPO = 1433
Y_CAMPO = 245
Y_BORDO_2_CAMPO = 47
LINEA_3_CAN_2 = ({'x': 1205, 'y': 274.5}, {'x': 1010, 'y': 259.5}, {'x': 980, 'y': 244.5}, {'x': 965, 'y': 229.5},
                 {'x': 965, 'y': 214.5}, {'x': 965, 'y': 199.5}, {'x': 965, 'y': 184.5}, {'x': 980, 'y': 169.5},
                 {'x': 995, 'y': 154.5}, {'x': 1010, 'y': 139.5}, {'x': 1025, 'y': 124.5}, {'x': 1055, 'y': 109.5},
                 {'x': 1085, 'y': 94.5}, {'x': 1130, 'y': 79.5})  # 'x' da sx a dx, facendo -60 si trovano con verso sx


class WindowInitial:
    def __init__(self):
        self.imgSfondo = pygame.image.load('images/campoSchermataIniz.png')
        self.display = pygame.display.set_mode(self.imgSfondo.get_size())
        self.inSchermataIniz = True
        pygame.display.set_caption(TITLE)

        self.fontInput = pygame.font.Font(None, 40)
        self.col_act = pygame.Color('gold')
        self.col_inact = pygame.Color('white')
        self.inpName_1 = {'box': pygame.Rect(300, 100, 140, 40), 'color': self.col_inact, 'active': False, 'text': 'nome team 1'}
        self.inpName_2 = {'box': pygame.Rect(WIDTH - 300, 100, 140, 40), 'color': self.col_inact, 'active': False, 'text': 'nome team 2'}

        self.fontNamePlayers = pygame.font.Font(None, 30)
        self.colName = pygame.Color('black')

        self.listPlayers = []
        self.indGiocUsciti = []
        self.paths = os.listdir('images/players/faces')
        while len(self.listPlayers) < 6:
            n = randint(0, len(self.paths) - 1)
            if n in self.indGiocUsciti:
                continue

            self.indGiocUsciti.append(n)
            self.listPlayers.append({'path': self.paths[n],
                                     'freccia su': pygame.image.load('images/frecciaSceltaGiocSu.png'),
                                     'freccia giu': pygame.image.load('images/frecciaSceltaGiocGiu.png'),
                                     'name': self.fontNamePlayers.render(self.paths[n][:self.paths[n].index('_')].capitalize(), True, self.colName),
                                     'surname': self.fontNamePlayers.render(self.paths[n][self.paths[n].index('_') + 1: -4].capitalize(), True, self.colName),
                                     'index': n})

    def __printPlayer(self, i, g):
        imgTesta = pygame.image.load('images/players/faces/' + g['path'])
        imgCorpo = pygame.image.load('images/players/maglia_1.png') if i < 3 else pygame.image.load('images/players/maglia_2.png')
        imgScarpe = pygame.image.load('images/players/shoes.png')
        x = 200 + i * (imgTesta.get_width() + 100) if i < 3 else WIDTH - 200 - (2 - i % 3) * (imgTesta.get_width() + 100)

        self.display.blit(imgScarpe, (x + 20, 460))
        self.display.blit(imgCorpo, (x + 20, 450 - imgScarpe.get_height()))
        self.display.blit(imgTesta, (x, 460 - imgScarpe.get_height() - imgTesta.get_height()))
        self.display.blit(g['freccia su'], (x + imgTesta.get_width() / 2 - g['freccia su'].get_width() / 2, 320 - imgScarpe.get_height() - g['freccia su'].get_height()))
        self.display.blit(g['freccia giu'], (x + imgTesta.get_width() / 2 - g['freccia giu'].get_width() / 2, 570))
        self.display.blit(g['name'], (x + imgTesta.get_width() / 2 - g['name'].get_width() / 2, 510))
        self.display.blit(g['surname'], (x + imgTesta.get_width() / 2 - g['surname'].get_width() / 2, 540))

    def __indexEff(self, n):
        if n < -len(self.paths):
            return self.__indexEff(n + len(self.paths))
        elif n < 0:
            return len(self.paths) + n
        elif n >= len(self.paths):
            return self.__indexEff(n - len(self.paths))
        return n

    def __cambioGioc(self, n, g, i):
        g['index'], g['path'], self.indGiocUsciti[i] = n, self.paths[n], n
        g['name'] = self.fontNamePlayers.render(g['path'][:g['path'].index('_')].capitalize(), True, self.colName)
        g['surname'] = self.fontNamePlayers.render(g['path'][g['path'].index('_') + 1: -4].capitalize(), True, self.colName)

    def checkEvt(self, e):
        if e.type == MOUSEBUTTONDOWN:
            if self.inpName_1['box'].collidepoint(e.pos):
                self.inpName_1['active'] = not self.inpName_1['active']
                self.inpName_2['active'] = False
            elif self.inpName_2['box'].collidepoint(e.pos):
                self.inpName_2['active'] = not self.inpName_2['active']
                self.inpName_1['active'] = False
            else:
                self.inpName_1['active'] = False
                self.inpName_2['active'] = False

            self.inpName_1['color'] = self.col_act if self.inpName_1['active'] else self.col_inact
            self.inpName_2['color'] = self.col_act if self.inpName_2['active'] else self.col_inact

            for i, g in enumerate(self.listPlayers):
                pos = pygame.mouse.get_pos()
                head = pygame.image.load('images/players/faces/' + g['path'])
                x = 200 + i * (head.get_width() + 100) if i < 3 else WIDTH - 200 - (2 - i % 3) * (head.get_width() + 100)
                x += head.get_width() / 2 - g['freccia su'].get_width() / 2
                y = 320 - pygame.image.load('images/players/shoes.png').get_height() - g['freccia su'].get_height()

                if x <= pos[0] <= x + g['freccia su'].get_width() and y <= pos[1] <= y + g['freccia su'].get_height():
                    while self.__indexEff(g['index']) in self.indGiocUsciti:
                        g['index'] -= 1
                    self.__cambioGioc(self.__indexEff(g['index']), g, i)
                    break
                # non serve ri-assegnare la x perchè le dim delle freccie sono uguali
                elif x <= pos[0] <= x + g['freccia giu'].get_width() and 570 <= pos[1] <= 570 + g['freccia giu'].get_height():
                    while self.__indexEff(g['index']) in self.indGiocUsciti:
                        g['index'] += 1
                    self.__cambioGioc(self.__indexEff(g['index']), g, i)
                    break

        if e.type == KEYDOWN and self.inpName_1['active']:
            if e.key == K_BACKSPACE:
                self.inpName_1['text'] = self.inpName_1['text'][:-1]
            else:
                self.inpName_1['text'] += e.unicode
        elif e.type == KEYDOWN and self.inpName_2['active']:
            if e.key == K_BACKSPACE:
                self.inpName_2['text'] = self.inpName_2['text'][:-1]
            else:
                self.inpName_2['text'] += e.unicode
        elif e.type == KEYDOWN and e.key == K_RETURN:
            self.inSchermataIniz = False

    def updateWindow(self):
        self.display.blit(self.imgSfondo, (0, 0))
        txt_sur_1 = self.fontInput.render(self.inpName_1['text'], True, self.inpName_1['color'])
        txt_sur_2 = self.fontInput.render(self.inpName_2['text'], True, self.inpName_2['color'])
        self.inpName_2['box'] = pygame.Rect(WIDTH - 300 - txt_sur_2.get_width(), 100, 140, 40)
        self.inpName_1['box'].w = max(200, txt_sur_1.get_width() + 10)
        self.inpName_2['box'].w = max(200, txt_sur_2.get_width() + 10)
        self.display.blit(txt_sur_1, (self.inpName_1['box'].x + 5, self.inpName_1['box'].y + 5))
        self.display.blit(txt_sur_2, (self.inpName_2['box'].x + 5, self.inpName_2['box'].y + 5))

        if self.inpName_1['text'].strip() == '' and not self.inpName_1['active']:
            self.inpName_1['text'] = 'nome team 1'
        if self.inpName_2['text'].strip() == '' and not self.inpName_2['active']:
            self.inpName_2['text'] = 'nome team 2'
        for i, g in enumerate(self.listPlayers):
            self.__printPlayer(i, g)

        txt_istruz = pygame.font.Font(None, 30).render('premere INVIO per iniziare', True, 'white')
        self.display.blit(txt_istruz, (WIDTH / 2 - txt_istruz.get_width() / 2, HEIGHT - 30))


class Game:
    def __init__(self, display):
        self.display = display
        self.imgCampo = pygame.image.load('images/campo.png')
        self.display.blit(self.imgCampo, (0, 0))
        self.ball = Ball()
        self.nomiInseriti = False
        self.team_1 = Team(1)
        self.team_2 = Team(2)

    def reloadWindow(self):
        self.display.blit(self.imgCampo, (0, 0))
        self.team_1.writeBarraTiro(self.ball, self.display)
        self.team_2.writeBarraTiro(self.ball, self.display)

        if self.ball.isInTiro:
            self.team_1.setGiocCheHaTirato()
            self.ball.tiro(self.team_1)
        elif self.ball.isInRimbalzo and not self.ball.isInTiro:
            self.ball.rimbalzoFerro()
            self.team_1.yFrecciaTiro = HEIGHT - self.team_1.imgFrecciaTiro.get_height()
        elif self.ball.isCanestro and not self.ball.isInTiro:
            self.ball.completeCanestro()
            if not self.team_1.puntiGiaAgg:
                self.team_1.aggiornaPunteggio(self.ball)
                self.team_1.puntiGiaAgg = True
            self.team_1.yFrecciaTiro = HEIGHT - self.team_1.imgFrecciaTiro.get_height()
        elif self.ball.isInPassaggio:
            self.ball.passaggio()
        else:
            self.ball.palleggia()

        self.display.blit(self.ball.imgBall, self.ball.coordToDraw())

        for p in self.team_1.players:
            p.updatePlayer(self.ball, self.team_1.attackTo)
            if not p.selected:
                if p.x < self.ball.x:
                    p.drawPlayer(self.display, 'right', self.team_1.imgTriangle)
                else:
                    p.drawPlayer(self.display, 'left', self.team_1.imgTriangle)
            else:
                p.drawPlayer(self.display, self.team_1.attackTo, self.team_1.imgTriangle)

    def __checkMovimentiComune(self, team, up, down, right, left, tiro):
        keys = pygame.key.get_pressed()
        if keys[left]:
            team.attackTo = 'left'
            for g in team.players:
                if g.selected and g.x > self.__calcoloCateto(g.y) - 30 and not g.inSalto and g.z == 0:
                    g.x -= 15
                    g.giaMossa = True
                    break
        if keys[right]:
            team.attackTo = 'right'
            for g in team.players:
                if g.selected and g.x < WIDTH - self.__calcoloCateto(g.y) - 140 and not g.inSalto and g.z == 0:
                    g.x += 15
                    g.giaMossa = True
                    break
        if keys[down]:
            for g in team.players:
                if g.selected and g.y > Y_BORDO_2_CAMPO + 15 and not g.inSalto and g.z == 0:
                    g.y -= 15
                    g.giaMossa = True
                    break
        if keys[up]:
            for g in team.players:
                if g.selected and g.y < Y_BORDO_2_CAMPO + Y_CAMPO - 15 and not g.inSalto and g.z == 0:
                    g.y += 15
                    g.giaMossa = True
                    if team.attackTo == 'left' and g.x > WIDTH - self.__calcoloCateto(g.y) - 140:
                        g.x = WIDTH - self.__calcoloCateto(g.y) - 140
                    elif g.x < self.__calcoloCateto(g.y) - 20:
                        g.x = self.__calcoloCateto(g.y) - 20
                    break
        if not keys[tiro] and team.isInSceltaTiro:
            self.ball.staPalleggiando = False
            self.ball.y += self.ball.z
            self.ball.z = 0
            self.ball.isInTiro = True
            for g in team.players:
                if g.selected:
                    g.giaMossa = False
                    g.haLaPalla = False
                    self.ball.yGiocCheTira = g.y
            self.ball.x0, self.ball.y0 = self.ball.x, HEIGHT - self.ball.y

            self.ball.preparazioneTiro(HEIGHT - team.imgFrecciaTiro.get_height() / 2 - team.yFrecciaTiro)
            self.ball.calcTraiettoria(self.ball.x0)
            for g in team.players:
                if g.selected:
                    g.haLaPalla = False
            self.ball.isAlone = True
            team.isInSceltaTiro = False
            team.dirFrecciaTiro = 'up'

    def checkMovimentiTeam_1(self):
        self.__checkMovimentiComune(self.team_1, K_w, K_s, K_d, K_a, K_x)

    def checkMovimentiTeam_2(self):
        self.__checkMovimentiComune(self.team_2, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE)

    def __checkAzioniComune(self, key, team, salto, cambioG, tiro, passaggio):
        if key == salto:
            self.ball.staPalleggiando = False
            for p in team.players:
                if p.selected:
                    p.inSalto = True
            if team.attackTo == 'left':
                self.ball.x += SIZE_BALL[0] / 2
            else:
                self.ball.x -= SIZE_BALL[0] / 2
        elif key == cambioG:
            iNewSelected, distance = -1, (WIDTH ** 2 + HEIGHT ** 2) ** (1 / 2)
            for i, g in enumerate(team.players):
                if g.selected:
                    g.selected = False
                    continue
                _distance = (abs(g.x - self.ball.x) ** 2 + abs(g.y - self.ball.y) ** 2) ** 0.5
                if iNewSelected == -1 or _distance < distance:
                    distance = _distance
                    iNewSelected = i
            if iNewSelected != -1:
                team.players[iNewSelected].selected = True
        elif key == tiro and not self.ball.isInTiro:
            for g in team.players:
                if g.haLaPalla:
                    team.isInSceltaTiro = True
                    team.puntiGiaAgg = False
                    break
        elif key == passaggio and team.isInPossesso():
            arrAltriGioc = [g for g in team.players if not g.selected]
            for g in team.players:
                if g.selected:
                    gSel = g
                    g.giaMossa = False

            gRicev, dist = None, -1
            for g in arrAltriGioc:
                if g.inMovimento:
                    gRicev = g
            if gRicev is None:
                for g in arrAltriGioc:
                    __dist = (abs(gSel.x - g.x) ** 2 + abs(gSel.y + gSel.z - g.y) ** 2) ** .5
                    if __dist < dist or dist == -1:
                        dist = __dist
                        gRicev = g

            self.ball.isInPassaggio = True
            self.ball.staPalleggiando = False
            gSel.haLaPalla = False
            self.ball.preparazionePassaggio(gSel, gRicev)

    def checkAzioniTeam_1(self, key):
        self.__checkAzioniComune(key, self.team_1, K_e, K_r, K_x, K_c)

    def checkAzioniTeam_2(self, key):
        self.__checkAzioniComune(key, self.team_2, K_SPACE, K_l, K_p, K_o)

    def __calcoloCateto(self, y):
        i = y / math.cos(15)
        return (i ** 2 - y ** 2) ** .5


class Ball:
    def __init__(self):
        self.imgBall = pygame.image.load('images/palla.png')
        self.x = WIDTH / 2 - SIZE_BALL[0] / 2
        self.y = Y_CAMPO / 2 + Y_BORDO_2_CAMPO + SIZE_BALL[1] + 120
        self.z = 0
        self.staPalleggiando = True
        self.isPalleggioVersoAlto = True
        self.x0 = self.x
        self.y0 = self.y
        self.yGiocCheTira = -1
        self.a_b_c = {'a': 0, 'b': 0, 'c': 0}
        self.m_q = {'m': 0, 'q': 0}
        self.giocRicevitorePassaggio = None
        self.giocPassatore = None
        self.listX = []
        self.isInTiro = False
        self.isInRimbalzo = False
        self.isCanestro = False
        self.calcRimbFatto = False
        self.isAlone = False
        self.isInPassaggio = False

    def palleggia(self):
        if self.staPalleggiando and self.isPalleggioVersoAlto and self.z < 20:
            self.z += 7
            if self.z >= 20:
                self.isPalleggioVersoAlto = False
        elif self.staPalleggiando and not self.isPalleggioVersoAlto and self.z > 0:
            self.z -= 7
            if self.z <= 0:
                self.isPalleggioVersoAlto = True

    def coordToDraw(self):
        return self.x, HEIGHT - self.y - self.z

    def preparazioneTiro(self, yBarraTiro):
        if yBarraTiro <= 185:
            coo = FERRO_1_CANESTRO_2
        elif yBarraTiro >= 224:
            coo = FERRO_2_CANESTRO_2
        else:
            coo = COORD_CANESTRO_2

        x0, x1 = self.x0, coo[0] - SIZE_BALL[0] / 2 - 5
        y0, y1 = HEIGHT - self.y0, HEIGHT - coo[1] if x1 > x0 else HEIGHT - coo[1] - SIZE_BALL[1] * 3 / 2
        x2, y2 = x1 + (x0 - x1) / 2 if x0 > x1 else x0 + 3 * (x1 - x0) / 4, HEIGHT - 45
        self.listX = [x0, x1, x2]

        a = np.array([[x0 ** 2, x0, 1], [x1 ** 2, x1, 1], [x2 ** 2, x2, 1]])
        b = np.array([y0, y1, y2])
        sol = np.linalg.solve(a, b)
        self.a_b_c['a'] = sol[0]
        self.a_b_c['b'] = sol[1]
        self.a_b_c['c'] = sol[2]

    def tiro(self, team):
        if HEIGHT - team.yFrecciaTiro < 205:
            cBallInTiro = FERRO_1_CANESTRO_2
            self.isInRimbalzo = True
        elif HEIGHT - team.yFrecciaTiro > 244:
            cBallInTiro = FERRO_2_CANESTRO_2
            self.isInRimbalzo = True
        else:
            cBallInTiro = COORD_CANESTRO_2
            self.isCanestro = True

        if self.listX[0] < self.listX[1]:
            if self.x + SIZE_BALL[0] / 2 >= cBallInTiro[0]:
                self.isInTiro = False
            elif self.x + 12 < cBallInTiro[0] - SIZE_BALL[0] / 2:
                self.calcTraiettoria(self.x + 12)
            else:
                self.x = cBallInTiro[0] - SIZE_BALL[0] / 2 - 5
                self.calcTraiettoria(self.x + 12)
        elif self.x <= cBallInTiro[0]:
            self.isInTiro = False
        elif self.x - 5 > cBallInTiro[0] - SIZE_BALL[0] / 2 - 10:
            self.calcTraiettoria(self.x - 5)
        else:
            self.x = cBallInTiro[0] - SIZE_BALL[0] / 2 - 10
            self.calcTraiettoria(self.x - 5)

    def prepRimbalzoFerro(self):
        x0, x1 = self.listX[0], self.listX[1]
        if x1 > x0:
            x0r, x1r, x2r = x1, x0 + (x1 - x0) / 2, x1 - (x1 - x0) / 4
        else:
            x0r, x1r, x2r = x1, x0, x1 + (x0 - x1) / 2
        self.calcTraiettoria(x0r)
        y0r, y1r, y2r = self.y, self.yGiocCheTira + SIZE_BALL[1], HEIGHT - Y_RIM_FERRO
        self.listX = [x0r, x1r, x2r]

        a = np.array([[x0r ** 2, x0r, 1], [x1r ** 2, x1r, 1], [x2r ** 2, x2r, 1]])
        b = np.array([y0r, y1r, y2r])
        sol = np.linalg.solve(a, b)
        self.a_b_c['a'] = sol[0]
        self.a_b_c['b'] = sol[1]
        self.a_b_c['c'] = sol[2]

    def rimbalzoFerro(self):
        if not self.calcRimbFatto:
            self.prepRimbalzoFerro()
            self.calcRimbFatto = True
        if self.listX[0] > self.listX[1]:
            if self.x <= self.listX[1]:
                self.isInRimbalzo = False
                self.calcRimbFatto = False
                self.isAlone = True
            elif self.x - 8 > self.listX[1]:
                self.calcTraiettoria(self.x - 8)
            else:
                self.x = self.listX[1]
                self.calcTraiettoria(self.x)
        else:
            if self.x >= self.listX[1]:
                self.isInRimbalzo = False
                self.calcRimbFatto = False
                self.isAlone = True
            elif self.x + 8 < self.listX[1]:
                self.calcTraiettoria(self.x + 8)
            else:
                self.x = self.listX[1]
                self.calcTraiettoria(self.x)

    def completeCanestro(self):
        if self.y == self.yGiocCheTira:
            self.isCanestro = False
            self.isAlone = True
        elif self.y - 35 > self.yGiocCheTira:
            self.y -= 35
        else:
            self.y = self.yGiocCheTira

    def preparazionePassaggio(self, gioc1, gioc2):
        self.giocPassatore = gioc1
        self.giocRicevitorePassaggio = gioc2
        x1 = gioc2.x + 30 if gioc2.giratoDa == 'left' else gioc2.x + gioc2.imgFace2Left.get_width() + gioc2.imgHand2Left.get_width() - 30
        y1 = gioc2.y + gioc2.imgShoes2Left.get_height() + gioc2.imgHand2Left.get_height() - SIZE_BALL[1] / 2 if gioc2.giratoDa == 'left' else gioc2.y + gioc2.imgShoes2Right.get_height() + gioc2.imgHand2Right.get_height() - SIZE_BALL[1] / 2
        a = np.array([[self.x, 1], [x1, 1]])
        b = np.array([self.y, y1])

        sol = np.linalg.solve(a, b)
        self.m_q['m'] = sol[0]
        self.m_q['q'] = sol[1]

    def passaggio(self):
        g = self.giocRicevitorePassaggio
        x = g.x + 30 if g.giratoDa == 'left' else g.x + g.imgFace2Left.get_width() + g.imgHand2Left.get_width() - 30

        if self.x == x:
            self.giocPassatore.selected = False
            self.isInPassaggio = False
            g.haLaPalla = True
            g.selected = True
            self.staPalleggiando = True
        elif self.x > x:
            if self.x - 23 > x:
                self.calcPassaggio(self.x - 23)
            else:
                self.calcPassaggio(x)
        elif self.x + 23 < x:
            self.calcPassaggio(self.x + 23)
        else:
            self.calcPassaggio(x)

    def calcTraiettoria(self, x):
        y = self.a_b_c['a'] * x * x + self.a_b_c['b'] * x + self.a_b_c['c']
        self.x = x
        self.y = y

    def calcPassaggio(self, x):
        y = self.m_q['m'] * x + self.m_q['q']
        self.x = x
        self.y = y


class Team:
    def __init__(self, n):
        self.attackTo = 'right' if n == 1 else 'left'
        self.imgTriangle = pygame.image.load('images/triangolo_bianco.png') if n == 1 else pygame.image.load('images/triangolo_verde.png')
        self.imgBarraTiro = pygame.image.load('images/barraTiro.png')
        self.imgFrecciaTiro = pygame.image.load('images/freccia_verde.png')
        self.players = []
        self.isInSceltaTiro = False
        self.dirFrecciaTiro = 'up'
        self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height()
        self.giocCheHaTirato = None
        self.puntiGiaAgg = False
        self.puntiPartita = 0

    def setGiocatori(self, g):
        n = 1 if self.attackTo == 'right' else 2
        giocBianchi = ('anthony_davis.png', 'domantas_sabonis.png', 'giannis_antetokounmpo.png', 'james_harden.png', 'jason_tatum.png', 'lebron_james.png', 'steph_curry.png')
        self.players = [Player('images/players/faces/' + g[0]['path'], g[0]['path'] in giocBianchi, n, 600, True, True),
                        Player('images/players/faces/' + g[1]['path'], g[1]['path'] in giocBianchi, n, 400),
                        Player('images/players/faces/' + g[2]['path'], g[2]['path'] in giocBianchi, n, 200)]

    def isInPossesso(self):
        for g in self.players:
            if g.haLaPalla:
                return True
        return False

    def writeBarraTiro(self, ball, display):
        if self.isInSceltaTiro or ball.isInTiro:
            hGeneric = HEIGHT - self.imgFrecciaTiro.get_height() / 2

            if self.attackTo == 'right':
                display.blit(self.imgBarraTiro, (10, hGeneric - self.imgBarraTiro.get_height()))
            else:
                display.blit(self.imgBarraTiro, (WIDTH - 10 - self.imgBarraTiro.get_width(), hGeneric - self.imgBarraTiro.get_height()))

            if hGeneric - self.yFrecciaTiro <= 147 or hGeneric - self.yFrecciaTiro >= 262:
                freccia = pygame.image.load('images/freccia_grigia.png')
            elif 148 <= hGeneric - self.yFrecciaTiro <= 173 or 236 <= hGeneric - self.yFrecciaTiro <= 261:
                freccia = pygame.image.load('images/freccia_arancione.png')
            elif 174 <= hGeneric - self.yFrecciaTiro <= 185 or 224 <= hGeneric - self.yFrecciaTiro <= 235:
                freccia = pygame.image.load('images/freccia_gialla.png')
            else:
                freccia = pygame.image.load('images/freccia_verde.png')

            if self.attackTo == 'right':
                display.blit(freccia, (10 + self.imgBarraTiro.get_width(), self.yFrecciaTiro))
            else:
                display.blit(freccia, (WIDTH - 20 - self.imgBarraTiro.get_width() - freccia.get_width(), self.yFrecciaTiro))

            if self.dirFrecciaTiro == 'up' and self.isInSceltaTiro:
                if self.yFrecciaTiro - 20 <= HEIGHT - self.imgFrecciaTiro.get_height() / 2 - self.imgBarraTiro.get_height():
                    self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height() / 2 - self.imgBarraTiro.get_height()
                    self.dirFrecciaTiro = 'down'
                else:
                    self.yFrecciaTiro -= 20
            elif self.isInSceltaTiro:
                if self.yFrecciaTiro + 20 >= HEIGHT - self.imgFrecciaTiro.get_height():
                    self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height()
                    self.dirFrecciaTiro = 'up'
                else:
                    self.yFrecciaTiro += 20

    def aggiornaPunteggio(self, ball: Ball):
        x, y, v = self.giocCheHaTirato.x, self.giocCheHaTirato.y, self.giocCheHaTirato.giratoDa
        if self.attackTo == 'right':
            for d in LINEA_3_CAN_2:
                if int(d['y']) == int(y):
                    if (v == 'right' and x <= d['x']) or (v == 'left' and x <= d['x'] - 60):
                        self.puntiPartita += 3
                    else:
                        self.puntiPartita += 2
                    return
        else:
            pass

        for g in self.players:
            if g.selected and not g.giaMossa and ball.giocPassatore is not None:
                ball.giocPassatore.stats['assist'] += 1

    def setGiocCheHaTirato(self):
        for g in self.players:
            if g.selected:
                self.giocCheHaTirato = g
                return


class Player:
    def __init__(self, path, isWhite, team, x, selected=False, haLaPalla=False):
        self.imgFace2Right = pygame.image.load(path)
        self.imgFace2Left = pygame.transform.flip(self.imgFace2Right, True, False)
        self.imgShoes2Right = pygame.image.load('images/players/shoes.png')
        self.imgShoes2Left = pygame.transform.flip(self.imgShoes2Right, True, False)
        self.imgHand2Right = pygame.image.load('images/players/mano_bianca.png') if isWhite else pygame.image.load('images/players/mano_nera.png')
        self.imgHand2Left = pygame.transform.flip(self.imgHand2Right, True, False)
        self.imgTshirt2Right = pygame.image.load('images/players/maglia_1.png') if team == 1 else pygame.image.load('images/players/maglia_2.png')
        self.imgTshirt2Left = pygame.transform.flip(self.imgTshirt2Right, True, False)
        self.x = x  # temporaneo
        self.y = Y_CAMPO / 2 + Y_BORDO_2_CAMPO  # + self.imgTshirt2Right.get_height() + self.imgFace2Right.get_height()
        self.z = 0
        self.inMovimento = False
        self.isWhite = isWhite
        self.selected = selected
        self.inSalto = False
        self.haLaPalla = haLaPalla
        self.giratoDa = 'right' if team == 1 else 'left'
        self.giaMossa = False
        self.stats = {'punti': 0, 'rimbalzi': 0, 'assist': 0, 'recuperi': 0, 'blocchi': 0, 'tiri campo': {'segnati': 0, 'totali': 0}, 'tiri 3': {'segnati': 0, 'totali': 0}}

    def __closeSaltoInPassaggio(self):
        if self.z > 0:
            self.z -= 9
        if self.z < 0:
            self.z = 0

    def updatePlayer(self, ball: Ball, verso):
        if self.selected:
            if self.inSalto and self.z < 120:
                self.z += 9
                if self.haLaPalla:
                    ball.z += 9
                return
            elif self.inSalto and 120 < self.z < 135:
                self.z += 4.5
                if self.haLaPalla:
                    ball.z += 4.5
                return

            self.inSalto = False
            if not ball.isInTiro and not ball.isCanestro and not ball.isInRimbalzo:
                ball.staPalleggiando = True

            if self.z > 0:
                self.z -= 9
                if self.haLaPalla:
                    ball.z -= 9
            elif self.z < 0:
                self.z = 0
                if self.haLaPalla:
                    ball.z = 0

            self.__setRecuperoPalla(ball)
            if not ball.isInTiro and not ball.isInRimbalzo and not ball.isCanestro and self.haLaPalla:
                if verso == 'left':
                    ball.x = self.x + 30
                    ball.y = self.y + self.imgShoes2Left.get_height() + self.imgHand2Left.get_height() - SIZE_BALL[1] / 2
                else:
                    ball.x = self.x + self.imgFace2Left.get_width() + self.imgHand2Left.get_width() - 30
                    ball.y = self.y + self.imgShoes2Right.get_height() + self.imgHand2Right.get_height() - SIZE_BALL[1] / 2
        else:
            self.__closeSaltoInPassaggio()

    def __setRecuperoPalla(self, ball: Ball):
        if not ball.isAlone:
            return
        xB, yB = ball.x, ball.y + ball.z
        if self.giratoDa == 'left':
            if self.x - 30 <= xB <= self.x + 30 and int(self.y + self.z) <= int(yB - SIZE_BALL[1]) <= int(self.y + self.z + self.imgShoes2Left.get_height() + self.imgHand2Left.get_height() - SIZE_BALL[1] / 2):
                self.haLaPalla = True
                ball.isAlone = False
                ball.staPalleggiando = True
                ball.isPalleggioVersoAlto = True
                ball.palleggia()
                self.stats['rimbalzi'] += 1
        elif self.x + self.imgFace2Left.get_width() + self.imgHand2Left.get_width() - 60 <= xB <= self.x + self.imgFace2Left.get_width() + self.imgHand2Left.get_width() and int(self.y + self.z) <= int(yB - SIZE_BALL[1]) <= int(self.y + self.z + self.imgShoes2Left.get_height() + self.imgHand2Left.get_height() - SIZE_BALL[1] / 2):
            self.haLaPalla = True
            ball.isAlone = False
            ball.staPalleggiando = True
            ball.isPalleggioVersoAlto = True
            ball.palleggia()
            self.stats['rimbalzi'] += 1

    def drawPlayer(self, display, verso, triangolo):
        self.giratoDa = verso
        img1 = self.imgFace2Right if verso == 'right' else self.imgFace2Left
        img2 = self.imgTshirt2Right if verso == 'right' else self.imgTshirt2Left
        img3 = self.imgShoes2Right if verso == 'right' else self.imgShoes2Left
        img4 = self.imgHand2Right if verso == 'right' else self.imgHand2Left

        if verso == 'right':
            display.blit(img2, (self.x + (img1.get_width() - img2.get_width()) / 2 + 5, HEIGHT - self.y - img3.get_height() - img2.get_height() + 10 - self.z))
            display.blit(img1, (self.x, HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() + 26 - self.z))
            if self.selected:
                display.blit(triangolo, (self.x + (img1.get_width() - triangolo.get_width()) / 2, HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() - 20 - self.z))
            if self.inSalto:
                newShoes = pygame.image.load('images/players/shoesInSalto.png') if verso == 'right' else pygame.transform.flip(pygame.image.load('images/players/shoesInSalto.png'), True, False)
                display.blit(newShoes, (self.x + (img1.get_width() - img2.get_width()) / 2, HEIGHT - self.y - img3.get_height() - self.z - 5))
                newHand = pygame.image.load('images/players/mano_bianca_inSalto.png') if self.isWhite else pygame.image.load('images/players/mano_nera_inSalto.png')
                display.blit(newHand, (self.x + img1.get_width() - img4.get_width() / 1.5, HEIGHT - self.y - img3.get_height() - newHand.get_height() - self.z))
            else:
                display.blit(img3, (self.x + (img1.get_width() - img2.get_width()) / 2, HEIGHT - self.y - img3.get_height() - self.z))
                display.blit(img4, (self.x + img1.get_width() - img4.get_width() / 1.5 + 15, HEIGHT - self.y - img3.get_height() - img4.get_height() - self.z - 20))
        else:
            display.blit(img2, (self.x + img1.get_width() + (img1.get_width() - img2.get_width()) / 2 - 5, HEIGHT - self.y - img3.get_height() - img2.get_height() + 10 - self.z))
            display.blit(img1, (self.x + img1.get_width(), HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() + 26 - self.z))
            if self.selected:
                display.blit(triangolo, (self.x + img1.get_width() + (img1.get_width() - triangolo.get_width()) / 2, HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() - 20 - self.z))
            if self.inSalto:
                newShoes = pygame.image.load('images/players/shoesInSalto.png') if verso == 'right' else pygame.transform.flip(pygame.image.load('images/players/shoesInSalto.png'), True, False)
                display.blit(newShoes, (self.x + img1.get_width(), HEIGHT - self.y - img3.get_height() - self.z - 5))
                newHand = pygame.transform.flip(pygame.image.load('images/players/mano_bianca_inSalto.png') if self.isWhite else pygame.image.load('images/players/mano_nera_inSalto.png'), True, False)
                display.blit(newHand, (self.x + img1.get_width() - img4.get_width() / 4, HEIGHT - self.y - img3.get_height() - newHand.get_height() - self.z))
            else:
                display.blit(img3, (self.x + img1.get_width(), HEIGHT - self.y - img3.get_height() - self.z))
                display.blit(img4, (self.x + img1.get_width() - img4.get_width() / 4 - 15, HEIGHT - self.y - img3.get_height() - img4.get_height() - self.z - 20))


def main():
    pygame.init()
    window = WindowInitial()
    game = Game(window.display)
    # sound = pygame.mixer.Sound('/home/fre/Scrivania/kung_fu_panda.mp3')
    # sound.play()

    while True:
        if not window.inSchermataIniz and not game.nomiInseriti:
            game.team_1.setGiocatori(window.listPlayers[:3])
            game.team_2.setGiocatori(window.listPlayers[3:])
            game.nomiInseriti = True

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if window.inSchermataIniz:
                window.checkEvt(e)
            elif e.type == KEYDOWN and game.nomiInseriti:
                game.checkAzioniTeam_1(e.key)
                game.checkAzioniTeam_2(e.key)

        if window.inSchermataIniz:
            window.updateWindow()
        elif game.nomiInseriti:
            game.checkMovimentiTeam_1()
            game.checkMovimentiTeam_2()
            game.reloadWindow()

        pygame.time.Clock().tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    main()

