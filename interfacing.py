import os
import sys
import random
import time
import hardware

def getinput():
    
    s=0
    mat=[]
    data1=[]
    one=1
    zer=0
    #print(s,mat,data1,one,zer)
    #x=raw_input("values..")

    while(s!=1):
        #print("begining of while loop")
        s=hardware.checkbutton()
        #print("check button",s)
        if(s==1):
            data=hardware.getbytes()
            j=0
            #print("bytes in getinput",data)
            for i in data:
                if(i=='O'):
                    #data1=data1+one
                    data1.append(one)
                elif(i=='F'):
                    data1.append(zer)
                else:
                    print("transmission error")
                j=j+1
            #print("bytes in 1,0 ",data1)
            n=8
            temp=[data1[i:i+n] for i in range(0, len(data1), n)]
            n1=1
            #print("temp",temp)
            dispmat(temp,r,c)
            #hardware.clear_button()
            #print("s after clr button ",s)
            #print("end of whiile loop and then break")
            return temp
            break

        else:
            #print("s is not 1");
            s=0
            #print("now s becomes ",s)
    
def swapmatrix():
    global matrix1,matrix2,wflag,lflag
    wflag[0]=0
    hardware.led_warning(wflag[0])
    lflag[0]=0
    hardware.led_turn(lflag[0])
    #hardware.disable_int()
    #print("Before swapping")
    #dispmat(matrix1,r,c)
    #dispmat(matrix2,r,c)
    swap(matrix1,matrix2)
    #print("After swapping")
    #dispmat(matrix1,r,c)
    #dispmat(matrix2,r,c)
    #x=raw_input()

def invalidmoveflag(flag):
    global wflag
    wflag[0]=flag
    #print(wflag[0])
    #x=raw_input()
    hardware.led_warning(wflag[0])
    #x=raw_input()
    #print(wflag)#set warning flag
    #print("end of invalid move flag function")
    #x=raw_input()

def invalidswap():
    global matrix2,matrix1
    swap(matrix2,matrix1)
    #print("After invalid move")
    #dispmat(matrix1,r,c)
    #dispmat(matrix2,r,c)


def checkinterface():    
    i,f=[],[]
    global initial,final,matrix2,matrix1,lflag,wflag
    lflag[0]=1
    hardware.led_turn(lflag[0])
    #hardware.enable_int()
    print("in checkinterface")
    print("wflg in check interface ",wflag[0])
    #x=raw_input()
    if(wflag[0]==0):
        matrix2=getinput()
        print("matrix2",matrix2)
        i,f=initialfinal(matrix1,matrix2,r,c)
        print("get poitions",i,f)
        if(len(i)!=0 and len(f)!=0):
            initial,final=i,f
        if(len(f)==0 and len(i)!=0):
            #time.sleep(3)
            t_f=i
            swap(temp,matrix2)
            matrix2=getinput()
            i,f=initialfinal(matrix2,temp,r,c)
            if(f==t_f):
                initial,final=i,f

        if(len(i)==0 and len(f)==0):#if plyr pick the piece and place it at the same position
            print("asd")
            while(len(i)==0 and len(f)==0):
                matrix2=getinput()
                print("matrix2 in infinite loop",matrix2)
                i,f=initialfinal(matrix1,matrix2,r,c)
                print("initial final in loop",i,f)
                initial,final=i,f

            
            
    if(wflag[0]==1): #for invalid move
        print("ok")
        #sglobal initial
        print(initial)
        matrix2=getinput()
        #set here the condition when the piece come to its initial position
        i,f=initialfinal(matrix1,matrix2,r,c)
        if(len(i)==0 and len(f)==0):
            wflag[0]=0
            hardware.led_warning(wflag[0])
            matrix2=getinput()
            i,f=initialfinal(matrix1,matrix2,r,c)
            initial,final=i,f
        else:
            initial,final=i,f  
            
    print("ini final in interfcng",initial,final)
    return initial,final

def finalpositions(i,f):
    global matrix1,matrix2
    print("in interfacing")
    print(i,f)
    #x=raw_input()
    if(matrix1[f[0]][f[1]]==1):
        hardware.remove_piece((f[0]+1),(f[1]+1))
    matrix1[i[0]][i[1]],matrix2[i[0]][i[1]]=0,0
    matrix1[f[0]][f[1]],matrix2[f[0]][f[1]]=1,1
    dispmat(matrix1,r,c)
    dispmat(matrix2,r,c)
    #x=raw_input()
    hardware.set_value((i[1]+1),(i[0]+1),(f[1]+1),(f[0]+1))
    print(hardware.x1,hardware.y1,hardware.x2,hardware.y2)
    #x=raw_input()
    hardware.perform_move()
    print("end of finalposition function")
    #x=raw_input()


#interfun.py functions

def initialfinal(m1,m2,r,c):
    i=[]
    f=[]
    for x in range(r):
        for y in range(c):
            if (m1[x][y] != m2[x][y]):
                if(m1[x][y]==1 and m2[x][y]==0):
                    i.append(x)
                    i.append(y)
                    #print("initial",initial)

                if(m1[x][y]==0 and m2[x][y]==1):
                    f.append(x);
                    f.append(y);
                    #print("final",final)
    return i,f

def swap(m1,m2):
    for x in range(8):
        for y in range(8):
            m1[x][y]=m2[x][y]
    return m1

def dispmat(matrix,r,c):
    for x in range(c):
        print(matrix[x])
    print("\n\n")

def initialize():
    hardware.initialize()
    

#end of interfun.py

    
print("Interfacing")
r,c=8,8
matrix1=[[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]
matrix2=[[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]
temp=[[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]
#matrixa=[[1,2,3,4,5,3,2,1],[6,6,6,6,6,6,6,6],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[12,12,12,12,12,12,12,12],[7,8,9,10,11,9,8,7]]
initial,final=[0,0],[0,0]
wflag=[0]
lflag=[0]
