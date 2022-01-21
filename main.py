import pygame
import time
import math
import random

pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()
particleNum = 200
particlePos = [[0 for i in range(5)] for j in range(50)]
flagSpin = False
flagAttract = False
flagRepel = False
flagInertie = False
xClick, yClick = 0, 0
unghiJucarieK = 0


def set_text(string, coordx, coordy, fontSize):
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    text = font.render(string, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (coordx, coordy)
    return text, textRect


def normalize_angle(alpha):
    if alpha > 360:
        return alpha - 360
    else:
        if alpha < 0:
            return alpha + 360
        else:
            return alpha


def current_milli_time():
    return round(time.time() * 1000)


def draw_particle(x, y, i):
    pygame.draw.circle(screen, particlePos[i][4], (x, y), 5)


for i in range(len(particlePos)):
    particlePos[i][0] = random.randint(1, 1399)
    particlePos[i][1] = random.randint(1, 799)
    particlePos[i][2] = random.randint(1, 350)
    particlePos[i][3] = 0.2
    particlePos[i][4] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def generate_particle():
    particlePos1 = [random.randint(1, 1399),
                    random.randint(1, 799),
                    random.randint(1, 350),
                    0.1, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))]
    return particlePos1


running = True
while running:
    a = current_milli_time()
    elapsedMillis = current_milli_time() - a
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                flagSpin = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                particleNum = particleNum + 1
            if event.key == pygame.K_q:
                particleNum = 0
            if event.key == pygame.K_s and particleNum > 0:
                particleNum = particleNum - 1
            if event.key == pygame.K_e:
                particleNum = particleNum + 10
            if event.key == pygame.K_d and particleNum - 9 > 0:
                particleNum = particleNum - 10
            if event.key == pygame.K_r:
                particleNum = particleNum + 100
            if event.key == pygame.K_f and particleNum - 99 > 0:
                particleNum = particleNum - 100
            if event.key == pygame.K_a:
                for i in range(len(particlePos)):
                    particlePos[i][3] = particlePos[i][3] + 0.2
            if event.key == pygame.K_z:
                for i in range(len(particlePos)):
                    particlePos[i][3] = particlePos[i][3] / 2
            if event.key == pygame.K_j:
                flagSpin = True
            if event.key == pygame.K_u:
                if flagInertie:
                    flagInertie = False
                else:
                    flagInertie = True
            if event.key == pygame.K_k:
                for i in range(len(particlePos)):
                    particlePos[i][2] = unghiJucarieK
                unghiJucarieK = normalize_angle(unghiJucarieK + 90)
            if event.key == pygame.K_l:
                for i in range(len(particlePos)):
                    particlePos[i][3] = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                flagAttract = True
            if event.button == 3:
                flagRepel = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                flagAttract = False
            if event.button == 3:
                flagRepel = False

    if flagSpin:
        for i in range(len(particlePos)):
            particlePos[i][2] = normalize_angle(particlePos[i][2] + 20)

    # todo slingshot cu mausul gen click trage si apoi lanseaza in directia aia
    # todo culori si marimi particule si fundal

    # jucarie maus
    if flagAttract:
        for i in range(len(particlePos)):
            xClick, yClick = pygame.mouse.get_pos()

            pct1 = (particlePos[i][0], particlePos[i][1])
            pct2 = (xClick, yClick)
            pct3 = (particlePos[i][0] + 1, particlePos[i][1])

            d12 = math.sqrt((pct1[0] - pct2[0]) ** 2 + (pct1[1] - pct2[1]) ** 2)
            d13 = 1
            d23 = math.sqrt((pct2[0] - pct3[0]) ** 2 + (pct2[1] - pct3[1]) ** 2)

            tempCalcul = (d12 ** 2 + 1 - d23 ** 2) / (2 * d12 * d13)

            try:
                diferenta = math.acos((d12 ** 2 + 1 - d23 ** 2) / (2 * d12 * d13))
            except:
                print("Programul a intampinat o erroare dar nu a fost oprit.")
                print("Eroare Non-Fatala.")
                print("Eroarea se poate vedea mai jos.")
                print(Exception)

            if yClick < particlePos[i][1]:
                diferenta = normalize_angle(-math.degrees(diferenta) - particlePos[i][2] + random.randint(0, 5))
                if diferenta > 180:
                    diferenta = diferenta - 360
            else:
                diferenta = normalize_angle(math.degrees(diferenta) - particlePos[i][2] + random.randint(0, 5))
                if diferenta > 180:
                    diferenta = diferenta - 360

            viteza = 1 / d12
            if viteza > 0.5:
                viteza = 0.5
            particlePos[i][3] = particlePos[i][3] + viteza
            particlePos[i][2] = normalize_angle(particlePos[i][2] + diferenta / 6)

    if flagRepel:
        for i in range(len(particlePos)):
            xClick, yClick = pygame.mouse.get_pos()

            pct1 = (particlePos[i][0], particlePos[i][1])
            pct2 = (xClick, yClick)
            pct3 = (particlePos[i][0] + 1, particlePos[i][1])

            d12 = math.sqrt((pct1[0] - pct2[0]) ** 2 + (pct1[1] - pct2[1]) ** 2)
            d13 = 1
            d23 = math.sqrt((pct2[0] - pct3[0]) ** 2 + (pct2[1] - pct3[1]) ** 2)

            try:
                diferenta = math.acos((d12 ** 2 + 1 - d23 ** 2) / (2 * d12 * d13))
            except:
                print("Programul a intampinat o erroare dar nu a fost oprit.")
                print("Eroare Non-Fatala.")
                print("Eroarea se poate vedea mai jos.")
                print(Exception)

            if yClick < particlePos[i][1]:
                diferenta = normalize_angle(math.degrees(diferenta) - particlePos[i][2] + random.randint(0, 5))
                if diferenta > 180:
                    diferenta = diferenta - 360
            else:
                diferenta = normalize_angle(-math.degrees(diferenta) - particlePos[i][2] + random.randint(0, 5))
                if diferenta > 180:
                    diferenta = diferenta - 360

            viteza = 1 / d12
            if viteza > 1:
                viteza = 1
            particlePos[i][3] = particlePos[i][3] + viteza
            particlePos[i][2] = normalize_angle(particlePos[i][2] + diferenta / 6)

    while particleNum > len(particlePos):
        particlePos.append(generate_particle())
    while particleNum < len(particlePos):
        particlePos.pop()

    screen.fill((50, 50, 50))

    for i in range(len(particlePos)):
        # coliziune cu pretii
        if particlePos[i][0] > 1600 or particlePos[i][1] > 1000 or particlePos[i][0] < -200 or particlePos[i][1] < -200:
            print(i)
            print(particlePos[i][0])
            print(particlePos[i][1])
            print(particlePos[i][2])
            print(particlePos[i][3])
            print()

        bounceXmax = 1400
        bounceXmin = 0
        bounceYmax = 800
        bounceYmin = 0

        if particlePos[i][0] < -200 or particlePos[i][0] > 1600 or particlePos[i][1] < -200 or particlePos[i][1] > 1000:
            particlePos[i][3] = 1

        if particlePos[i][0] > bounceXmax and (particlePos[i][2] == 0 or particlePos[i][2] == 360):
            particlePos[i][2] = 181
        elif particlePos[i][0] < bounceXmin and particlePos[i][2] == 180:
            particlePos[i][2] = 1
        elif particlePos[i][1] > bounceYmax and particlePos[i][2] == 90:
            particlePos[i][2] = 271
        elif particlePos[i][1] < bounceYmin and particlePos[i][2] == 270:
            particlePos[i][2] = 91

        elif particlePos[i][0] < bounceXmin and 90 < particlePos[i][2] < 270:
            unghiImpact = 180 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))

        elif particlePos[i][0] > bounceXmax and 270 < particlePos[i][2] < 360:
            unghiImpact = 180 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))
        elif particlePos[i][0] > bounceXmax and 0 < particlePos[i][2] < 90:
            unghiImpact = 180 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))

        elif particlePos[i][1] > bounceYmax and 0 < particlePos[i][2] < 180:
            unghiImpact = 360 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))

        elif particlePos[i][1] < bounceYmin and 180 < particlePos[i][2] < 360:
            unghiImpact = 360 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))

        distantaParcursaX = particlePos[i][3] * 60

        if not flagInertie:
            particlePos[i][3] = particlePos[i][3] - particlePos[i][3] / 100
        particlePos[i][0] = particlePos[i][0] + distantaParcursaX * math.cos(math.radians(particlePos[i][2]))
        particlePos[i][1] = particlePos[i][1] + distantaParcursaX * math.sin(math.radians(particlePos[i][2]))

    for i in range(len(particlePos)):
        draw_particle(particlePos[i][0], particlePos[i][1], i)

    elapsedMillis = current_milli_time() - a
    if 16 > elapsedMillis >= 0:
        time.sleep((16 - elapsedMillis) / 1000)
    elapsedMillis = current_milli_time() - a
    if elapsedMillis != 0:
        totalText = set_text("FPS:", 1370, 14, 20)
        screen.blit(totalText[0], totalText[1])
        totalText = set_text(str(round(1000 / elapsedMillis)), 1370, 38, 20)
        screen.blit(totalText[0], totalText[1])

    totalText = set_text("Numar de particule:", 930, 14, 20)
    screen.blit(totalText[0], totalText[1])
    totalText = set_text(str(particleNum), 930, 38, 20)
    screen.blit(totalText[0], totalText[1])

    totalText = set_text("Forta de frecare:", 90, 14, 20)
    screen.blit(totalText[0], totalText[1])
    if flagInertie:
        textInertie = "Oprita"
    else:
        textInertie = "Pornita"
    totalText = set_text(textInertie, 90, 38, 20)
    screen.blit(totalText[0], totalText[1])


    directieK = "Error"
    if unghiJucarieK == 0 or unghiJucarieK == 360:
        directieK = "Dreapta"
    if unghiJucarieK == 90:
        directieK = "Jos"
    if unghiJucarieK == 180:
        directieK = "Stanga"
    if unghiJucarieK == 270:
        directieK = "Sus"
    totalText = set_text("K Urmatoarea Directie:", 1195, 14, 20)
    screen.blit(totalText[0], totalText[1])
    totalText = set_text(directieK, 1195, 38, 20)
    screen.blit(totalText[0], totalText[1])

    totalText = set_text("Culoare Particule: ", 295, 14, 20)
    screen.blit(totalText[0], totalText[1])
    totalText = set_text("Multi-Color", 295, 38, 20)
    screen.blit(totalText[0], totalText[1])

    totalText = set_text("Culoare Fundal: ", 500, 14, 20)
    screen.blit(totalText[0], totalText[1])
    totalText = set_text("Gri", 500, 38, 20)
    screen.blit(totalText[0], totalText[1])

    totalText = set_text("Marime Particule: ", 700, 14, 20)
    screen.blit(totalText[0], totalText[1])
    totalText = set_text("5", 700, 38, 20)
    screen.blit(totalText[0], totalText[1])

    pygame.display.update()
pygame.quit()
exit(0)
