import time
import rrdtool
from getSNMP import consultaSNMP, consultaSNMP2
from threading import Thread
from trendGraphDetection import grafica
from inventarioPDF import creaPDF, acomodaInfo
from datetime import datetime
from datetime import timedelta
from  Notify import send_alert_attached
#from  Notify import send_alert_attached
import time

rrdpath = '/home/eric/ASR/Practicas/Practica3/4-AdministraciónDeRendimiento/RRD/'
NumPack = 0
numP = 0

i = 0
ini = 0
pack = 5000
tarifa= 1.25
cincuenta = pack/2
ochenta = pack*0.8
noventay5 = pack*0.95
newString = ''
# fechas de inicio y fin del periodo de facturación
now = datetime.now()
vigencia = now + timedelta(days=30)

def sentinela (n):
    global numP, NumPack, cincuenta, ochenta, noventay5, ini , now , vigencia, newString
    flag = 3
    while 1:
        if numP >= cincuenta and numP <=  ochenta and flag >=3:
            msn = 'Consumiste la mitad de tus paquetes UDP el :{}'.format(now)+'\n'
            print(msn)
            newString = newString + msn
            flag = 2
        if numP >= ochenta and numP <=  noventay5 and flag >=2:
            msn = 'Consumiste el 80% de tus paquetes UDP el :{}'.format(now) +'\n'
            print(msn)
            newString = newString + msn
            flag = 1
        if numP >= noventay5  and flag >=1:
            msn = 'Consumiste el 95% de tus paquetes UDPel :{}'.format(now)  +'\n'
            print(msn)
            newString = newString + msn
            flag = 0
            time.sleep(1)
        if numP >= pack  and flag >= 0 :
            print('ya has consumido tus paquetes UDP, se aplicará una tarifa diferente a partir de esta fecha {}\n'.format(now))
            print(msn)
            newString = newString + msn                        
            flag = -1  
            time.sleep(3)
            grafica()                      
            time.sleep(3)
            msn = 'Detalle de consumo: \n Incluidos en tu UDPack: {}'.format(pack)+' con tarifa de: ${}c/u' .format(tarifa) + ' Total de UDPack: ${}\n'.format(pack*tarifa)+'Por tu consumo de paquetes extra son {}'.format(numP-pack)+' con tarifa de: ${}c/u' .format(tarifa*2) + 'Total de paquetes extra: ${}\n'.format((numP-pack)*(tarifa*2))
            print(msn)
            newString = newString + msn     
            creaPDF(newString, 'deteccion.png')  
            send_alert_attached(newString)          
            time.sleep(120)

# iniciamos el demonio con la funcion sentinela

t = Thread(target = sentinela, args=(10, ), daemon=True )
t.start()

#recuperamos los datos del dispositivo que va a consumir paquetes

info = consultaSNMP2('comunidadASR','192.168.0.8','1.3.6.1.2.1.1.1.0')
newString = newString + info+'\n'
# establecemos la referencia del numero de paquete UDP actual para el inicio

ini = int(consultaSNMP('comunidadASR','192.168.0.8','1.3.6.1.2.1.7.1.0'))

# imprimimos la fecha de inicio del paquete y el periodo de duración

newString = newString + 'Tu consumo de {} paquetes'.format(pack)+' con tarifa de ${}'.format(tarifa)+' tiene una vigencia de 30 días apartir de ahora {}'.format(now) + ' y concluye el {}'.format(vigencia) +'\n'
print(newString)


'''
print(ini)
print(ini + cincuenta)
print(ini + ochenta)
print(ini + noventay5)
'''

while 1:

    NumPack = int(consultaSNMP('comunidadASR','192.168.0.8','1.3.6.1.2.1.7.1.0'))       
    numP = NumPack - ini
    valor = "N:" + str(numP)  
    print(numP)
    #print (i)
    rrdtool.update(rrdpath+'trend.rrd', valor)
    rrdtool.dump(rrdpath+'trend.rrd','trend.xml')
    time.sleep(10)
    if now > vigencia:
            print("Ha concluido el periodo de tus paquetes UDP")

if ret:
    print (rrdtool.error())
    time.sleep(300)
