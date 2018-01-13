def oriNumb(ori):
    
    if(ori=='r'):
        return 0
    elif(ori=='d'):
        return 1
    elif(ori=='l'):
        return 2
    elif(ori=='u'):
        return 3

def numbOri(numb):
    
    if(numb==0):
        return 'r'
    elif(numb==1):
        return 'd'
    elif(numb==2):
        return 'l'
    elif(numb==3):
        return 'u'    

def desloc(x,y,ori):
    des=1
    if(ori=='r'):
        return (x+des,y)
    elif(ori=='l'):
        return (x-des,y)
    elif(ori=='u'):
        return (x,y-des)
    elif (ori=='d'):
        return (x,y+des)

def calcTag(lastori,ori):
    
    resp=oriNumb(ori)-oriNumb(lastori)
    if((lastori=='u' and ori=='r')):
        resp=1
    elif((lastori=='r' and ori=='u')):
        resp=-1
    return resp