from random import randint
import pygame, os
from pygame import *


# Chemins d'accès aux différentes données
file = os.getcwd()  # Chemin du fichier
chemin = os.path.dirname(__file__)  # Ces lignes permettent de retrouver le chemin qui nous intéresse, ici le chemin
# /images pour les utiliser dans le projet
chemin = os.path.dirname(chemin)
pathImage = os.path.join(chemin, "1DEV\images")  # Chemin des images
pathFiles = os.path.join(chemin, "1DEV\sysfiles") # Chemin des fichiers de jeu
pathMusic = os.path.join(chemin, "1DEV\musics") # Chemin des sons de jeu
WHITE = (255, 255, 255) # Définition d'une variable de couleur
RED = (255, 0, 0) # Définition d'une variable de couleur
GREEN = (0, 255, 0) # Définition d'une variable de couleur


def initBoard(difficulty, save):  # Initialisation de variables essentiels.
    # Si save == True on lit dans la sauvegarde sinon on défini les variables par défaut.
    if save:
        difficulty, board, x, y, startingBoard, score, air, heartBroken = saveFile(difficulty)
        bestscore = bestScore(difficulty,0)
    else:
        heartBroken = 0
        x,y,startingBoard = 4,4,0
        depth = difficulty*50
        score = 0
        air =100
        board = [[randint(1,7) if i > 4 else 0 for j in range(9)]for i in range(depth)]
        airPercent = difficulty+2
        for i in range(5,depth,airPercent):
            j = randint(0,8)
            board[i][j] = 8
        bestscore = bestScore(difficulty,score)
    return difficulty, board, x, y, startingBoard, score, air, heartBroken,bestscore


def graviteJoueur(board,x,y,air,score):  # Déplace le joueur vers le bas tant qu'il peut tomber
    while x+1 < len(board) and (board[x+1][y] == 0 or board[x+1][y] == 8):
        if board[x+1][y] == 8:
            board[x+1][y] = 0
            air = min(100,air+20)
            score += 20
        x += 1
    return x, y, air, score


def initDurability(board):  # Initialisation de la durabilité des blocs
    durability = [[5 if board[i][j] == 7 else 0 if board[i][j] == 0 else 1 for j in range(9)] for i in range(len(board))]
    return durability


def timerFunc(mySurface,air):
    font = pygame.font.SysFont('Impact', 50)
    pygame.draw.rect(mySurface, (0, 0, 0), pygame.Rect(775, 327, 200, 1+(100-air))) if air > 0 else print("No air anymore ")
    mySurface.blit(font.render(str(air), True, WHITE), (810, 345)) if air == 100 else mySurface.blit(font.render(str(air), True, WHITE), (818, 345))
    return air


def scoreDisplay(mySurface, score):
    mySurface.blit(pygame.font.SysFont('Impact', 35).render(str(score), True, (255, 255, 255)), (775, 60))


def bestScore(difficulty, score, mode = 0): # Avec mode 0 lecture du HighScore avec mode != 0 Ecriture du HighScore
    difficulty -= 1
    os.chdir(pathFiles)
    if mode == 0:
        with open('bestScore.txt',"r") as f:
            line = f.readline()
            while int(line[0]) != difficulty:
                line = f.readline()
            return int(line[2::])
    else:
        with open('bestScore.txt',"r") as f:
            lines = f.readlines()
        position = 0
        while int(lines[position][0]) != difficulty:
            position += 1
        lines[position] = str(difficulty)+';'+str(score)+'\n'
        with open('bestScore.txt','w') as f:
            f.writelines(lines)


def saveFile(number):
    os.chdir(os.path.dirname(__file__) + "\sysfiles\save" + str(number))
    difficulty = eval(open("difficulty.txt", "r").read())
    board = eval(open("board.txt", "r").read())
    coords = eval(open("x, y.txt", "r").read())  # x et y sous forme de liste
    x, y = coords[0], coords[1]
    air = eval(open("air.txt", "r").read())
    score = eval(open("score.txt", "r").read())
    startingBoard = eval(open("startingBoard.txt", "r").read())
    heartBroken = eval(open("heartBroken.txt", "r").read())
    return difficulty, board, x, y, startingBoard, score, air, heartBroken


