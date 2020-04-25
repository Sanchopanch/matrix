import pickle
import os
from tkinter import *
import time



class moove():
    def __init__(self):
        self.points = []
        self.lines = []
        self.pause = 0
if __name__ == "__main__":
    fileNameOfJob = 'mov_1.pkl'
    if(not os.path.exists( fileNameOfJob)): 
        pass    
    with open(fileNameOfJob,'rb') as f:
        currMoove =pickle.load(f)
    print(' loaded moove with %i cadrs'%len(currMoove))


    root = Tk()
    canvas = Canvas(root, width=600+3, height=700+3)
    canvas.pack()
    canvas.create_rectangle(0, 0, 600+2, 700+2, fill="white")
    cAlin=[]
    cApo=[]
    firstCadr =currMoove[0] 
    for lin in firstCadr.lines:
        cA = canvas.create_line(lin[0], lin[1], lin[2], lin[3],  fill="#555555", width = lin[4])
        cAlin.append(cA)
    for po in firstCadr.points:
        cA = canvas.create_oval(po[0]-po[2], po[1]-po[2],po[0]+po[2],po[1]+po[2], fill="#FF5555")    
        cApo.append(cA)
        
    for i,cadr in enumerate(currMoove):
        currTime=time.time()
        for lin in range( len(cadr.lines)):
            if not cadr.lines[lin][5]:
                canvas.coords(cAlin[lin], cadr.lines[lin][0], cadr.lines[lin][1], cadr.lines[lin][2], cadr.lines[lin][3])
            else:
                canvas.coords(cAlin[lin], 0, 0, 0, 1)    
        for po in range( len(cadr.points)):
            large = cadr.points[po][2]
            canvas.coords(cApo[po], cadr.points[po][0]-large, cadr.points[po][1]-large,cadr.points[po][0]+large, cadr.points[po][1]+large)
        root.update()


        time.sleep(1/250)

    root.destroy()








        
        
