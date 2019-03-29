from math import sqrt
import serial
#import struct
from time import sleep
ser = serial.Serial(
    port='COM7',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

x1=1
y1=1
y2=1
x2=1
mag_x=1
mag_y=1

def send_data_motor(val,ch,op='x'):
    '''
    if(ch==112):
        ch==64
    elif(ch==96):
        ch=80
    elif(ch==64):
        ch=112
    elif(ch==80):
        ch=96
    '''
    d ='a'
    st='m'
    print("send_data_motor","m",chr(val[0]),chr(val[1]),ch,op)
    st+=chr(int(val[0])+65)
    st+=chr(int(val[1])+65)
    st+=chr(ch)
    st+=op
    print(st)
    ser.write(st) 
    sleep(1)
    d=ser.read(1)
    if(d=='d'):
        print("move performed\n")
    else:
        print("move failed\n")
    sleep(0.4)
        



def init_mag_move(p,q):  #p,q -> final position
    global mag_x,mag_y
    direc=0b01110000
    print('initmagmove',mag_x,mag_y)
    if((mag_x-p)>0):
        direc=0b01000000
    else:
        direc=0b01100000
    send_data_motor([abs(mag_x-p),0],direc)
    
    if((mag_y-q)>0):
        direc=0b01000000
    else:
        direc=0b01010000
    send_data_motor([0,abs(mag_y-q)],direc)  # abs() returns only positive value
    mag_y=q
    mag_x=p

def set_value(p,q,r,s):
    global x1,x2,y1,y2
    x1=p
    y1=q
    x2=r
    y2=s
    print("set_value",x1,y1,x2,y2)

def diagonal_move():
    global x1,x2,y1,y2,mag_x,mag_y
    dirc=0b01110000
    print("diagonal move")
    if((x1-x2)<0 and (y1-y2)<0):
        dirc=0b01110000
    elif((x1-x2)>0 and (y1-y2)>0):
        dirc=0b01000000
    elif((x1-x2)>0 and (y1-y2)<0):
        dirc=0b01010000
    elif((x1-x2)<0 and (y1-y2)>0):
        dirc=0b01100000
    send_data_motor([abs(x1-x2),abs(y1-y2)],dirc)
    mag_x=x2
    mag_y=y2
    

def knight_move():
    global x1,x2,y1,y2,mag_x,mag_y
    dirc=0b01110000
    values=[1,1]
    print("knight move")
    if(((y2-y1)>0)and(abs(x1-x2)==1)):
        if(x1<x2):
            dirc=0b01110000
            send_data_motor(values,dirc,'z')
            send_data_motor([0,1],dirc)
            send_data_motor(values,dirc,'z')
                
        else:
            dirc=0b01010000
            send_data_motor(values,dirc,'z')
            send_data_motor([0,1],dirc)
            send_data_motor(values,dirc,'z')
            
    elif(((y1-y2)>0)and(abs(x1-x2)==1)):
        if(x1<x2):
            dirc=0b01100000
            send_data_motor(values,dirc,'z')
            send_data_motor([0,1],dirc)
            send_data_motor(values,dirc,'z')
            
        else:
            dirc=0b01000000
            send_data_motor(values,dirc,'z')
            send_data_motor([0,1],dirc)
            send_data_motor(values,dirc,'z')
            
    elif(((x2-x1)>0)and(abs(y1-y2)==1)):
        if(y1<y2):
            dirc=0b01110000
            send_data_motor(values,dirc,'z')
            send_data_motor([1,0],dirc)
            send_data_motor(values,dirc,'z')
            
        else:
            dirc=0b01100000
            send_data_motor(values,dirc,'z')
            send_data_motor([1,0],dirc)
            send_data_motor(values,dirc,'z')

    elif(((x1-x2)>0)and(abs(y1-y2)==1)):
        if(y1<y2):
            dirc=0b01010000
            send_data_motor(values,dirc,'z')
            send_data_motor([1,0],dirc)
            send_data_motor(values,dirc,'z')
        else:
            dirc=0b01000000
            send_data_motor(values,dirc,'z')
            send_data_motor([1,0],dirc)
            send_data_motor(values,dirc,'z')
    mag_x=x2
    mag_y=y2
    

def straight_move():
    global x1,x2,y1,y2,mag_x,mag_y
    dist_move=0
    print("straight move")
    if(x1==x2):
        if((y1-y2)<0):
            dirc=0b01010000
        else:
            dirc=0b01000000
        print(" move",chr(dirc))
        dist_move=abs(y1-y2)
        print("dist_move",dist_move)
        send_data_motor([0,dist_move],dirc)

    else:
        if((x1-x2)<0):
            dirc=0b01100000
        else:
            dirc=0b01000000
        dist_move=abs(x1-x2)
        print(" move",chr(dirc))
        print("dist_move",dist_move)
        send_data_motor([dist_move,0],dirc)
    mag_x=x2
    mag_y=y2
    
    
    
def perform_move():
    global x1,x2,y1,y2,mag_x,mag_y
    p=x1
    q=y1
    print("perform_move",x1,y1,x2,y2)
    magnet(0)
    init_mag_move(p,q)
    magnet(1)
    if((x1!=x2)and(y1!=y2)):
        if(abs(x1-x2)==abs(y1-y2)):
            diagonal_move()
        else:
            knight_move()
    else:
        straight_move()
    magnet(0)



def remove_piece(p,q): #p=x , q=y
    global mag_x,mag_y,x1,y1
    init_mag_move(x1,y1)
    magnet(0)
    dirc=0b01010000
    send_data_motor([1,1],dirc,'z')
    p=p-1
    send_data_motor([p,0],dirc)
    dirc=0b01000000
    send_data_motor([1,1],dirc,'z')
    dirc=0b01100000
    send_data_motor([1,0],dirc)
    mag_x=1
    mag_y=q

#--------------------------------------------------------------------------

def checkbutton():
    d=''
    ser.write('u')
    sleep(0.5)
    d=ser.read(1)
    if(d=='s'):
        return 1
    else:
        print("check button failed\n")

'''
def clear_button():
    d=''
    ser.write('z')
    sleep(0.1)
    d=ser.read(1)
    if(d=='d'):
        print("button cleared\n")
    else:
        print("button value unable to be cleared\n")

def enable_int():
    d=''
    ser.write('j')
    sleep(0.1)
    d=ser.read(1)
    if(d=='d'):
        print("interrupt enabled\n")
    else:
        print("interrupt enable error\n")

def disable_int():
    d=''
    ser.write('k')
    sleep(0.1)
    d=ser.read(1)
    if(d=='d'):
        print("interrupt disabled\n")
    else:
        print("interrupt disable error\n")

'''
def magnet(boo):
    d=''
    mag=''
    if(boo==1):
        mag='go'
    else:
        mag='gf'
    ser.write(mag)
    sleep(0.5)
    d=ser.read(1)
    if(d=='d'):
        if(boo==1):
            print("magnet activated\n")
        else:
            print("magnet deactivated\n")
    else:
        print("magnet data transmission failed\n")
    sleep(0.5)
    


def initialize():
    d=''
    ser.write('o')
    sleep(0.4)
    d=ser.read(1)
    if(d=='d'):
       print("initialisation done\n")
    else:
        print("initialisation failed\n")
        
    
    
def getbytes():   #getbyte
    ser.write('b')
    sleep(0.1)
    data=ser.read(64)
    print data
    return data

def led_warning(val):
    q=0
    if(val==1):
        ser.write("lwn")
        q=1        
    else:
        ser.write("lwf")
        q=0
        
    d=''
    d=ser.read(1)
    if(d=='d'):
        if(q==1):
            print("warning led on")
        else:
            print("warning led off")


def led_turn(val):
    q=0
    if(val==1):
        ser.write("ltn")
        q=1
    else:
        ser.write("ltf")
        q=0
        
    d=''
    d=ser.read(1)
    if(d=='d'):
        if(q==1):
            print("turn led on")
        else:
            print("turn led off")






