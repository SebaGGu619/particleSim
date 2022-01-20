import pygame
import time
import math
import random

pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()
particleNum = 50
particlePos = [[0 for i in range(5)] for j in range(50)]
flagSpin = False
flagAttract = False
flagRepel = False
xClick, yClick = 0, 0

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
    particlePos[i][2] = random.randint(1, 369)
    particlePos[i][3] = 0.2
    particlePos[i][4] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def generate_particle():
    particlePos = [random.randint(1, 1399), random.randint(1, 799), random.randint(1, 369), 0.2, (random.randint(0, 255),
                                                                                                 random.randint(0, 255),
                                                                                                 random.randint(0,
                                                                                                                255))]
    return particlePos


running = True
while running:
    a = current_milli_time()
    elapsedMillis = current_milli_time() - a
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
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
            if event.key == pygame.K_h:
                flagSpin = True
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

    # todo aici tool maus jucarie gen chestie manevra blana bombao
    # todo amundoua sunt cam belite ajutor

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

            diferenta = math.acos((d12 ** 2 + 1 - d23 ** 2) / (2 * d12 * d13))

            if xClick < particlePos[i][0] and yClick < particlePos[i][1]:
                diferenta = normalize_angle(-math.degrees(diferenta) - particlePos[i][2])
                diferenta = diferenta
            else:
                diferenta = normalize_angle(math.degrees(diferenta) - particlePos[i][2])
                diferenta = diferenta

            particlePos[i][2] = normalize_angle(particlePos[i][2] + diferenta / 2)

    if flagRepel:
        for i in range(len(particlePos)):
            xClick, yClick = pygame.mouse.get_pos()

            pct1 = (particlePos[i][0], particlePos[i][1])
            pct2 = (xClick, yClick)
            pct3 = (particlePos[i][0] + 1, particlePos[i][1])

            d12 = math.sqrt((pct1[0] - pct2[0]) ** 2 + (pct1[1] - pct2[1]) ** 2)
            d13 = 1
            d23 = math.sqrt((pct2[0] - pct3[0]) ** 2 + (pct2[1] - pct3[1]) ** 2)

            diferenta = math.acos((d12 ** 2 + 1 - d23 ** 2) / (2 * d12 * d13))

            if xClick < particlePos[i][0] and yClick < particlePos[i][1]:
                diferenta = normalize_angle(-math.degrees(diferenta-180) - particlePos[i][2])
                diferenta = diferenta
            else:
                diferenta = normalize_angle(math.degrees(diferenta-180) - particlePos[i][2])
                diferenta = diferenta

            particlePos[i][2] = normalize_angle(particlePos[i][2] + diferenta / 2)

    while particleNum > len(particlePos):
        particlePos.append(generate_particle())
    while particleNum < len(particlePos):
        particlePos.pop()

    screen.fill((50, 50, 50))

    for i in range(len(particlePos)):
        # todo slingshot cu mausul gen click trage si apoi lanseaza in directia aia
        # coliziune cu pretii
        # todo idk inca e belit ceva trebuie vazut

        if particlePos[i][0] > 1400 and particlePos[i][2] == 0:
            particlePos[i][2] = 181
        elif particlePos[i][0] < 0 and particlePos[i][2] == 180:
            particlePos[i][2] = 1
        elif particlePos[i][1] > 800 and particlePos[i][2] == 90:
            particlePos[i][2] = 271
        elif particlePos[i][1] < 0 and particlePos[i][2] == 270:
            particlePos[i][2] = 91

        elif particlePos[i][0] < 0 and 90 < particlePos[i][2] < 270:
            unghiImpact = 180 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))

        elif particlePos[i][0] > 1400 and 270 < particlePos[i][2] < 360:
            unghiImpact = 180 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))
        elif particlePos[i][0] > 1400 and 0 < particlePos[i][2] < 90:
            unghiImpact = 180 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))

        elif particlePos[i][1] > 800 and 0 < particlePos[i][2] < 180:
            unghiImpact = 360 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))

        elif particlePos[i][1] < 0 and 180 < particlePos[i][2] < 360:
            unghiImpact = 360 - particlePos[i][2]
            particlePos[i][2] = normalize_angle(unghiImpact + random.randint(0, 5))

        distantaParcursaX = particlePos[i][3] * 60

        particlePos[i][3] = particlePos[i][3] - particlePos[i][3] / 100
        particlePos[i][0] = particlePos[i][0] + distantaParcursaX * math.cos(math.radians(particlePos[i][2]))
        particlePos[i][1] = particlePos[i][1] + distantaParcursaX * math.sin(math.radians(particlePos[i][2]))

    for i in range(len(particlePos)):
        draw_particle(particlePos[i][0], particlePos[i][1], i)

    elapsedMillis = current_milli_time() - a
    if 16 > elapsedMillis > 0:
        time.sleep((16 - elapsedMillis) / 1000)
    elapsedMillis = current_milli_time() - a
    if elapsedMillis != 0:
        totalText = set_text("FPS: ", 1340, 14, 20)
        screen.blit(totalText[0], totalText[1])
        totalText = set_text(str(round(1000 / elapsedMillis)), 1380, 14, 20)
        screen.blit(totalText[0], totalText[1])
    totalText = set_text("Particle Number: " + str(particleNum), 700, 14, 20)
    screen.blit(totalText[0], totalText[1])
    pygame.display.update()

pygame.quit()
exit(0)
