import rrdtool
import time
rrdpath = '/home/eric/ASR/Practicas/Practica2/4-AdministraciónDeRendimiento/RRD/'
imgpath = '/home/eric/ASR/Practicas/Practica2/4-AdministraciónDeRendimiento/IMG/'
fname = 'trend.rrd'
ultima_lectura = int(rrdtool.last(rrdpath+fname))
tiempo_final = ultima_lectura
tiempo_inicial = tiempo_final - 2000

ret = rrdtool.graph( imgpath+"trendC.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Carga CPU",
                     "--title=Tendencia del uso del CPU",
                     "--color", "ARROW#009900",
                     '--vertical-label', "Uso de CPU (%)",
                     '--lower-limit', '0',
                     '--upper-limit', '100',
                     "DEF:carga="+rrdpath+"trend.rrd:CPUload:AVERAGE",
                     "AREA:carga#00FF00:Carga CPU",                     
                     "LINE1:30",
                     "AREA:5#ff000022:stack",
                     "VDEF:CPUlast=carga,LAST",
                     "VDEF:CPUmin=carga,MINIMUM",
                     "VDEF:CPUavg=carga,AVERAGE",
                     "VDEF:CPUmax=carga,MAXIMUM",

                    "COMMENT:Now          Min             Avg             Max",
                     "GPRINT:CPUlast:%12.0lf%s",
                     "GPRINT:CPUmin:%10.0lf%s",
                     "GPRINT:CPUavg:%13.0lf%s",
                     "GPRINT:CPUmax:%13.0lf%s",
                     "VDEF:m=carga,LSLSLOPE",
                     "VDEF:b=carga,LSLINT",
                     'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                     "LINE2:tendencia#FFBB00" )