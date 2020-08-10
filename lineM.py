from tkinter import *
import numpy as np
import math
import time
import pickle
from moove import moove
import random


from world import world,pointM,lineM
from check import updateCheck


my_world = world( 1000,700, gravity=0.7 )

##check**************************************
checking = False

##my_world.appendTri(230+(20),430+(20),    230+(20+20),430+(20)   , 230+(20),   440+(20))
for i in range(15):
    for ii in range(1):
        my_world.appendTri(100+(i*20),530+(ii*20),    100+(i*20+20),530+(ii*20)   , 100+(i*20),530+(20)+(ii*20))
        my_world.appendTri(100+(i*20),530+20+(ii*20), 100+(i*20+20),530+20+(ii*20), 100+(i*20+20),530+(ii*20))
my_world.pointList[0].moovable = False
my_world.pointList[len(my_world.pointList)-1].moovable = False

##my_world.appendTri(130+(20),560+(20),    130+(20+20),640+(20)   , 330+(20),   530+(20)+(20))
for i in range(3):
    for ii in range(2):
        my_world.appendTri(230+(i*20),430+(ii*20),    230+(i*20+20),430+(ii*20)   , 230+(i*20),   430+(20)+(ii*20))
        my_world.appendTri(230+(i*20),430+20+(ii*20), 230+(i*20+20),430+20+(ii*20), 230+(i*20+20),430+(ii*20))


##my_world.appendTri(250,490, 400,450, 400,520)
##my_world.pointList[4].moovable = False
##my_world.pointList[5].moovable = False
##
##my_world.appendTri(200,490, 200,550, 280,620)
##my_world.pointList[7].moovable = False
##my_world.pointList[8].moovable = False





root = Tk()
canvas = Canvas(root, width=my_world.x_size+3, height=my_world.y_size+3)
canvas.pack()
canvas.create_rectangle(0, 0, my_world.x_size+3, my_world.y_size+3, fill="white")

##check**************************************
matCheck, listenPo, cObjRemoovable = [],3,[]
if checking:
    canvas.create_rectangle(my_world.x_size-400, 0, my_world.x_size+3, 300, fill="#F2F2F2",width=0)
    for i in range(int(400/20)):
        newList = []
        for ii in range(int(300/20)):
            newList.append(canvas.create_rectangle(my_world.x_size-400+i*20,
                                                   ii*20,my_world.x_size-400+(i+1)*20, (ii+1)*20, width=0))
        matCheck.append(newList)
    updateCheck(matCheck,my_world,canvas, listenPo,cObjRemoovable)
#end of check****************************


for lin in my_world.linesList:
    lin.cA = canvas.create_line(lin.x1, lin.y1,lin.x2, lin.y2,  fill="#999999",width=int(lin.granze1))
for po in my_world.pointList:
    po.cA  = canvas.create_oval(po.x-po.large, po.y-po.large,po.x+po.large, po.y+po.large, fill="#FF5555")
    po.cAx = canvas.create_line(po.x, po.y,po.x+1, po.y,  fill="#000000")
    po.cAy = canvas.create_line(po.x, po.y,po.x, po.y+1,  fill="#111100")

canvas_idText = canvas.create_text(25, 10, text="kadr")
cadrs = []
currTime = 0.0
currKoeff = 3.0
nom =0
while True:
    my_world.calcSchnelligkeit(currKoeff)

    currKoeff = my_world.calcSpeedKoeff()
    my_world.calcSpeeds(currKoeff)
    currKoeff = my_world.calcSpeedKoeff()
    # M O V E !
    allOK = my_world.move(currKoeff)
    # =======
    my_world.brokeLines()
    nom=nom+1
    print('turn %i koeff = %f '%(nom,currKoeff))

    currPoints = []
    currLines = []
    if currKoeff>0:
        currTime +=  1 / currKoeff
    for lin in my_world.linesList:
        if lin.broken:
            canvas.coords(lin.cA, 0, 0, 0, 0)
        else:
            canvas.coords(lin.cA, int(lin.x1), int(lin.y1), int(lin.x2), int(lin.y2))
        canvas.itemconfig(lin.cA, fill=lin.color)
    for po in my_world.pointList:
        canvas.coords(po.cA, int(po.x)-po.large, int(po.y)-po.large,int(po.x)+po.large, int(po.y)+po.large)
        canvas.coords(po.cAx, int(po.x), int(po.y),int(po.x)+int(po.speedX*4), int(po.y))
        canvas.coords(po.cAy, int(po.x), int(po.y),int(po.x), int(po.y)+int(po.speedY*4))
        
    if checking: updateCheck(matCheck,my_world,canvas, listenPo,cObjRemoovable)
#end of check****************************
    
    if not allOK:
        time.sleep(1)
    else:
        pass #time.sleep(.1)


    
    if currTime>=1/5:
        for lin in my_world.linesList:
            currLines.append([ int(lin.x1), int(lin.y1), int(lin.x2), int(lin.y2), int(lin.granze1),lin.broken] )

##        while len(cObjRemoovable)>0:
##            currCa = cObjRemoovable.pop()
##            canvas.delete(currCa)
##        for xx in range(len(my_world.mat)):
##            for yy in range(len(my_world.mat[xx])):
##                currList = my_world.mat[xx][yy]
##                if len(currList)>0:
##                    cObjRemoovable.append(canvas.create_line(xx, yy, xx+1, yy, fill="#666666"))

        for po in my_world.pointList:
            currPoints.append([int(po.x),int(po.y),po.large])

        cadr = moove()
        cadr.points=currPoints
        cadr.lines=currLines
        cadr.pause = 1 / currKoeff
        cadrs.append(cadr)
        currTime=0.0
        if len(cadrs) >=520:
            fileName='mov_1.pkl'
            with open(fileName,'wb') as f:
                pickle.dump(cadrs, f)
            break
            
    canvas.itemconfig(canvas_idText, text=str(len(cadrs))) 

    root.update()
    
    #time.sleep(0.01)

root.destroy()
