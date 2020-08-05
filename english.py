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
s=" "
def Reverse(tuples):
    new_tup = ()
    for k in reversed(tuples):
        new_tup = new_tup + (k,)
    return new_tup
if __name__=="__main__":
    with ZipFile('sample.zip','r') as zipObj:
        #zipObj.extractall('temp')
        names=zipObj.namelist()
    files=[]
    index=0
    combo1=[]
    combo=[]
    matched=[]
    percent_list=[]
    checked=[]
    all_data=[]
    final_words=[]
    final_words_count=[]
    hfiles=[]
    for c, x in enumerate(names):
        f = open ('temp/'+str(x),'r')
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
        matching=[]
        matching_count1=[]
        matching_count2=[]
        f3=[]
        f4=[]
        f1=files[i[0]].read()
        f2=files[i[1]].read()
        f33=f1.split('\n')
        f44=f2.split('\n')
        count=0
        for ii in f33:
            if ii=='':
                f33.pop(count)
            count=count+1
        count=0
        for ii in f44:
            if ii=='':
                f44.pop(count)
            count=count+1
        f5=''.join(f33)
        f6=''.join(f44)
        l1=f5.split('.')
        l2=f6.split('.')
        count=0
        for ii in l1:
            if ii=='':
                l1.pop(count)
            count=count+1
        count=0
        for ii in l2:
            if ii=='':
                l2.pop(count)
            count=count+1
        l3=''.join(l1)
        l4=''.join(l2)
        f3=l3.split(' ')
        f4=l4.split(' ')
        canvas=Canvas(str(i[0])+str(i[1])+".pdf", pagesize=(8*inch,((len(f33)*1)+(len(f44)*1))*inch))
        frame=Frame(0.3*inch, 0.3*inch,7.4*inch,(((len(f33)*1)+(len(f44)*1))-0.6)*inch,showBoundary=1)
        bodyStyle = ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=6)
        bodyStyle1 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=16, leading=28, spaceBefore=6)
        bodyStyle11 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=16, leading=28, spaceBefore=6,alignment=TA_CENTER)
        bodyStyle2 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=12, leading=28, spaceBefore=6,alignment=TA_CENTER)
        bodyStyle3 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=10, leading=28, spaceBefore=6,alignment=TA_CENTER)
        bodyStyle4 = ParagraphStyle('Body', fontName="Helvetica-bold", fontSize=16, leading=28, spaceBefore=6,alignment=TA_CENTER)
        bodyStyle5 = ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=50)
        bodyStyle6 = ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=10,alignment=TA_CENTER)
        if i[0] not in checked and i[1] not in checked:
            all_data.append(f3)
            all_data.append(f4)
            checked.append(i[0])
            checked.append(i[1])
        if i[0] not in checked:
            all_data.append(f3)
            checked.append(i[0])
        if i[1] not in checked:
            all_data.append(f4)
            checked.append(i[1])
        for p in f3:
            count=1
            if p.lower() in matching:
                ind=matching.index(p.lower())
                if ind>=0:
                    matching_count1[ind]=matching_count1[ind]+1
            else:
                for q in f4:
                    if p.lower()==q.lower():
                        if count==1:
                            matching.append(p.lower())
                            matching_count1.append(1)
                            matching_count2.append(1)
                            count=2
                        else:
                            ind=matching.index(p.lower())
                            if ind>=0:
                                matching_count2[ind]=matching_count2[ind]+1
        
        #print("Matching words' count value in "+names[i[0]]+" is :",matching_count1)
        #print("Matching words' count value in "+names[i[1]]+" is :",matching_count2)
        total_words=len(f3)+len(f4)
        w1=sum(matching_count1)
        w2=sum(matching_count2)
        total_match_words=w1+w2
        percent=(total_match_words/total_words)*100
        matched.append(matching)
        percent_list.append(percent)
        #print("percentage of Matching words in "+names[i[0]]+" and "+names[i[1]]+" is :"+str(percent)+" %")
        para1=Paragraph("Comparison between two files :  ( "+names[i[0]]+" ) & ( "+names[i[1]]+" )\n",style=bodyStyle1)
        para2=Paragraph("Plagiarism: "+str(percent)+" % , Total words: "+str(total_words)+" & matched words: "+str(total_match_words),style=bodyStyle3)
        para3=Paragraph("-( "+names[i[0]]+" )-",bodyStyle2)
        para4=Paragraph(f1,style=bodyStyle)
        para5=Paragraph("-( "+names[i[1]]+" )-",bodyStyle2)
        para6=Paragraph(f2,style=bodyStyle)
        mydata=[para1,para2,para3,para4,para5,para6]
        frame.addFromList(mydata,canvas)
        canvas.save()
        doc = fitz.open(str(i[0])+str(i[1])+".pdf")
        page = doc[0]
        for jp in matching:
            text = " "+jp+" "
            text_instances = page.searchFor(text)
            ### HIGHLIGHT
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
            ### OUTPUT
        doc.save(str(i[0])+str(i[1])+"h.pdf", garbage=4, deflate=True, clean=True)
        hfiles.append(str(i[0])+str(i[1])+"h.pdf")
        files[i[0]].seek(0)
        files[i[1]].seek(0)
    stat=0
    pstat=1
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
    final_count=sum(final_words_count)
    final_percent=(final_count/le)*100
    #print("All Common words in all files :",final_words)
    #print("Count value of above words",final_words_count)
    #print("Total percentage :"+str(final_percent)+" %")
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
    para5=Paragraph("Total Plagiarism calculated: "+str(final_percent)+" % , Total words in all files : "+str(le)+", matched words among all files: "+str(len(final_words))+" & theses words occur total "+str(final_count)+" times.\n",style=bodyStyle3)
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
