from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from getSNMP import consultaSNMP2

def acomodaInfo(cadena):
    rowsize = 70
    filas = len(cadena)/rowsize
    size = len(cadena)
    newString = ''
    pos = 0

    while size != 0 :
        if (size>=rowsize):
            newString = newString + cadena[pos:pos+rowsize]
            newString = newString+'\n'
            size = size - rowsize
            pos = pos + rowsize
        else:
            newString = newString + cadena[pos:pos+size]
            size = 0
    #print('Entre a inventarioPDF')
    return newString    

# dimensiones de letter (612.0, 792.0)
def creaPDF(info,img ):
    h=792.0
    infoDisp = acomodaInfo(info)
    c=canvas.Canvas('inventario.pdf', letter)
    text = c.beginText(50,h-50)
    #text.setFont('arial', 12)
    text.textLine('Reporte de dispositivo:')
    text.textLine('')
    text.textLines(infoDisp)
    c.drawText(text)
    c.drawImage('../IMG/'+img, 50,h-600)
    c.showPage
    c.save()

#infoDisp = str(consultaSNMP2('comunidadASR','localhost','1.3.6.1.2.1.1.1.0'))
#infoDisp = acomodaInfo(infoDisp)
#creaPDF(infoDisp, 'deteccion.png')
#creaPDF('hola', 'deteccion.png')
#print (infoDisp)
