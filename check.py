from world import world,pointM,lineM
from tkinter import *

def updateCheck(matCheck,my_world,canvas, listenPo, cObjRemoovable):
    while len(cObjRemoovable)>0:
        currCa = cObjRemoovable.pop()
        canvas.delete(currCa)
        
    
    currPo = my_world.pointList[listenPo]
    currX, currXint  = currPo.x, int(currPo.x)
    currY, currYint  = currPo.y, int(currPo.y)
    print('x='+str(currX)+' y='+str(currY))
    linesList = []
    for x in range(len(matCheck)): 
        for y in range(len(matCheck[x])):
            currXmat = currXint + x -int(400/20/2)
            currYmat = currYint + y -int(300/20/2)
            if currXmat<0 or currYmat<0 or currXmat>=my_world.x_size or currYmat>=my_world.y_size:
                continue
            if len(my_world.mat[currXmat][currYmat])>0:
                canvas.itemconfig(matCheck[x][y], fill="#F3DDFA")
            else:
                canvas.itemconfig(matCheck[x][y], fill="#F3FAFA")
            for li in my_world.mat[currXmat][currYmat]:
                if not li in linesList:
                    linesList.append(li)
    for li in linesList:
        cObjRemoovable.append(canvas.create_line(my_world.x_size-400+(li.x1-currXint)*20+int(400/2),
                                                 (li.y1-currYint)*20+int(140),
                                                 my_world.x_size-400+(li.x2-currXint)*20+int(400/2),
                                                 (li.y2-currYint)*20+int(140),
                                                 fill="#111111"))

    cObjRemoovable.append(canvas.create_line(    my_world.x_size-400+int(400/2)+(currX-currXint)*20,
                                                 int(140)+(currY-currYint)*20,
                                                 my_world.x_size-400+int(400/2)+int(currPo.speedX*40)+(currX-currXint)*20,
                                                 int(140)+int(currPo.speedY*40)+(currY-currYint)*20,
                                                 fill="#FF0100"))               
##    print('ok')
    
    
    
