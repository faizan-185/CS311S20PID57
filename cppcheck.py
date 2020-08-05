from zipfile import ZipFile
from itertools import permutations
import re
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import blue,red,black
from reportlab.lib.units import inch,cm
import fitz
from PyPDF2 import PdfFileMerger
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from PyPDF2 import PdfFileMerger, PdfFileReader
from reportlab.lib.colors import PCMYKColor
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import os
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
s=""
def Reverse(tuples):
    new_tup = ()
    for k in reversed(tuples):
        new_tup = new_tup + (k,)
    return new_tup
def LCS(X,Y):
    m=len(X)
    n=len(Y)
    c=[[0 for i in range(m+1)] for j in range(n+1)]
    b=[[0 for i in range(m+1)] for j in range(n+1)]
    if X[0].lower()==Y[0].lower():
        if m==0 or n==0:
            return
        for i in range(1,n+1):
            for j in range(1,m+1):
                if Y[i-1].upper()==X[j-1].upper():
                    c[i][j]=1+c[i-1][j-1]
                    b[i][j]="D"
                else:
                    c[i][j]=max(c[i-1][j],c[i][j-1])
                    if c[i-1][j]>c[i][j-1]:
                        b[i][j]="U"
                    else:
                        b[i][j]="L"
    return b,c
def Print_LCS(b, X, i, j):
    if i == 0 or j == 0:
        return
    if b[i][j] == "D":
        global s
        s=X[j-1]+s
        Print_LCS(b, X, i-1, j-1)
    elif b[i][j] == "U":
        Print_LCS(b, X, i-1, j)
    elif b[i][j] == "L":
        Print_LCS(b, X, i, j-1)
def checker(X,Y):
    global s
    s=""
    if len(X)>len(Y):
        t=(len(X)*90)/100
    else:
        t=(len(Y)*90)/100
    if X==Y:
       return X
    else:
        b,c=LCS(X,Y)
        Print_LCS(b,X,len(Y),len(X))
        if s != "" and len(s)>t:
            return s
