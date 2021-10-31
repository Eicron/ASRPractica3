import rrdtool
ret = rrdtool.create("/home/eric/ASR/Practicas/Practica3/4-AdministraciónDeRendimiento/RRD/trend.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:CPUload:GAUGE:600:U:U",
                     #"DS:RAMload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:24")
if ret:
    print (rrdtool.error())
