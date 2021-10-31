from threading import Thread
import time
from getSNMP import consultaSNMP
i=0
def temporizador (n):
    global i
    while 1:
        if i >=50:
            print('mas de 50')
            flag = 1
            time.sleep(10)

t = Thread(target = temporizador, args=(10, ))#, daemon=True )
t.start()


print('fin de main')