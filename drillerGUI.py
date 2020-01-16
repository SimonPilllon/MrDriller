from drillerAlgo import *
file = os.getcwd()  # Chemin du fichier
chemin = os.path.dirname(__file__)
chemin = os.path.dirname(chemin)
pathImage = os.path.join(chemin, "MrDriller-master\images")  # Chemin des images

#Redirection du chemin vers le dossier des images et initialisation des variables essentielles
os.chdir(pathImage)
mySurface = pygame.display.set_mode((1023, 625))
BLACK, WHITE, GREY, drillerColor = (0, 0, 0), (255, 255, 255), (211, 211, 211), 0
pygame.font.init()


def display():  # Procédure d'affichage graphique du menu principal
    pygame.display.set_caption("Mr Driller - Main Menu")
    pygame.display.set_icon(pygame.image.load("mrDriller_RightX4.png"))
    imgList = [["wallpaperMenu.jpg", (0, 0)],
               ["mrDrillerLogo.png", (0, 0)],
               ["mrDriller_Rightx4.png", (420, 225)],
               ["wrench.png", (390, 342)],
               ["howtoplay.png", (390, 440)],
               ["exit.png", (420, 537)]]
    textList = [[35, "Play", WHITE, (495, 250)],
                [35, "Options", WHITE, (470, 350)],
                [35, "How to play", WHITE, (450, 450)],
                [35, "Exit", WHITE, (495, 550)]]
    for i in range(len(imgList)):
        mySurface.blit(pygame.image.load(imgList[i][0]), imgList[i][1])
    for i in range(len(textList)):
        mySurface.blit(pygame.font.SysFont('Impact', textList[i][0]).render(textList[i][1], True, textList[i][2]),
                       textList[i][3])



def playMenu(drillerColor, sound):  # Fonction d'affichage graphique de la sélection de niveau / sauvegarde
    mySurface.blit(pygame.image.load("wallpaperMenu.jpg"), (0, 0))
    mySurface.blit(pygame.image.load("mrDrillerLogo.png"), (0, -50))
    pygame.display.set_caption("Choose a level or a save")
    mySurface.blit(pygame.font.SysFont('Impact', 35).render("Select a level :", True, WHITE), (400, 175))
    w = 0
    for i in range(1,3):
        for j in range(5):
            w += 1
            mySurface.blit(pygame.image.load("button.png"), ((j*200)+37, (i*50)+200))
            mySurface.blit(pygame.font.SysFont('Impact', 25).render("Level "+str(w), True, WHITE),
                           ((j*200)+75, (i*50)+202))
    mySurface.blit(pygame.font.SysFont('Impact', 35).render("Or choose a save :", True, WHITE), (395, 375))
    w = 0
    for i in range(2):
        for j in range(2):
            w += 1
            mySurface.blit(pygame.image.load("buttonSave.png"), ((j*175)+337, (i*50)+450))
            mySurface.blit(pygame.font.SysFont('Impact', 25).render("Save " + str(w), True, WHITE),
                           (((j*175)+337)+38, ((i*50)+450)+2))
    mySurface.blit(pygame.image.load("buttonBack.png"), (437, 575))
    mySurface.blit(pygame.font.SysFont('Impact', 25).render("Back", True, WHITE), (485, 577))
    while 1:
        save = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 360 <= y <= 550:
                    save = True
                elif 437 <= x <= 590 and 575 <= y <= 615:
                    return
                buttons(x, y, save, drillerColor, sound)  # Sert à obtenir la difficulté ou la sauvegarde choisie
        pygame.display.update()


def leftTheGame():  # Fonction d'affichage de menu de sortie du jeu
    textList = [[30, "Do you really want to leave the game ?", (255, 255, 255), (280, 300)],
                [19, "Yes   [ you don't really want it ]", (255, 255, 255), (220, 370)],
                [19, "No   [ the best choice of your life ]", (255, 255, 255), (560, 370)]]
    mySurface.blit(pygame.image.load("exitMenu.png"), (-45, 0))
    pygame.display.set_caption("Choose the correct answer", "Exit")
    pygame.display.set_icon(pygame.image.load("exit.png"))
    for i in range(len(textList)):
        mySurface.blit(pygame.font.SysFont('Impact', textList[i][0]).render(textList[i][1], True, textList[i][2]),
                       textList[i][3])
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 215 <= x <= 455 and 350 <= y <= 400:
                    return False
                elif 555 <= x <= 795 and 350 <= y <= 400:
                    return True
        pygame.display.update()


def buttons(x, y, save, drillerColor, sound):  # Procédure permettant la sélection de niveau ou de sauvegarde
    coords = [[37, 187, 250, 290], [237, 387, 250, 290], [437, 587, 250, 290], [637, 787, 250, 290],
              [837, 987, 250, 290],
              [37, 187, 300, 340], [237, 387, 300, 340], [437, 587, 300, 340], [637, 787, 300, 340],
              [837, 987, 300, 340]]
    coordSave = [[337, 487, 450, 490], [537, 687, 450, 490],
                 [337, 487, 500, 540], [537, 687, 500, 540]]
    if not save:
        for i in range(len(coords)):
            if coords[i][0] <= x <= coords[i][1] and coords[i][2] <= y <= coords[i][3]:
                init(i+1, save, drillerColor, sound)
    else:
        for i in range(len(coordSave)):
            if coordSave[i][0] <= x <= coordSave[i][1] and coordSave[i][2] <= y <= coordSave[i][3]:
                init(i+1, save, drillerColor, sound)


