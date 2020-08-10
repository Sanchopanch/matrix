import math
from genXY import renerateXYline
class pointM():
    def __init__(self,x,y,mass, moovable = True):
        self.x = x
        self.y = y
        self.mass = mass
        self.speedX = 0.0
        self.speedY = 0.0
        self.moovable = moovable
        self.large = int(self.mass)
        self.cA = 0
        self.cAx = 0
        self.cAy = 0
        self.accX = 0.0
        self.accY = 0.0
        self.accX1 = 0.0
        self.accY1 = 0.0
        self.color="#FF5555"

class lineM():
    def __init__(self,x1,y1,x2,y2,m1=2.0,m2=2.0,granze1=1.4,granze2=0.6,
                 steifheit=15.5, moovable1=True, moovable2=True):
        self.steifheit = steifheit
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.broken = False
        self.lange = math.sqrt( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )
        self.m1 = m1
        self.m2 = m2
        self.granze1 = granze1
        self.granze2 = granze2
        self.cA=0
        self.moovable1=moovable1
        self.moovable2=moovable2
        self.color="#999999"

    def calcForces(self,numP):
        if self.broken:
            return 0.0,0.0
        currLange = math.sqrt( (self.x1-self.x2)*(self.x1-self.x2) + (self.y1-self.y2)*(self.y1-self.y2) )
        if numP == 1:
            cos = (self.x1 - self.x2) / currLange
            sin = (self.y1 - self.y2) / currLange
            massKoeff = self.point2.mass / self.point1.mass
            forsX = cos * massKoeff *(self.lange-currLange) * self.steifheit
            forsY = sin * massKoeff *(self.lange-currLange) * self.steifheit
        elif numP == 2:
            cos = (self.x2 - self.x1) / currLange
            sin = (self.y2 - self.y1) / currLange
            massKoeff = self.point1.mass / self.point2.mass
            forsX =  cos * massKoeff * (self.lange-currLange) * self.steifheit
            forsY =  sin * massKoeff * (self.lange-currLange) * self.steifheit
        return  forsX, forsY

    def calcSignNormX(self,x,y,xNor = True):
        if (self.x2 - self.x1)==0:
            if xNor:
                rez = 1 if  x >= self.x1 else -1
            else:
                rez = 0 #???    
        else:                                                         # y = kx + b
            k =           (self.y2 - self.y1) / (self.x2 - self.x1)   # y = mx + k
            b = self.y1 - self.x1 * (self.y2 - self.y1) / (self.x2 - self.x1) 
            if xNor:
                xN =     (x + k*y - k*b) / (k**2 +1)
                rez = 1 if  x >= xN else -1
            else:
                lineX1,lineX2,lineY1,lineY2 = self.x1,self.x2,self.y1,self.y2
                yN = b + k*(x + k*y - k*b) / (k**2 +1)
                rez = 1 if  y >= yN else -1
        return rez
        
        
class world():
    def __init__(self,x_size,y_size , gravity = 0.07, resistance = 0.1):
        self.lines = []
        self.x_size = x_size
        self.y_size = y_size
        self.gravity = gravity
        self.mat=[]
        for xx in range(x_size):
            nl=[]
            for yy in range(y_size):
                nl.append([])
            self.mat.append(nl)
        #self.mat = [[[]]*x_size]*y_size
        self.pointList = []        
        self.linesList = []
        self.cA=0
        self.resistance = resistance

    def appendLine(self,line):
        for li in self.linesList:
            if li.x2==line.x2 and li.y2==line.y2:
                if li.x1==line.x1 and li.y1==line.y1:
                    return
            if li.x1==line.x2 and li.y1==line.y2:
                if li.x2==line.x1 and li.y2==line.y1:
                    return
        
        p1 = None
        p2 = None
        for p in self.pointList:
            if p.x==line.x1 and p.y==line.y1:
                p1=p
                break
        for p in self.pointList:
            if p.x==line.x2 and p.y==line.y2:
                p2=p
                break
        self.linesList.append(line)
        if p1==None:
            p1 = pointM(line.x1,line.y1,line.m1,moovable=line.moovable1)
            self.pointList.append(p1)
        if p2==None:
            p2 = pointM(line.x2,line.y2,line.m2,moovable=line.moovable2)
            self.pointList.append(p2)
        line.point1 = p1
        line.point2 = p2
        self.addMatLine( line)
    def appendTri(self,x1,y1,x2,y2,x3,y3,mm=None):
        self.appendLine(lineM(x1,y1,x2,y2,granze1=1.5,granze2=.6))
        self.appendLine(lineM(x2,y2,x3,y3,granze1=1.5,granze2=.6))
        self.appendLine(lineM(x1,y1,x3,y3,granze1=1.5,granze2=.6))


    def calcSchnelligkeit(self,koeffiz):
        for po in self.pointList:
            if not po.moovable:
                continue
            accX = 0
            accY = self.gravity / koeffiz * po.mass

            for lin in self.linesList:
                if lin.point1 == po:
                    forsX, forsY = lin.calcForces(1)
                    accX += forsX / koeffiz 
                    accY += forsY / koeffiz 
                elif lin.point2 == po:
                    forsX, forsY = lin.calcForces(2)
                    accX +=  forsX / koeffiz 
                    accY +=  forsY / koeffiz 
            resistX = -po.speedX  * self.resistance
            resistY = -po.speedY  * self.resistance
            accX += resistX / koeffiz
            accY += resistY / koeffiz
            po.accX = accX
            po.accY = accY
            po.accX1 = -resistX
            po.accY1 = -resistY
            
    def calcSpeedKoeff(self):
        maxSpeed=0
        for po in self.pointList:
            if not po.moovable:
                continue
            newSpeed = math.sqrt(po.speedX**2+po.speedY**2)
            maxSpeed = newSpeed if newSpeed > maxSpeed else maxSpeed
        maxSpeed = 2 if maxSpeed < 2 else maxSpeed
        return maxSpeed*3         
            
    def calcSpeeds(self,koeffiz):