if __name__=="__main__":
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    with ZipFile('sample1.zip','r') as zipObj:
        #zipObj.extractall('temp1')
        names=zipObj.namelist()
    files=[]
    index=0
    combo1=[]
    combo=[]
    checked=[]
    all_data=[]
    matched=[]
    matched_count=[]
    final_words=[]
    final_words_count=[]
    tolerate=2
    hfiles=[]
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
    for i in combo:
        f5=[]
        f6=[]
        matching=[]
        matching_count1=[]
        matching_count2=[]
        f1=files[i[0]].read()
        f2=files[i[1]].read()
        f3=f1.split('\n')
        f4=f2.split('\n')
        for ii in f3:
            k=ii.strip()
            ki=' '.join(k.split())
            if not ki.startswith("//"):
                if not ki.startswith("{"):
                    if not ki.startswith("}"):
                        if not ki == '':
                            f5.append(ki)
        for ii in f4:
            k=ii.strip()
            ki=' '.join(k.split())
            if not ki.startswith("//"):
                if not ki.startswith("{"):
                    if not ki.startswith("}"):
                        if not ki == '':
                            f6.append(ki)
        if i[0] not in checked and i[1] not in checked:
            all_data.append(f5)
            all_data.append(f6)
            checked.append(i[0])
            checked.append(i[1])
        if i[0] not in checked:
            all_data.append(f5)
            checked.append(i[0])
        if i[1] not in checked:
            all_data.append(f6)
            checked.append(i[1])
        line=((len(f5)*0.3)+(len(f6)*0.3))-1.7
        canvas=Canvas(str(i[0])+str(i[1])+".pdf", pagesize=(8*inch,((len(f5)*0.3)+(len(f6)*0.3))*inch))
        frame=Frame(0.3*inch, 0.3*inch,7.4*inch,(((len(f5)*0.3)+(len(f6)*0.3))-0.6)*inch,showBoundary=1)
        bodyStyle = ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=6)
        bodyStyle1 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=16, leading=28, spaceBefore=6)
        bodyStyle11 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=16, leading=28, spaceBefore=6,alignment=TA_CENTER)
        bodyStyle2 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=12, leading=28, spaceBefore=6,alignment=TA_CENTER)
        bodyStyle3 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=10, leading=28, spaceBefore=6,alignment=TA_CENTER)
        bodyStyle4 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=16, leading=28, spaceBefore=6,alignment=TA_CENTER)
        bodyStyle5 = ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=50)
        bodyStyle6 = ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=10,alignment=TA_CENTER)
        for p in range(len(f5)):
            if p in matching:
                ind=matching.index(p)
                matching_count2[ind]=matching_count2[ind]+1
            for q in range(p-tolerate,p+tolerate):
                if not q < 0 and not q >= len(f6):
                    value=checker(f5[p],f6[q])
                    if value != None:
                        if value not in matching:
                            matching.append(value)
                            matching_count1.append(1)
                            matching_count2.append(1)
                        else:
                            ind=matching.index(value)
                            matching_count1[ind]=matching_count1[ind]+1
        total_words=len(f5)+len(f6)
        w1=sum(matching_count1)
        w2=sum(matching_count2)
        total_match_words=w1+w2
        percent=(total_match_words/total_words)*100
        matched.append(matching)
        para1=Paragraph("Comparison between two files :  ( "+names[i[0]]+" ) & ( "+names[i[1]]+" )\n",style=bodyStyle1)
        para2=Paragraph("Plagiarism: "+str(percent)+" % , Total lines: "+str(total_words)+" & matched lines: "+str(total_match_words),style=bodyStyle3)
        para3=Paragraph("-( "+names[i[0]]+" )-",bodyStyle2)
        mydata=[para1,para2,para3]
        frame.addFromList(mydata,canvas)
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
        doc = fitz.open(str(i[0])+str(i[1])+".pdf")
        page = doc[0]
        for jp in matching:
            tru=1
            text = jp
            text_instances = page.searchFor(text)
            ### HIGHLIGHT
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
            ### OUTPUT
        doc.save(str(i[0])+str(i[1])+"h.pdf", garbage=4, deflate=True, clean=True)
        hfiles.append(str(i[0])+str(i[1])+"h.pdf")
        files[i[0]].seek(0)
        files[i[1]].seek(0)
    for it in matched[0]:
        for ids in range(1,len(matched)):
            if it in matched[ids]:
                stat=1
            else:
                stat=0
        if stat==1:
            final_words.append(it)
    for i in final_words:
        words_count=0
        for j in all_data:
            words_count=words_count+j.count(i)
        final_words_count.append(words_count)
    le=0
    final_count=0
    for i in all_data:
        le=le+len(i)
    if len(matched)==1:
        final_words=matched[0]
        for i in final_words:
            words_count=0
            for j in all_data:
                words_count=words_count+j.count(i)
            final_words_count.append(words_count)
    final_count=sum(final_words_count)
    final_percent=(final_count/le)*100
    d = Drawing(4*inch,2*inch)
    bar = HorizontalBarChart()
    bar.x = 1*inch
    bar.y = 0.4*inch
    data1 = []
    o=[]
    o.append(final_percent)
    o.append(100-final_percent)
    data1.append(o)
    bar.data = data1
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = 100
    bar.valueAxis.valueStep = 10
    bar.categoryAxis.labels.boxAnchor = 'ne'
    bar.categoryAxis.labels.dx = -5
    bar.categoryAxis.labels.fontName = 'Helvetica'
    bar.categoryAxis.categoryNames = ['Plagiarized', 'Uniqueness']
    bar.bars[(0, 0)].fillColor = colors.red
    bar.bars[(0, 1)].fillColor = colors.green
    d.add(bar, '')
    d.save(formats=['jpg'], outDir='.', fnRoot='chart')
    canvas=Canvas("0.pdf",pagesize=(8*inch,(6*inch)+(len(final_words)/1.5)*inch))
    frame=Frame(0.3*inch, 0.3*inch,7.4*inch,(6*inch)+(len(final_words)/1.5)*inch-4.3*inch)
    coverpic="temp/2.png"
    logo="temp/1.jpg"
    chart="chart.jpg"
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    canvas.drawBoundary(2,0.3*inch,0.3*inch,7.4*inch,(6*inch)+(len(final_words)/1.5)*inch-0.6*inch)
    canvas.drawImage(coverpic,0.4*inch,(6*inch)+(len(final_words)/1.5)*inch-3.9*inch,width=7.2*inch,height=3.5*inch,mask='auto')
    canvas.drawImage(logo,2.2*inch,(6*inch)+(len(final_words)/1.5)*inch-4.5*inch,width=0.5*inch,height=0.5*inch,mask='auto')
    canvas.drawImage(chart,3.5*inch,(6*inch)+(len(final_words)/1.5)*inch-10*inch,width=4*inch,height=2*inch,mask='auto')
    para1=Paragraph("The File Doctorz",bodyStyle4)
    para2=Paragraph("Client's Name : Faizan Ali",bodyStyle5)
    para3=Paragraph("Client's e-Mail : fa686319@gmail.com",bodyStyle)
    para4=Paragraph("Plagiarism Report",bodyStyle11)
    para5=Paragraph("Total Plagiarism calculated: "+str(final_percent)+" % , Total lines in all files : "+str(le)+", matched lines among all files: "+str(len(final_words))+" & theses lines occur total "+str(final_count)+" times.\n",style=bodyStyle3)
    para6=Paragraph("Further Details : ",bodyStyle1)
    mydata=[para1,para2,para3,para4,para5,para6]
    frame.addFromList(mydata,canvas)
    data = []
    # Headers
    h1 = Paragraph('''<b>Matched Words</b>''', styleBH)
    h2 = Paragraph('''<b>Count Value</b>''', styleBH)
    d1=[h1,h2]
    data.append(d1)
    for i in range(len(final_words)):
        a=[]
        v1 = Paragraph(final_words[i], styleN)
        v2 = Paragraph(str(final_words_count[i]), styleN)
        a.append(v1)
        a.append(v2)
        data.append(a)
    table = Table(data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,
                               3* cm, 3 * cm])
    table.setStyle(TableStyle([
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))
    width = 400
    height = 100
    x = 1*inch
    y = 1*inch
    table.wrapOn(canvas, width, height)
    table.drawOn(canvas, x, y)
    canvas.save()
    hfiles.append("0.pdf")
    merger = PdfFileMerger()
    files = hfiles
    for fname in sorted(files):
        merger.append(PdfFileReader(open(fname, 'rb')))
    merger.write("PlagiarismReport.pdf")