def doSave(difficulty, board, x, y, startingBoard, score, air, heartBroken, mySurface, startBoard, bScore, drillerColor):
    fontObj = pygame.font.Font('freesansbold.ttf', 20)
    mySurface.blit(pygame.image.load("game_over.png"), (0, 0))
    mySurface.blit(fontObj.render("Choose your save number :", True, (255, 255, 255)), (410, 290))
    pygame.display.update()
    w = 0
    for i in range(2):
        for j in range(2):
            w += 1
            mySurface.blit(pygame.image.load("buttonSave.png"), ((j * 175) + 337, (i * 50) + 348))
            mySurface.blit(pygame.font.Font('freesansbold.ttf', 25).render("Save " + str(w), True, WHITE),
                           (((j * 175) + 337) + 38, ((i * 50) + 348) + 2))
    pygame.display.update()
    coordSave = [[337, 487, 348, 388], [537, 687, 348, 388],
                 [337, 487, 398, 438], [537, 687, 398, 438]]
    check = True
    while check:
        save = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px, py = event.pos
                for i in range(len(coordSave)):
                    if coordSave[i][0] <= px <= coordSave[i][1] and coordSave[i][2] <= py <= coordSave[i][3]:
                        number = i+1
                        check = False
    os.chdir(os.path.dirname(__file__) + "\sysfiles\save" + str(number))
    names = ["difficulty.txt", "board.txt", "startingBoard.txt", "score.txt", "air.txt", "heartBroken.txt"]
    variables = [difficulty, board, startingBoard, score, air, heartBroken]
    for i in range(len(names)):
        f = open(names[i], "w")
        f.write(str(variables[i]))
        f.close()
    f = open("x, y.txt", "w")
    f.write(str([x, y]))
    f.close()
    displaySurface(mySurface, board, heartBroken, x, y, startBoard, score, bScore, air, difficulty, drillerColor)
    rect = pygame.Surface((300, 625), pygame.SRCALPHA, 32)
    rect.fill((0, 0, 0, 230))
    mySurface.blit(rect, (0, 0))
    mySurface.blit(fontObj.render("- - - |PAUSED| - - -", True, (255, 255, 255)), (60, 50))
    mySurface.blit(fontObj.render("Resume", True, (255, 255, 255)), (50, 150))
    mySurface.blit(fontObj.render("Save", True, (255, 255, 255)), (50, 200))
    mySurface.blit(fontObj.render("Quit the game", True, (255, 255, 255)), (50, 250))