##        for po in self.pointList:
##            if not po.moovable:
##                continue
##            newSpeedX = po.speedX + po.accX / koeffiz
##            newSpeedY = po.speedY + po.accY / koeffiz
        for po in self.pointList:
            if not po.moovable:
                continue
            po.speedX += po.accX / koeffiz
            po.speedY += po.accY / koeffiz
            po.speedX = 100 if po.speedX > 100 else po.speedX
            po.speedX = -100 if po.speedX < -100 else po.speedX
            po.speedY = 100 if po.speedY > 100 else po.speedY
            po.speedY = -100 if po.speedY < -100 else po.speedY
            
##        return  maxSpeed

    def addMatLine(self, line):
        for currX,currY,xf,yf in renerateXYline(line.x1, line.y1, line.x2, line.y2):
            currList = self.mat[currX][currY]
            if not line in currList:
                currList.append(line)
                
    def minusMatLine(self, line):
        for currX,currY,xf,yf in renerateXYline(line.x1, line.y1, line.x2, line.y2):
            currList = self.mat[currX][currY]
            if line in currList:
                while line in currList: currList.remove(line)
               
                
    def impulse1(self, line, currX, currY):
        length = math.sqrt( (line.x1 - line.x2)**2+(line.y1 - line.y2)**2)
##        l1_ct = length* line.m1 / (line.m2 + line.m1)
##        l2_ct = length* line.m2 / (line.m2 + line.m1)

        l1 = math.sqrt( (line.x1 - currX)**2+(line.y1 - currY)**2) 
        l2 = math.sqrt( (line.x2 - currX)**2+(line.y2 - currY)**2)

        centroCoeff = abs(abs(l1/length)-.5)
        koef1speed = l1 / length
        koef1speed = 1 if koef1speed>1 else koef1speed
        koef2speed = l2 / length
        koef2speed = 1 if koef2speed>1 else koef2speed
        m  = line.m1 * koef1speed + line.m2 * koef2speed
        speedX = line.point1.speedX*  (1-koef1speed)  + line.point2.speedX* (1-koef2speed)
        speedY = line.point1.speedY*  (1-koef1speed)  + line.point2.speedY* (1-koef2speed)

        return centroCoeff,m,speedX,speedY, koef1speed, koef2speed
        
    def impulse(self, line, lineM, currX, currY, oldX, oldY):
        centroCoeff1, m1, speedX1,  speedY1,  koefspeed1,   koefspeed2   = self.impulse1(line,  oldX, oldY)
        centroCoeff2, m2, speedX2,  speedY2,  koefspeed1_m, koefspeed2_m = self.impulse1(lineM, oldX, oldY)

        lineX1,lineX2,lineMX1,lineMX2 = line.x1,line.x2,lineM.x1,lineM.x2
        lineY1,lineY2,lineMY1,lineMY2 = line.y1,line.y2,lineM.y1,lineM.y2
        if centroCoeff2 > centroCoeff1:
            # normal from line
            koeffNormalX = line.calcSignNormX(oldX,oldY,True)
            koeffNormalY = line.calcSignNormX(oldX,oldY,False)
            normX = 0 if (line.x2 - line.x1)==0 else  koeffNormalX* 1 / abs(line.x2 - line.x1)
            normY = 0 if (line.y2 - line.y1)==0 else  koeffNormalY* 1 / abs(line.y2 - line.y1)
            signForce = -1
        else:
            # normal from lineM
            koeffNormalX = lineM.calcSignNormX(oldX,oldY,True)
            koeffNormalY = lineM.calcSignNormX(oldX,oldY,False)
            normX = 0 if (lineM.x2 - lineM.x1)==0 else  koeffNormalX* 1 / abs(lineM.x2 - lineM.x1)
            normY = 0 if (lineM.y2 - lineM.y1)==0 else  koeffNormalY* 1 / abs(lineM.y2 - lineM.y1)
            signForce = 1
            
        normalizeKoeff = (1/math.sqrt(normX**2+normY**2))
        normX, normY = normX* normalizeKoeff, normY* normalizeKoeff 

        if (speedX1==0 and speedY1==0) or (normX==0 and normY==0):
            cosSchlag = 0
        else:
            # cosinus angle between normal vector and speed 1 (line)
            cosSchlag = (speedX1 *normX + speedY1 *normY) / math.sqrt(speedX1**2 + speedY1**2) / math.sqrt(normX**2 + normY**2)
                
        cosSchlag = abs(cosSchlag)
        cosSchlag = .1 if cosSchlag < .1 else cosSchlag    
       # after 
