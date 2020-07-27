from zipfile import ZipFile
from itertools import permutations
import re
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import blue,red,black
from reportlab.lib.units import inch
import fitz
from PyPDF2 import PdfFileMerger
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase import pdfmetrics
s=" "
def Reverse(tuples):
    new_tup = ()
    for k in reversed(tuples):
        new_tup = new_tup + (k,)
    return new_tup
if __name__=="__main__":
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    testfile=open('temp1/test.txt','w+')
    with ZipFile('sample1.zip','r') as zipObj:
        #zipObj.extractall('temp1')
        names=zipObj.namelist()
    files=[]
    index=0
    combo1=[]
    combo=[]
    for count, x in enumerate(names):
        f = open ('temp1/'+str(x),'r')
        files.append(f)
        index=index+1
    indextable=list(range(index))
    perm=permutations(indextable,2)
    for i in list(perm):
        combo1.append(i)
    for i in range(len(combo1)):
        for j in range(i):
            if Reverse(combo1[i])==combo1[j]:
                combo.append(Reverse(combo1[i]))
    matched=[]
    for i in combo:
        f5=[]
        f6=[]
        match=[]
        print(i)
        f1=files[i[0]].read()
        f2=files[i[1]].read()
        f3=f1.split('\n')
        f4=f2.split('\n')
        for ii in f3:
            k=ii.strip()
            ki=' '.join(k.split())
            f5.append(ki)
        for ii in f4:
            k=ii.strip()
            ki=' '.join(k.split())
            f6.append(ki)
        canvas=Canvas("temp1/"+str(i[0])+str(i[1])+".pdf", pagesize=(8*inch,((len(f5)*0.22)+(len(f6)*0.22))*inch))
        #frame1 = Frame(0.25*inch, 0.25*inch, 7.5*inch, (((len(f5)*0.5)+(len(f6)*0.5))-0.5)*inch, showBoundary=1)
        #styles = getSampleStyleSheet()
        line=((len(f5)*0.22)+(len(f6)*0.22))-0.4
        for p in f5:
            for q in f6:
                if p==q:
                    if not p.startswith("#"):
                        if not p.startswith("using"):
                             if not p.startswith("{"):
                                  if not p.startswith("}"):
                                       if not p.startswith("int main"):
                                            if not p.startswith("return 0"):
                                                if not p.startswith("//"):
                                                    match.append(p)
        files[i[0]].seek(0)
        files[i[1]].seek(0)
        matched.append(match)
        canvas.drawString(3*inch,line*inch,"-( "+names[i[0]]+" )-")
        line=line-0.5
        for ii in f5:
            canvas.drawString(0.5*inch,line*inch,ii)
            line=line-0.2
        canvas.drawString(3*inch,line*inch,"-( "+names[i[1]]+" )-")
        line=line-0.5
        line=line-0.3
        for ii in f6:
            canvas.drawString(0.5*inch,line*inch,ii)
            line=line-0.2
        canvas.save()
        doc = fitz.open("temp1/"+str(i[0])+str(i[1])+".pdf")
        page = doc[0]
        for jp in match:
            tru=1
            text = jp
            text_instances = page.searchFor(text)
            ### HIGHLIGHT
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
            ### OUTPUT
        doc.save("temp1/"+str(i[0])+str(i[1])+"h.pdf", garbage=4, deflate=True, clean=True)