def displaySurface(mySurface, board, heartBroken, x, y, startBoard, score, bscore, air, difficulty, drillerColor):
    # Affichage visuel du plateau et de variables
    os.chdir(pathImage)
    mrDrillerSkin = ["mrDriller_Rightx4.png", "mrDrillerBlack_Rightx4.png", "mrDrillerRed_Rightx4.png",
                      "mrDriller_Leftx4.png","mrDrillerBlack_Leftx4.png", "mrDrillerRed_Leftx4.png"]
    mrDrillerLeft = pygame.image.load(mrDrillerSkin[drillerColor]).convert_alpha()
    mrDrillerRight = pygame.image.load(mrDrillerSkin[drillerColor+3]).convert_alpha()
    wallpaper = pygame.image.load("wallpaper.png")
    mySurface.blit(wallpaper, (0, 0))
    pygame.draw.rect(mySurface, (0, 0, 0), (725, 510, (heartBroken*85), 70))
    mySurface.blit(pygame.image.load("mrDriller_Right.png"), (615, (startBoard+3)*(570//(50*difficulty))))
    timerFunc(mySurface, air)
    mySurface.blit(pygame.font.SysFont('Impact', 35).render(str(score), True, (255, 255, 255)), (775, 60))
    mySurface.blit(pygame.font.SysFont('Impact', 35).render(str(bscore), True, (255, 255, 255)), (775, 206))
    for i in range(startBoard, min(startBoard+9, len(board))):
        for j in range(9):
            if x == i and y == j:
                mySurface.blit(mrDrillerLeft, (j * 60 + 67, (i-startBoard) * 70))
            elif 0 < board[i][j] < 9:
                p = board[i][j] - 1
                os.chdir(pathImage)
                colorBlock = ["block_b.png", "block_g.png", "block_y.png", "block_r.png", "block_crystal.png", "block_w.png",
                              "block_brown.png",
                              "air.png"]
                block = pygame.image.load(colorBlock[p]).convert_alpha()
                mySurface.blit(block, (j * 60 + 67, (i-startBoard) * 70))


def move(board, x, y, direction, air, score):  # Action du joueur qui le déplace dans la direction donnée
    i, j = direction[0], direction[1]
    if board[x][y+j] == 8:
        board[x][y + j] = 0
        score += 20
        y += j
        air = min(100, air+20)
    elif board[x][y+j] != 0 and (board[x-1][y+j] == 0 or board[x-1][y+j] == 8) and board[x-1][y] == 0:
        if board[x-1][y+j] == 8:
            air = min(air+20, 100)
            board[x-1][y+j] = 0
        x -= 1
        y += j
    elif board[x][y+j] == 0:
        y += j
    return board, x, y, air, score


def drill(board, x, y, blockDurability, direction, air, score):
    # Action du joueur qui consiste à miner un bloc dans une direction donner
    i, j = direction[0], direction[1]
    if 0 <= y+j <= 8 and blockDurability[x+i][y+j] >= 1:
        blockDurability[x + i][y+j] -= 1
        if blockDurability[x+i][y+j] == 0:
            if board[x + i][y + j] == 7:
                air = max(0, air - 20)
            blockBroken = []
            if board[x + i][y + j] == 6:
                blockBroken.append((x + i, y + j))
            else:
                blockRecursive(board, x + i, y + j, blockBroken, board[x + i][y + j])
            for block in blockBroken:
                board[block[0]][block[1]] = 0
                blockDurability[block[0]][block[1]] = 0
                score += 50
    return board, blockDurability, air, score


def blockCanFall(board, i, j):  # Retourne vrai si le bloc peut tomber
    return True if board[i+1][j] == 0 or board[i][j] == board[i+1][j] else False


def canFall(board, i, j):  # Retourne Vrai si un bloc ou un des blocs adjacents
    blocks = []
    blockRecursive(board, i, j, blocks, board[i][j])
    for block in blocks:
        if not blockCanFall(board, block[0], block[1]):
            return False
    return True


def gravite(board, durability, maxrange, score, x, y, heartBroken):
    # Fonction qui déplace les blocs d'une colonne de 1 vers le bas
    for j in range(9):
        for i in range(maxrange-1, max(0, x-6), -1):
            if canFall(board, i, j) and board[i][j] != 0:
                blocks = []
                blockRecursive(board, i, j, blocks, board[i][j])
                for block in blocks:
                    i, j = block
                    board[i+1][j], board[i][j] = board[i][j], 0
                    durability[i + 1][j], durability[i][j] = durability[i][j], 0
                    if i+1 == x and j == y:
                        heartBroken += 1
                        for position in range(x-4, x):
                            board[position][j] = 0
                            durability[position][j] = 0
    return board, durability, score, heartBroken


def reset(difficulty):  # Reset du plateau et de toutes les variables liées au joueur
    difficulty, board, x, y, startingBoard, score, air, heartBroken,bestscore = initBoard(difficulty, False)
    air = 100
    x, y = 4, 4
    return board, air, x, y, startingBoard, difficulty, score, air, heartBroken, bestscore


def pause(mySurface, timer, heartBroken, board, x, y, startingBoard, score, air, difficulty, bestscore, drillerColor):
    fontObj = pygame.font.Font('freesansbold.ttf', 20)
    pygame.time.set_timer(timer, 0)
    for i in range(300):
        pygame.draw.rect(mySurface, (0, 0, 0), (0, 0, i, 625))
        pygame.display.update()
    displaySurface(mySurface, board, heartBroken, x, y, startingBoard, score, bestscore, air, difficulty, drillerColor)
    rect = pygame.Surface((300, 625), pygame.SRCALPHA, 32)
    rect.fill((0, 0, 0, 230))
    mySurface.blit(rect, (0, 0))
    mySurface.blit(fontObj.render("- - - |PAUSED| - - -", True, (255, 255, 255)), (60, 50))
    mySurface.blit(fontObj.render("Resume", True, (255, 255, 255)), (50, 150))
    mySurface.blit(fontObj.render("Save", True, (255, 255, 255)), (50, 200))
    mySurface.blit(fontObj.render("Quit the game", True, (255, 255, 255)), (50, 250))
    inPause = True
    while inPause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leftTheGame(mySurface, board, heartBroken, x, y, startingBoard, score, bestscore, air,
                            difficulty, drillerColor)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px, py = event.pos
                if 45 <= px <= 135 and 145 <= py <= 175:  # Resume button
                    inPause = False
                    pygame.time.set_timer(timer, 1000)
                elif 45 <= px <= 105 and 195 <= py <= 225:  # Save button
                    # Montrer la liste des saves
                    doSave(difficulty, board, x, y, startingBoard, score, air, heartBroken, mySurface,
                           startingBoard, bestscore, drillerColor)
                elif 45 <= px <= 245 and 245 <= py <= 275:  # Quit the game button
                    leftTheGame(mySurface, board, heartBroken, x, y, startingBoard, score, bestscore,
                                air, difficulty, drillerColor)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    inPause = False
                    pygame.time.set_timer(timer, 1000)
        pygame.display.update()


def blockRecursive(board, i, j, cases, value):
    # Fonction qui ajoute dans une liste les cases adjacentes d'une certaine case
    if board[i][j] == value and (i, j) not in cases:
        depth = len(board)
        cases.append((i, j))
        for x1 in range(-1, 2, 2):
            if (i + x1) not in cases and 0 <= (i + x1) < depth-1:
                blockRecursive(board, i + x1, j, cases, value)
        for x2 in range(-1, 2, 2):
            if (j + x2) not in cases and 0 <= (j + x2) <= 8:
                blockRecursive(board, i, j + x2, cases, value)


def inLife(heartBroken):  # Dans que le joueur est en vie cette fonction retourne True
    return True if heartBroken < 3 else False


def win(board, x, y, depth):  # Si le joueur atteint la profondeur maximale la fonction retourne True
    return True if x == depth else False


def gameOver(mySurface, difficulty, save, drillerColor, sound):
    os.chdir(pathImage)
    mySurface.blit(pygame.image.load("game_over.png"), (0, 0))
    mySurface.blit(pygame.font.Font('freesansbold.ttf', 75).render("Game Over", True, RED), (340, 300))
    mySurface.blit(pygame.font.Font('freesansbold.ttf', 25).render("Replay", True, WHITE), (300, 385))
    mySurface.blit(pygame.font.Font('freesansbold.ttf', 25).render("Quit", True, WHITE), (700, 385))
    action = False
    while not action:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x,y = event.pos
                if 300 <= x <= 390 and 385 <= y <= 410:
                    init(difficulty, save, drillerColor, sound)
                elif 700 <= x <= 760 and 385 <= y <= 410:
                    pygame.quit()
        pygame.display.update()


def victory(mySurface, difficulty, save, drillerColor, sound):
    os.chdir(pathImage)
    mySurface.blit(pygame.image.load("game_over.png"), (0, 0))
    mySurface.blit(pygame.font.Font('freesansbold.ttf', 75).render("Victory", True, GREEN), (400, 300))
    mySurface.blit(pygame.font.Font('freesansbold.ttf', 25).render("Replay", True, WHITE), (300, 385))
    mySurface.blit(pygame.font.Font('freesansbold.ttf', 25).render("Quit", True, WHITE), (700, 385))
    action = False
    while not action:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 300 <= x <= 390 and 385 <= y <= 410:
                    init(difficulty, save, drillerColor, sound)
                elif 700 <= x <= 760 and 385 <= y <= 410:
                    pygame.quit()
        pygame.display.update()


def game(mySurface, difficulty, save, drillerColor):  # Fonction Principale
    Clock = pygame.time.Clock()
    difficulty, board, x, y, startingBoard, score, air, heartBroken, bestscore = initBoard(difficulty, save)
    depth = len(board)-1
    durability = initDurability(board)
    airlevel, crystal = USEREVENT + 1, USEREVENT + 2
    pygame.time.set_timer(crystal, 5000)
    pygame.time.set_timer(airlevel, 1000)
    displaySurface(mySurface, board, heartBroken, x, y, startingBoard, score, bestscore, air, difficulty, drillerColor)
    while inLife(heartBroken) and not win(board, x, y, depth):
        Clock.tick(60)
        for event in pygame.event.get():
            if event.type == USEREVENT + 1:
                air -= 1
                displaySurface(mySurface, board, heartBroken, x, y, startingBoard, score, bestscore,
                               air, difficulty, drillerColor)
                air = timerFunc(mySurface, air)
                if air <= 0:
                    heartBroken += 1
                    pygame.time.set_timer(airlevel, 1000)
                    air = 100
            elif event.type == USEREVENT + 2:
                for i in range(startingBoard, min(startingBoard+9, depth)):
                    for j in range(9):
                        if board[i][j] == 5:
                            board[i][j] = 0
                board, durability, score, heartBroken = gravite(board, durability, min(startingBoard+8, depth-1),
                                                                score, x, y, heartBroken)
                x, y, air, score = graviteJoueur(board, x, y, air,score)
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == K_ESCAPE:
                    pause(mySurface, airlevel, heartBroken, board, x, y, startingBoard, score, air,
                          difficulty, bestscore, drillerColor)
                elif keys[K_SPACE] and keys[K_LEFT]:
                    direction = (0, -1)
                    board, durability, air, score = drill(board, x, y, durability, direction, air, score)
                elif keys[K_SPACE] and keys[K_RIGHT]:
                    direction = (0, 1)
                    board, durability, air, score = drill(board, x, y, durability, direction, air, score)
                elif keys[K_SPACE] and keys[K_DOWN]:
                    direction = (1, 0)
                    board, durability, air, score = drill(board, x, y, durability, direction, air, score)
                elif keys[K_RIGHT]:
                    if 0 <= y < 8:
                        direction = (0, 1)
                        board, x, y, air, score = move(board, x, y, direction, air, score)
                elif keys[K_LEFT]:
                    if 0 < y <= 8:
                        direction = (0, -1)
                        board, x, y, air, score = move(board, x, y, direction, air, score)
                board, durability, score, heartBroken = gravite(board, durability, min(startingBoard+8, depth-1),
                                                                score, x, y, heartBroken)
                x, y, air, score = graviteJoueur(board, x, y, air, score)
                startingBoard = x - 4 if x - 4 > 0 else 0
                displaySurface(mySurface, board, heartBroken, x, y, startingBoard, score,
                               bestscore, air, difficulty, drillerColor)
        pygame.display.update()
    if score > bestscore:   # Ecrire du HighScore si le score est supérieur
        bestScore(difficulty, score, 1)
    return True if inLife(heartBroken) and win(board, x, y, depth) else False


def init(difficulty, save, drillerColor, sound):  # initialisation du plateau de la fenêtre et du jeu
    os.chdir(pathImage)
    wallpaper = pygame.image.load("wallpaper.png")
    pygame.init()
    pygame.display.set_caption("Mr Driller - The Game")
    pygame.display.set_icon(pygame.image.load("mrDriller_RightX4.png"))
    os.chdir(pathMusic)
    pygame.mixer.music.load("bensound-sweet.mp3")
    pygame.mixer.music.play()
    pygame.mixer_music.set_volume(sound/100)
    mySurface = pygame.display.set_mode((1023, 625))
    mySurface.blit(wallpaper, (0, 0))
    result = game(mySurface, difficulty, save, drillerColor)
    victory(mySurface, difficulty, save, drillerColor, sound) if result else gameOver(mySurface, difficulty, save, drillerColor, sound)


def leftTheGame(mySurface, board, heartBroken, x, y, startBoard, score, bScore, air, difficulty, drillerColor):
    fontObj = pygame.font.Font('freesansbold.ttf', 20)
    textList = [[30, "Do you really want to leave the game ?", (230, 300)],
                [19, "Yes  [you don't really want it]", (190, 370)],
                [19, "No  [the best choice of your life]", (530, 370)]]
    mySurface.blit(pygame.image.load("exitMenu.png"), (-45, 0))
    pygame.display.set_caption("Choose the correct answer", "Exit")
    pygame.display.set_icon(pygame.image.load("exit.png"))
    for i in range(len(textList)):
        mySurface.blit(pygame.font.Font('freesansbold.ttf', textList[i][0]).render(textList[i][1], True, WHITE), textList[i][2])
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px, py = event.pos
                if 190 <= px <= 460 and 370 <= py <= 400:
                    pygame.quit()
                elif 525 <= px <= 825 and 370 <= py <= 400:
                    displaySurface(mySurface, board, heartBroken, x, y, startBoard, score, bScore,
                                   air, difficulty, drillerColor)
                    rect = pygame.Surface((300, 625), pygame.SRCALPHA, 32)
                    rect.fill((0, 0, 0, 230))
                    mySurface.blit(rect, (0, 0))
                    mySurface.blit(fontObj.render("- - - |PAUSED| - - -", True, (255, 255, 255)), (60, 50))
                    mySurface.blit(fontObj.render("Resume", True, (255, 255, 255)), (50, 150))
                    mySurface.blit(fontObj.render("Save", True, (255, 255, 255)), (50, 200))
                    mySurface.blit(fontObj.render("Quit the game", True, (255, 255, 255)), (50, 250))
                    return True
        pygame.display.update()
