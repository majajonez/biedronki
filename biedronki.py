import math
import random

import pygame

pygame.init()

#################
##  CONFIG     ##
#################
szerokosc = 800
wysokosc = 800
debug = False


# seed = random.randrange(sys.maxsize)
seed = 3409909095736502432
print("Seed to " + str(seed))
rng = random.Random(seed)
screen = pygame.display.set_mode((szerokosc, wysokosc))

pygame.display.set_caption("gra w biedronki")


class Biedronka():
    def __init__(self):
        self.szer = 13
        self.wys = 13
        self.x = rng.randint(0, 800 - self.szer)
        self.y = rng.randint(0, 800 - self.wys)
        self.vx = rng.randint(-2, 2)
        self.vy = rng.randint(-2, 2)
        self.ksztalt = pygame.Rect(self.x, self.y, self.szer, self.wys)
        self.grafika = pygame.image.load("biedronka.png")

    def rysuj(self):
        screen.blit(self.grafika, (self.x - self.szer/2, self.y - self.wys/2))
        if debug:
            pygame.draw.rect(screen, (255,0,0) ,self.ksztalt, 2)

    def ruch(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        if self.x <= 0:
            self.vx = abs(self.vx)
        if self.x >= szerokosc - self.szer:
            self.vx = abs(self.vx) * (-1)
        if self.y <= 0:
            self.vy = abs(self.vy)
        if self.y >= wysokosc - self.wys:
            self.vy = abs(self.vy) * (- 1)
        self.ksztalt = pygame.Rect(self.x, self.y, self.szer, self.wys)

    def kolizja(self, player):
        czyKolizja = self.ksztalt.colliderect(player.ksztalt)
        return czyKolizja

    def odleglosc(self, p):
        a1 = p.x - self.x
        a2 = p.y - self.y
        a3 = math.sqrt((a1 ** 2) + (a2 ** 2))
        return a3

    def zawroc(self):
        self.vx = self.vx * (-1)
        self.vy = self.vy * (-1)


class Gracz():
    def __init__(self):
        self.x = 400
        self.y = 400
        self.szer = 10
        self.wys = 10
        self.kolor = (0, 0, 255)
        self.ksztalt = pygame.Rect(self.x, self.y, self.szer, self.wys)

    def rysuj(self):
        pygame.draw.rect(screen, self.kolor, self.ksztalt, 0)

    def ruch(self, vx, vy):
        self.x = self.x + vx
        self.y = self.y + vy
        self.ksztalt = pygame.Rect(self.x, self.y, self.szer, self.wys)



def napis(tekst, x, y, rozmiar, color=(255, 255, 255)):
    czcionka = pygame.font.SysFont("Arial", rozmiar)
    rend = czcionka.render(tekst, True, color)
    screen.blit(rend, (x, y))


ekran = "menu"
gracz = Gracz()
player = gracz
biedronki = []

def mnozenie_biedronek():
    for i in range(20):
        generowanie_biedronki()


def generowanie_biedronki():
    biedronka = Biedronka()
    while biedronka.odleglosc(gracz) <= 50:
        biedronka = Biedronka()
    for j in biedronki:
        while j.odleglosc(biedronka) <= 40 or biedronka.odleglosc(gracz) <= 50:
            biedronka = Biedronka()
    biedronki.append(biedronka)

def wyniki(nowy_wynik):
    lista_wynikow = open("wyniki_biedronki.pg")
    lista = lista_wynikow.readlines()
    lista_wynikow.close()
    print(lista)
    lista.append(nowy_wynik)
    najlepsze = [int(i) for i in lista]
    najlepsze.sort(reverse=True)
    lista_do_zapisu = [str(i) + '\n' for i in najlepsze]
    lista_wynikow = open("wyniki_biedronki.pg", "w")
    lista_wynikow.writelines(lista_do_zapisu)
    print(lista_do_zapisu)
    lista_wynikow.close()
    print(najlepsze)

def lista_wynikow():
    lista_wynikow = open("wyniki_biedronki.pg")
    lista = lista_wynikow.readlines()
    lista_wynikow.close()
    y = 50
    for i in lista:
        j = i.strip()
        napis(j, 50, y, 20)
        y += 20
    print(lista)



class Button():
    def __init__(self, tekst, x, y):
        self.guzik = pygame.Rect(x, y, 300, 80)
        czcionka = pygame.font.SysFont("Arial", 30)
        self.napis = czcionka.render(tekst, True, (255, 255, 255))

    def rysuj_button(self, color, ramka):
        pygame.draw.rect(screen, color, self.guzik, ramka)
        screen.blit(self.napis, self.guzik)

button_color = (255, 51, 51)
klikniety = (255, 153, 153)

guziki = [
    Button("najlepsze wyniki", 250, 300),
    Button("instrukcja", 250, 400)
    ]

# lista_wynikow = open("wyniki_biedronki.pg", "w")
# lista_wynikow.write(str("456"))
# lista_wynikow.close()


licznik_obrotow = 0

# mnozenie_biedronek()
ktory_guzik = 0

run = True
v = 2
mnozenie_biedronek()
while run:
    dx = 0
    dy = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if ekran != "rozgrywka":
                    gracz.rysuj()
                    ekran = "rozgrywka"
                    biedronki.clear()
            if event.key == pygame.K_ESCAPE:
                if ekran != "menu":
                    biedronki.clear()
                    ekran = "menu"
                    mnozenie_biedronek()
            if event.key == pygame.K_DOWN:
                if ekran == "menu":
                    if ktory_guzik < 1:
                        ktory_guzik += 1
            if event.key == pygame.K_UP:
                if ekran == "menu":
                    if ktory_guzik > 0:
                        ktory_guzik -= 1
            if event.key == pygame.K_RETURN:
                if ekran == "menu":
                    if ktory_guzik == 0:
                        ekran = "wyniki"
                    elif ktory_guzik == 1:
                        ekran = "instrukcja"

    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_UP]:
        dy = -v
    if keys[pygame.K_DOWN]:
        dy = +v
    if keys[pygame.K_LEFT]:
        dx = -v
    if keys[pygame.K_RIGHT]:
        dx = +v


    screen.fill((0, 0, 0))

    if ekran == "menu":
        napis("Mordercze biedronki", 200, 100, 40)
        for i in range(len(guziki)):
            if i == ktory_guzik:
                guziki[i].rysuj_button(klikniety, 0)
            else:
                guziki[i].rysuj_button(button_color, 4)
        napis("Aby zagrać, naciśnij spację", 170, 600, 40)
        for b in biedronki:
            b.ruch()
            b.rysuj()
    elif ekran == "wyniki":
        lista_wynikow()
    elif ekran == "instrukcja":
        instrukcja = open("instrukcja biedronek", encoding='utf8')
        pokaz_instrukcje = instrukcja.readlines()
        instrukcja.close()
        y = 50
        for i in pokaz_instrukcje:
            j = i.strip()
            napis(j, 50, y, 20)
            y += 40
    elif ekran == "rozgrywka":
        punkty = licznik_obrotow / 10
        if licznik_obrotow % 20 == 0:
            generowanie_biedronki()
        licznik_obrotow +=1
        gracz.rysuj()
        gracz.ruch(dx, dy)
        for b in biedronki:
            b.ruch()
            b.rysuj()
            if b.kolizja(gracz):
                ekran = "koniec"
                biedronki.clear()
                mnozenie_biedronek()
                gracz = Gracz()
                wyniki(punkty)
            for dronka in biedronki:
                if b != dronka:
                    if b.kolizja(dronka):
                        b.zawroc()
                        dronka.zawroc()
                        b.ruch()
        napis(str(punkty), 20, 20, 20, (179, 198, 255))
    elif ekran == "koniec":
        napis("GAME OVER", 50, 300, 20)
        napis(("Liczba punktów: " + str(punkty)), 50, 400, 20)
        napis("Naciśnij spację, aby zagrać jeszcze raz", 50, 500, 20)
        biedronki.clear()
        licznik_obrotow = 0


    pygame.display.update()
    pygame.time.wait(10)