##        speed1 = ((m1 - m2) * math.sqrt(speedX1**2+speedY1**2)) /  (m1 + m2)
##        speed2 = (  2 * m1  * math.sqrt(speedX2**2+speedY2**2)) /  (m1 + m2)
        speed1 = (  m2 / m1  * math.sqrt(speedX1**2+speedY1**2)) 
        speed2 = (  m1 / m2  * math.sqrt(speedX1**2+speedY1**2)) 
        
        speedX1_ = speedX1 + signForce* normX * speed1 * cosSchlag
        speedY1_ = speedY1 + signForce* normY * speed1 * cosSchlag 
        speedX2_ = speedX2 - signForce* normX * speed2 * cosSchlag 
        speedY2_ = speedY2 - signForce* normY * speed2 * cosSchlag 

        newX1line    = speedX1_ *  (1-koefspeed1) + line.point1.speedX   *koefspeed1
        newX2line    = speedX1_ *  (1-koefspeed2) + line.point2.speedX   *koefspeed2
        newY1line    = speedY1_ *  (1-koefspeed1) + line.point1.speedY   *koefspeed1
        newY2line    = speedY1_ *  (1-koefspeed2) + line.point2.speedY   *koefspeed2
        newX1lineM   = speedX2_ * (1-koefspeed1_m)+ lineM.point1.speedX  *koefspeed1_m
        newX2lineM   = speedX2_ * (1-koefspeed2_m)+ lineM.point2.speedX  *koefspeed2_m 
        newY1lineM   = speedY2_ * (1-koefspeed1_m)+ lineM.point1.speedY  *koefspeed1_m
        newY2lineM   = speedY2_ * (1-koefspeed2_m)+ lineM.point2.speedY  *koefspeed2_m

        
##        print(" 1 k1=%f k2=%f speedY1=%f speedY2=%f after speedY1_=%f speedY2_=%f "
##              %(koefspeed1,koefspeed2,line.point1.speedY,line.point2.speedY,newY1line,newY2line))
##        print(" 2 k1=%f k2=%f speedY1=%f speedY2=%f after speedY1_=%f speedY2_=%f "
##              %(koefspeed1_m,koefspeed2_m,lineM.point1.speedY,lineM.point2.speedY,newY1lineM,newY2lineM))
        
        line.point1.speedX, line.point1.speedY = (newX1line, newY1line) if line.point1.moovable else (0,0)
        line.point2.speedX, line.point2.speedY = (newX2line, newY2line) if line.point2.moovable else (0,0)
        lineM.point1.speedX, lineM.point1.speedY = (newX1lineM, newY1lineM)  if lineM.point1.moovable else (0,0)
        lineM.point2.speedX, lineM.point2.speedY = (newX2lineM, newY2lineM)  if lineM.point2.moovable else (0,0)
