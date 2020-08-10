import math
def renerateXYline(x1,y1,x2,y2):
    length = int(math.sqrt((x1-x2)**2+(y1-y2)**2))
    length = 1 if length < 1 else length
    
    steepsInt = int(length*4)
    steepX = (x2-x1)/steepsInt 
    steepY = (y2-y1)/steepsInt 
    currList = []
    for aaa in range(steepsInt+1):
        prevX = currX if aaa>0 else -1
        prevY = currY if aaa>0 else -1
        currXf = x1 + aaa * steepX 
        currYf = y1 + aaa * steepY
        currX = int(currXf)
        currY = int(currYf)
        if (prevX-currX == 1 and prevY-currY == 1) or (prevX-currX == -1 and prevY-currY == 1):
            currList.append([currX,currY+1])
            yield (currX,currY+1,currXf,currYf)
        elif (prevX-currX == -1 and prevY-currY == -1) or (prevX-currX == 1 and prevY-currY == -1):
            currList.append([currX,currY-1])
            yield (currX,currY-1,currXf,currYf)
        if not [currX,currY] in currList:
            currList.append([currX,currY])
            yield (currX,currY,currXf,currYf)
    if not [int(x2),int(y2)] in currList:
        yield (int(x2),int(y2),x2,y2)    
if __name__ == "__main__":
    for x,y,xf,yf in renerateXYline(1.2,1.1,9.0,6.9):
        print (x,y,xf,yf)
