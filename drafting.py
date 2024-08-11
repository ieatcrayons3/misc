import pygame
from math import sin, cos, floor, sqrt
import serial
import time
from datetime import datetime
from gcodeplot import plotcode
sim = True
Xac = 1800
Yac = Xac
Zac = 1500

xv = 150
yv = 150
zv = 50

ppi = floor(3840 / 60)

zEngagued = 6
zClear = 11
scaleF = 2 * 25.4 / (ppi * 6)

XRES = 3840
YRES = floor(XRES * 9 / 16)
prec = 2

#print(scaleF * XRES / 2)
#quit()

print("PPI: ",ppi)
print("RES:",XRES,"x",YRES)
print("Precision:",1 / (10 ** prec),"mm")
print("Writing Height:",zEngagued)
print("Clearance Height:", zClear)

ds = 1 / sqrt(3)
#quit()
srf = None
minix = 0
miniy = 0


def command(ser, command):
  start_time = datetime.now()
  ser.write(str.encode(command))
  time.sleep(1)

  while False:
    line = ser.readline()
    print(line)

    if line == b'ok\n':
      break
if sim:
    ser = None
    def setupprint():
        pass
    def command(a = 0, b = 0):
        pass
else:
    ser = serial.Serial('COM8', 115200)
#command(ser, "G90\n")
    command(ser, "echo\n")
    def setupprint():
        command(ser, "G0 Z" + str(zClear) + "\n")
        command(ser,"G0 F1500\n")
        command(ser, "G4 P3000\n")
        command(ser, "G90\n")
        command(ser,"G28 X Y Z\n")
        print("Homing...")
        time.sleep(10)
        command(ser,"G0 X0 Y0 Z25\n")
        command(ser, "G4 P1500\n")
        command(ser,"G0 F15000\n")
        command(ser, "M203 " + "X" +str(xv)+ " Y" +str(yv)+ " Z" + str(zv) + "\n")
        command(ser, "M201 " + "X" +str(Xac)+ " Y" +str(Yac)+ " Z" + str(Zac) + "\n")


def linmov(p1,p2,chained=False):
    sy = round(p1[0] * scaleF, prec)
    sx = round(p1[1] * scaleF, prec)
    ey = round(p2[0] * scaleF, prec)
    ex = round(p2[1] * scaleF, prec)
    s = ""
    if not chained:
        s += "G0 Z" + str(zClear) + "\n"
        #s += "G4 P500\n"
        s += "G0 X" + str(sx) + " Y" + str(sy) + "\n"
        s += "G0 Z" + str(zEngagued) + "\n"
    s += "G0 X" + str(ex) + " Y" + str(ey) + "\n"
    #time.sleep(1)
    #print(s)
    return s

def chainMov(linelist):
    movs = ""
    s = (0,0)
    e = None
    cn = False
    for i in linelist:
        s = i[0]
        if s == e:
            cn = True
        else:
            cn = False
        e = i[1]
        movs += linmov(s,e,cn)
    return movs





pygame.init()
pygame.mouse.set_visible(False)
mainDisplay = pygame.display.set_mode((XRES, YRES),pygame.FULLSCREEN)
mainSurf = pygame.Surface((XRES, YRES))
p1 = None
p2 = None
lines = []
undolist = []
mode = 1
glist = ""


while True:
    mainSurf.fill((0,0,0))
    if mode == 1:
        ppi = floor(3840 / 120)
        for x in range(floor(XRES / ppi)):
            for y in range(floor(YRES / ppi)):
                mainSurf.set_at((ppi*x, ppi*y), (255,255,255))
        for i in lines:
            pygame.draw.line(mainSurf,(255,255,255),i[0],i[1],1)
        lines2 = lines
    else:
        ppi = floor(3840 / 120)
        for x in range(floor(XRES / ppi)):
            for y in range(floor(YRES / ppi)):
                dy = floor(ppi * x * ds)
                if (dy + ppi*y - 2*ppi) > YRES:
                    dy -= YRES
                mainSurf.set_at((ppi*x, ppi*y + dy), (255,255,255))
        for i in lines:
            pygame.draw.line(mainSurf,(255,255,255), (i[0][0], floor(i[0][1] + i[0][0] * ds)), (i[1][0], floor(i[1][1] + i[1][0] * ds)), 1)
    #w, h = pygame.display.get_surface().get_size()

    events = pygame.event.get()
    mpos = pygame.mouse.get_pos()
    if mode == 1:
        mpos = (ppi*round(mpos[0] / ppi), ppi*round(mpos[1] / ppi))
        if (mpos[0] < 260 and mpos[1] < 260 and minix == 0):
            minix = 1350
        if (mpos[0] > 1350) and (mpos[1] <  260) and (minix != 0):
            minix = 0
    else:
        pass
        #mpos = (ppi*round(mpos[0] / ppi), round(mpos[0]*ds)+ppi*round(mpos[1] / (ppi*ds)))
    pygame.draw.circle(mainSurf,(255,255,255),mpos,3)
    glist = chainMov(lines2)
    if p1 != None:
        pygame.draw.circle(mainSurf,(255,255,255),p1,2)
        pygame.draw.line(mainSurf,(150,150,150),p1, mpos, 1)
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                #print("h")
                if p1 == None:
                    p1 = mpos
                else:
                    p2 = mpos
                    lines.append((p1,p2))
                    if event.button == 1:
                        p1 = None
                    else:
                        p1 = p2
            if event.button == 2:
                print(glist)
            if event.button == 4:
                if len(undolist) > 0:
                    addon = undolist.pop(-1)
                    lines.append(addon)
            if event.button == 5:
                if len(lines) > 0:
                    remo = lines.pop(-1)
                    undolist.append(remo)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                p1 = None
            if event.key == pygame.K_SPACE:
                    for i in range(1):
                        print("\n")
                    print(glist)
                    setupprint()
                    command(ser, "G0 Z15\n")
                    command(ser, glist)
                    for line in glist.splitlines():
                        command(ser,    line + "\n")
                    command(ser, "G0 Z25\n")
                    command(ser, "G0 Y200\n")
                    miniview = plotcode(glist)
                    srf = pygame.surfarray.make_surface(miniview)

            if event.key == pygame.K_m:
                mode = 1 - mode
            if event.key == pygame.K_q:
                quit()
    if srf != None:
        pygame.Surface.blit(mainSurf, srf, (minix, 0))
    pygame.Surface.blit(mainDisplay,mainSurf,(0,0))
    pygame.display.update()