##        line.point1.speedX, line.point1.speedY =
        

    def gelegenheitMove(self, line,num,newX,newY):
        lengthOld = round(math.sqrt((line.x2 - line.x1) **2 + (line.y2 - line.y1) **2))
        lengthOld = 1 if lengthOld < 1 else lengthOld
        
        if num==1:
           length = round(math.sqrt((newX - line.x2) **2 + (newY - line.y2) **2))
           length = 1 if length < 1 else length
           for currX,currY,xf,yf in renerateXYline(newX, newY, line.x2, line.y2):
                currList = self.mat[currX][currY]
                if line in currList:
                    continue
                for lineM in currList:
                    if lineM.point1==line.point1 or lineM.point1==line.point2 or lineM.point2==line.point1 or lineM.point2==line.point2:
                        continue
                    progress = math.sqrt((xf - line.x2) **2 + (yf - line.y2) **2)/length
                    oldX = line.x2 + (line.x1 - line.x2) * progress
                    oldY = line.y2 + (line.y1 - line.y2) * progress
                    self.impulse( line, lineM, xf, yf, oldX, oldY )
                    return False, lineM
           return True, None
        elif num==2:
            length = round(math.sqrt((newX - line.x1) **2 + (newY - line.y1) **2))
            length = 1 if length < 1 else length
            for currX,currY,xf,yf in renerateXYline( line.x1, line.y1,newX, newY):
                currList = self.mat[currX][currY]
                if line in currList:
                    continue
                for lineM in currList:
                    if lineM.point1==line.point1 or lineM.point1==line.point2 or lineM.point2==line.point1 or lineM.point2==line.point2:
                        continue
                    progress = math.sqrt((xf - line.x1) **2 + (yf - line.y1) **2)/lengthOld
                    oldX = line.x1 + (line.x2 - line.x1) * progress
                    oldY = line.y1 + (line.y2 - line.y1) * progress
                    self.impulse( line, lineM, xf, yf, oldX, oldY )
                    return False, lineM
            return True, None


    def move(self, koeffiz ):
        already = []
        for iii in range(4):
            for po in self.pointList:
                if not po.moovable:
                    already.append(po)
                    continue
                if po in already:
                    continue
                curX, curY = po.x, po.y
                curXint, curYint = int (curX), int (curY)
                newX = curX+ po.speedX / koeffiz
                newY = curY+ po.speedY / koeffiz
                newXint, newYint = int (newX), int (newY)
                
                if(newXint<0):
                    newX=0
                if(newYint<0):
                    newY=0
                if(newXint>=self.x_size):
                    newX, newXint = curX, int(curX)
                if(newYint>=self.y_size):
                    newY, newYint = curY, int(curY)
                    po.speedY = 0
                #lets move
                notColliz = True
                for lin in self.linesList:
                    if lin.broken:
                        continue
                    if lin.point1 == po:
                        # let's check for collisions
                        notColliz, lineM = self.gelegenheitMove(lin, 1, newX, newY)
                    if lin.point2 == po:
                        notColliz, lineM = self.gelegenheitMove(lin, 2, newX, newY)
                    if not notColliz: break
                if not notColliz:
                    if lineM.point1 in already:
                        already.remove(lineM.point1)
                    if lineM.point2 in already:
                        already.remove(lineM.point2)
                else:
                    for lin in self.linesList:
                        if lin.broken:
                             continue
                        if lin.point1 == po:
                             self.minusMatLine( lin)
                             lin.x1 = newX
                             lin.y1 = newY
                             self.addMatLine( lin)
                        if lin.point2 == po:
                             self.minusMatLine( lin)
                             lin.x2 = newX
                             lin.y2 = newY
                             self.addMatLine( lin)
                    po.x = newX
                    po.y = newY
                    already.append(po)
                    
            koeffiz = self.calcSpeedKoeff()
            for lin in self.linesList:
                if not lin.point1 in already:
                    lin.point1.speedX *= .95
                    lin.point1.speedY *= .95    
                if not lin.point2 in already:
                    lin.point2.speedX *= .95
                    lin.point2.speedY *= .95    
          
        for lin in self.linesList:
            lin.color="#FF1111" if not lin.point1 in already or not lin.point2 in already else "#999999"
        if len(already)<len(self.pointList):
            return False
        else:
            return True
        
    def brokeLines(self):
        for lin in self.linesList:
            if not lin.broken:
                currLange = math.sqrt((lin.x1 - lin.x2) * (lin.x1 - lin.x2) + (lin.y1 - lin.y2) * (lin.y1 - lin.y2)) \
                            / lin.lange
                if lin.granze1<currLange:
                    lin.broken = True
                    self.minusMatLine( lin)
                if lin.granze2>currLange:
                    lin.broken = True
                    self.minusMatLine( lin)

