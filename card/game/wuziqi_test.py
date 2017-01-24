#coding=utf-8
import os
import pdb
class five:
    def __init__(self,maxx,maxy):
        self.maxx=maxx
        self.maxy=maxy
        self.qipan=[]
        for i in range(maxx):
            self.qipan.append([])
            for j in range(maxy):
                self.qipan[i].append(0)
    def start(self):
        '''
            初始化测试
        '''
        #self.qipan[1][1]=self.qipan[2][1]=self.qipan[3][1]=self.qipan[4][1]=self.qipan[5][1]=1
        who=False
        os.system('cls')
        self.printqp()
        while True:
            t=input('Please input(x,y),now is'+('〇' if who else '乂')+':')
            t=t.split(',')
            if len(t)==2:
                x=int(t[0])
                y=int(t[1])
                if self.qipan[x][y]==0:
                    self.qipan[x][y]=1 if who else 2
                    os.system('cls')
                    self.printqp()
                    ans=self.isWin(x,y)
                    if ans:
                        print(('〇'if who else '乂')+'Win')
                        break
                    who=not who
        os.system('pause')
    def isWin(self,xPoint,yPoint):#判赢
        pdb.set_trace
        flag=False
        t=self.qipan[xPoint][yPoint]
        x=xPoint
        y=yPoint
        #横向
        count=0
        x=xPoint
        y=yPoint
        while (x>0 and t==self.qipan[x][y]):
            count+=1
            x-=1
        x=xPoint
        y=yPoint
        while (x<self.maxx and t==self.qipan[x][y]):
            count+=1
            x+=1
        if (count>5):return True
        #纵向
        count=0
        x=xPoint
        y=yPoint
        while (y>0 and t==self.qipan[x][y]):
            count+=1
            y-=1
        y=yPoint
        while (y<self.maxy and t==self.qipan[x][y]):
            count+=1
            y+=1
        if (count>5): return True
        #/
        count=0
        x=xPoint
        y=yPoint
        while (x>0 and y<self.maxy and t==self.qipan[x][y]):
            count+=1
            x+=1
            y-=1
        x=xPoint
        y=yPoint
        while (x<self.maxx and y>0 and t==self.qipan[x][y]):
            count+=1
            x-=1
            y+=1
        if (count>5):return True
        #\
        count=0
        x=xPoint
        y=yPoint
        while (x>0 and y>0 and t==self.qipan[x][y]):
            count+=1
            x+=1
            y-=1
        x=xPoint
        y=yPoint
        while (x<self.maxx and y<self.maxy and t==self.qipan[x][y]):
            count+=1
            x-=1
            y+=1
        if (count>5): return True
        return False
    def printqp(self):#打印棋盘
        print '〇一二三四五六七八九'
        for i in range(self.maxx):
            print i
            for j in range(self.maxy):
                if self.qipan[i][j]==0:
                    print '十'
                elif self.qipan[i][j]==1:
                    print '〇'
                elif self.qipan[i][j]==2:
                    print '乂'
            print('\n')
if __name__=='__main__':
    t=five(10,10)
    #pdb.set_trace()
    t.start()