def displayOptions(w, sound):  # Procédure d'affichage graphique des options du menu
    images = ["wallpaperMenu.jpg", "mrDrillerLogo.png", "buttonBack.png", "button.png"]
    coordsImg = [[0, 0], [0, -50], [437, 575], [437, 450]]
    text = ["Define your options :", "Choose your skin : ", "<", ">", "Sound :", "-", "+", str(sound), "Back",
            "Credits"]
    coordsTxt = [[400, 175], [300, 300], [500, 303], [600, 303], [413, 375], [502, 375], [600, 375], [545, 375],
                 [485, 577], [470, 452]]
    for i in range(len(images)):
        mySurface.blit(pygame.image.load(images[i]), coordsImg[i])
    for i in range(len(text)):
        mySurface.blit(pygame.font.SysFont('Impact', 25).render(text[i], True, WHITE), coordsTxt[i])
    pygame.display.set_caption("Mr Driller - Options")
    mrDrillerSkin = ["mrDriller_Rightx4.png", "mrDrillerBlack_Rightx4.png", "mrDrillerRed_Rightx4.png"]
    mySurface.blit(pygame.image.load(mrDrillerSkin[w]), (530, 280))


def options():  # Fonction de sélection des diverses options proposées
    w, sound = 0, 0
    displayOptions(w, sound)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 600 <= x <= 625 and 303 <= y <= 330:
                    w += 1 if w != 2 else 0
                elif 500 <= x <= 525 and 303 <= y <= 330:
                    w -= 1 if w != 0 else 0
                elif 500 <= x <= 515 and 375 <= y <= 400 and sound > 0:
                    sound -= 10
                elif 600 <= x <= 615 and 375 <= y <= 400 and sound < 100:
                    sound += 10
                elif 437 <= x <= 590 and 450 <= y <= 490:
                    credits()
                elif 437 <= x <= 590 and 575 <= y <= 615:
                    return w, sound
            displayOptions(w, sound)
        pygame.display.update()


def credits():  # Fonction d'affichage des crédits du jeu
    images = ["wallpaperMenu.jpg", "mrDrillerLogo.png", "buttonBack.png", "credits.png"]
    coordsImg = [[0, 0], [0, -50], [437, 575], [75, 150]]
    text = ["Back", "MrDriller original concept is a property of Namco's company",
            "This version of MrDriller has been realised by Simon PILLON and Ferenc DEKONINCK",
            "Developement manager & commercial", "Simon PILLON  - 291170", "Graphics manager & commercial",
            "Ferenc DEKONINCK  - 291177", "Use of ARCO Font is free", "thanks to Rafael Olivo",
            "Free music from www.bensound.com"]
    coordsTxt = [[485, 577], [200, 175], [90, 210], [100, 300], [175, 335], [100, 370], [175, 405], [600, 300],
                 [613, 325], [530, 380]]
    for i in range(len(images)):
        mySurface.blit(pygame.image.load(images[i]), coordsImg[i])
    for i in range(len(text)):
        mySurface.blit(pygame.font.SysFont('Impact', 25).render(text[i], True, WHITE),
                       coordsTxt[i])
    pygame.display.set_caption("MrDriller's credits")
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 437 <= x <= 590 and 575 <= y <= 615:
                    return
            pygame.display.update()


def howToPlay():  # Fonction d'affichage d'une présentation de la manière de jouer
    pygame.display.set_caption("How To Play MrDriller ?")
    listImg = ["wallpaperMenu.jpg", "mrDrillerLogo.png", "buttonBack.png", "keyboard_left.png", "keyboard_down.png",
               "keyboard_right.png", "keyboard_esc.png", "keyboard_space.png"]
    coordsImg = [[0, 0], [0, -50], [437, 575], [200, 185], [300, 185], [400, 185], [300, 285], [240, 385]]
    listTxt = ["= Moves", "= Pause", "= Drill blocks", "Back"]
    coordsTxt = [[550, 200], [550, 300], [550, 400], [485, 577]]
    for i in range(len(listImg)):
        mySurface.blit(pygame.image.load(listImg[i]), coordsImg[i])
    for i in range(len(listTxt)):
        mySurface.blit(pygame.font.SysFont('Impact', 25).render(listTxt[i], True, WHITE), coordsTxt[i])
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 437 <= x <= 590 and 575 <= y <= 615:
                    return
            pygame.display.update()


def menu():  # Boucle d'affichage et de sélection du menu
    display()
    drillerColor, sound = 0, 0.5
    inProgress = True
    while inProgress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inProgress = leftTheGame()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 490 <= x <= 595 and 245 <= y <= 295:
                    playMenu(drillerColor, sound)
                elif 465 <= x <= 585 and 345 <= y <= 395:
                    drillerColor, sound = options()
                    # drillerColor = skin, sound = volume pour le son du jeu (val entre 0 et 100)
                elif 445 <= x <= 615 and 445 <= y <= 495:
                    howToPlay()
                elif 490 <= x <= 550 and 545 <= y <= 595:
                    inProgress = leftTheGame()
            display()
        pygame.display.update()
    pygame.quit()


menu()
