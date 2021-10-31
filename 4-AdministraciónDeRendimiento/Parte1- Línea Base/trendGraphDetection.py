import sys
import rrdtool
from  Notify import send_alert_attached
from inventarioPDF import creaPDF
from getSNMP import consultaSNMP2


def grafica ():
    rrdpath = '/home/eric/ASR/Practicas/Practica3/4-AdministraciónDeRendimiento/RRD/'
    imgpath = '/home/eric/ASR/Practicas/Practica3/4-AdministraciónDeRendimiento/IMG/'

    ultima_lectura = int(rrdtool.last(rrdpath+"trend.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 600
    imgName = 'deteccion.png'


    ret = rrdtool.graphv( imgpath+imgName,
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Paquetes UDP",
                        '--lower-limit', '0',
                        '--upper-limit', '5000',
                        "--title=Consumo de paquetes UDP \n En un periodo",

                        "DEF:NumPack="+rrdpath+"trend.rrd:CPUload:AVERAGE",

                        "VDEF:cargaMAX=NumPack,MAXIMUM",
                        "VDEF:cargaMIN=NumPack,MINIMUM",
                        "VDEF:cargaSTDEV=NumPack,STDEV",
                        "VDEF:cargaLAST=NumPack,LAST",

                        "LINE10:2500#ff000020",
                        "LINE10:4500#ff000040",
                        "CDEF:umbral5=NumPack,5000,LT,0,NumPack,IF",
                        "AREA:NumPack#00FF00:Consumo menos al 50%",
                        "AREA:umbral5#FF9F00:Consumo mayor al 80%",
                        "HRULE:5000#FF0000:Umbral 1 - 5%",

                        "PRINT:cargaLAST:%6.2lf",
                        "GPRINT:cargaMIN:%6.2lf %SMIN",
                        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                        "GPRINT:cargaLAST:%6.2lf %SLAST" )
    
    print (ret)
'''
    ultimo_valor=float(ret['print[0]'])
    if ultimo_valor>50000:
        infoDisp = consultaSNMP2('comunidadASR','localhost','1.3.6.1.2.1.7.1.0')
        print(infoDisp)
        #creaPDF(infoDisp, imgName)  
        send_alert_attached("Se han consumido todo tus paquetes")
        print("El uso de procesador ha sobrepasado la recomendación")
'''
        
    