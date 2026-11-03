"""Render six distinct listing images per language using the actual final PDFs."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import fitz,zipfile
P=Path(__file__).resolve().parent
W,H=3000,2250
GREEN='#173F35';CREAM='#F6F2E9';ORANGE='#BF542E';MUTED='#54645B'
FONT='/usr/share/fonts/truetype/dejavu/'
def ft(n,b=True):return ImageFont.truetype(FONT+('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'),n)
def text(im,s,x,y,size=44,color=GREEN,b=True,maxw=None):
 d=ImageDraw.Draw(im);f=ft(size,b)
 if maxw:
  while d.textbbox((0,0),s,font=f)[2]>maxw and size>18:size-=1;f=ft(size,b)
 d.text((x,y),s,font=f,fill=color);return y+int(size*1.45)
def lines(im,s,x,y,size=44,color=GREEN,b=True,spacing=1.22):
 for row in s.split('\n'):text(im,row,x,y,size,color,b);y+=round(size*spacing)
 return y
def base(de,dark=False):
 if dark:im=Image.new('RGB',(W,H),GREEN)
 else:im=Image.open(P/'images/etsy-background.jpg').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
 # Readability layer; retains light tabletop atmosphere.
 if not dark:
  wash=Image.new('RGB',(W,H),CREAM);im=Image.blend(im,wash,.48)
 color=CREAM if dark else GREEN;muted='#CED8C5' if dark else MUTED
 text(im,'BLACKOUT READY',410,130,34,color)
 text(im,'DEUTSCHE AUSGABE' if de else 'ENGLISH EDITION',1900,138,24,muted,maxw=690)
 d=ImageDraw.Draw(im);d.line((410,205,2590,205),fill='#6A8270' if dark else '#CCD1C2',width=2)
 return im
def footer(im,de,dark=False):
 d=ImageDraw.Draw(im);color=CREAM if dark else GREEN;muted='#CED8C5' if dark else MUTED
 d.line((410,1970,2590,1970),fill='#6A8270' if dark else '#CCD1C2',width=2)
 text(im,'DIGITALER DOWNLOAD · KEIN PHYSISCHER ARTIKEL' if de else 'DIGITAL DOWNLOAD · NO PHYSICAL ITEM',410,2010,29,color,maxw=2180)
 text(im,'12 Seiten · A4 + US Letter · Zum Ausdrucken' if de else '12 pages · A4 + US Letter · Print at home',410,2070,26,muted,False)
def sheet(im,doc,i,x,y,w,angle=0):
 pg=doc[i];pix=pg.get_pixmap(matrix=fitz.Matrix(2,2));p=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);p=p.resize((w,round(w*p.height/p.width)),Image.Resampling.LANCZOS).convert('RGBA')
 border=Image.new('RGBA',(p.width+10,p.height+10),'white');border.alpha_composite(p,(5,5));p=border
 if angle:p=p.rotate(angle,Image.Resampling.BICUBIC,expand=True)
 # Soft drop shadow created for the graphic layout.
 mask=Image.new('RGBA',im.size,(0,0,0,0));m=Image.new('RGBA',p.size,(0,0,0,0));m.putalpha(p.getchannel('A').point(lambda a:int(a*.18)));mask.alpha_composite(m,(x+18,y+28));mask=mask.filter(ImageFilter.GaussianBlur(22));im.paste(Image.alpha_composite(im.convert('RGBA'),mask).convert('RGB'))
 im.paste(p,(x,y),p)
def pill(im,s,x,y,w,dark=False):
 d=ImageDraw.Draw(im);d.rounded_rectangle((x,y,x+w,y+78),radius=39,fill='#DDE4D5' if not dark else '#36594B');text(im,s,x+28,y+18,27,CREAM if dark else GREEN,maxw=w-56)
def save(im,out,name,de):
 footer(im,de,name=='06_Lieferumfang');im.save(out/(name+'.jpg'),quality=95,subsampling=0,dpi=(300,300))
for lang in ['DE','EN']:
 de=lang=='DE';out=P/'Etsy-Bilder'/lang;out.mkdir(parents=True,exist_ok=True)
 doc=fitz.open(P/f'Blackout-Ready_{lang}_A4.pdf');letter=fitz.open(P/f'Blackout-Ready_{lang}_US-Letter.pdf')
 # 01 — main listing image: unmistakable offer with a large actual cover.
 im=base(de);text(im,'DER NOTFALLPLAN FÜR ZU HAUSE' if de else 'YOUR HOUSEHOLD POWER OUTAGE PLAN',410,330,28,ORANGE,maxw=1120)
 lines(im,'DEIN PLAN.\nMEHR\nÜBERBLICK.' if de else 'YOUR PLAN.\nMORE\nCLARITY.',402,430,115)
 lines(im,'Stromausfälle vorbereiten.\nVorräte sinnvoll planen.\nAls Haushalt organisiert bleiben.' if de else 'Prepare for power outages.\nOrganize essential supplies.\nMake a plan together.',410,920,39,b=False,spacing=1.6)
 pill(im,'12 SEITEN' if de else '12 PAGES',410,1250,300);pill(im,'2 PAPIERFORMATE' if de else '2 PAPER SIZES',735,1250,390)
 text(im,'Ratgeber + Checklisten' if de else 'Guide + checklists',410,1410,40)
 text(im,'Mit 3 Arbeitsblättern' if de else 'With 3 planning worksheets',410,1477,34,MUTED,False)
 sheet(im,doc,8,1580,470,810,angle=4);sheet(im,doc,0,1650,365,900)
 text(im,'Tatsächliches Cover der PDF-Ausgabe' if de else 'Actual cover of the PDF edition',1650,1718,23,MUTED,False,maxw=950)
 save(im,out,'01_Hero',de)
 # 02 — six-topic benefit grid.
 im=base(de);lines(im,'WAS STECKT DRIN?' if de else 'WHAT’S INSIDE?',410,300,82)
 text(im,'Sechs Themen für einen übersichtlichen Haushaltsplan.' if de else 'Six practical topics for your household plan.',410,430,37,MUTED,False,maxw=2180)
 cards=[('Start & Orientierung','Erste Schritte beim Stromausfall.'),('Wasser','Bedarf planen und sicher lagern.'),('Lebensmittel','Vorräte und Essen ohne Strom.'),('Hygiene & Gesundheit','Persönliche Bedürfnisse berücksichtigen.'),('Licht & Wärme','Risiken erkennen und Alternativen planen.'),('Kontakt & Zusammenarbeit','Treffpunkte und Unterstützung vereinbaren.')] if de else [('First actions','Know where to start during an outage.'),('Water','Plan your needs and safe storage.'),('Food','Organize supplies and no-power meals.'),('Hygiene & health','Account for individual needs.'),('Light & warmth','Recognize risks and plan alternatives.'),('Contact & cooperation','Agree meeting places and support.')]
 d=ImageDraw.Draw(im)
 for i,(title,body) in enumerate(cards):
  x=410+(i%2)*1120;y=580+(i//2)*390
  d.rounded_rectangle((x,y,x+1060,y+330),radius=18,fill='#FFFFFF',outline='#DBDFD2',width=2)
  text(im,f'0{i+1}',x+40,y+32,33,ORANGE);text(im,title,x+40,y+103,40,maxw=980);text(im,body,x+40,y+187,28,MUTED,False,maxw=980)
 save(im,out,'02_Inhalte',de)
 # 03 — honest interior previews, not invented page text.
 im=base(de);text(im,'SO SIEHT DAS HEFT AUS' if de else 'TAKE A LOOK INSIDE',410,290,78,maxw=2180)
 text(im,'Zweispaltige Kapitel, passende Bilder und kurze Checklisten.' if de else 'Two-column chapters, relevant images and quick checklists.',410,414,35,MUTED,False,maxw=2180)
 sheet(im,doc,4,510,565,875);sheet(im,doc,5,1610,565,875)
 text(im,'WASSER PLANEN' if de else 'PLAN YOUR WATER',510,1850,27,ORANGE)
 text(im,'VORRÄTE ORGANISIEREN' if de else 'ORGANIZE YOUR FOOD',1610,1850,27,ORANGE,maxw=900)
 save(im,out,'03_Blick-ins-Heft',de)
 # 04 — show the three included worksheets at useful scale.
 im=base(de);text(im,'DEIN HAUSHALT. DEIN PLAN.' if de else 'YOUR HOUSEHOLD. YOUR PLAN.',410,290,73,maxw=2180)
 text(im,'Drei Arbeitsblätter – zum Ausdrucken und Ausfüllen per Hand.' if de else 'Three worksheets — print and complete by hand.',410,417,35,MUTED,False,maxw=2180)
 for i,idx in enumerate([8,9,10]):sheet(im,doc,idx,410+i*745,620,690)
 labels=['HAUSHALTSPLAN','VORRATSLISTE','PRAXISTEST'] if de else ['HOUSEHOLD PLAN','SUPPLIES LIST','PRACTICE SESSION']
 for i,s in enumerate(labels):text(im,s,410+i*745,1670,28,maxw=690)
 text(im,'Keine interaktiven Formularfelder.' if de else 'No interactive PDF form fields.',410,1820,27,MUTED,False)
 save(im,out,'04_Arbeitsblaetter',de)
 # 05 — paper-size comparison and a simple purchase workflow.
 im=base(de);text(im,'ZWEI FORMATE. DEINE WAHL.' if de else 'TWO SIZES. YOUR CHOICE.',410,285,75,maxw=2180)
 text(im,'Der gleiche Inhalt in A4 und US Letter – kein Spezialpapier nötig.' if de else 'The same content in A4 and US Letter — no special paper needed.',410,410,34,MUTED,False,maxw=2180)
 sheet(im,doc,8,640,555,640);sheet(im,letter,8,1730,555,640)
 text(im,'A4',640,1500,42);text(im,'210 × 297 mm',640,1570,29,MUTED,False)
 text(im,'US LETTER',1730,1500,42);text(im,'8.5 × 11 in',1730,1570,29,MUTED,False)
 pill(im,'1  HERUNTERLADEN' if de else '1  DOWNLOAD',410,1765,670)
 pill(im,'2  AUSDRUCKEN' if de else '2  PRINT',1140,1765,590)
 pill(im,'3  AUSFÜLLEN' if de else '3  COMPLETE',1790,1765,780)
 save(im,out,'05_Drucken-und-Nutzen',de)
 # 06 — exact deliverables, no false physical-product impression.
 im=base(de,True);text(im,'DAS BEKOMMST DU' if de else 'WHAT YOU RECEIVE',410,295,82,CREAM)
 text(im,'Zwei PDF-Dateien in deutscher Sprache.' if de else 'Two PDF files in English.',410,435,40,'#CED8C5',False)
 dr=ImageDraw.Draw(im)
 for x,name,detail in [(410,'PDF / A4','12 SEITEN' if de else '12 PAGES'),(1540,'PDF / US LETTER','12 SEITEN' if de else '12 PAGES')]:
  dr.rounded_rectangle((x,620,x+1040,1115),radius=24,fill=CREAM)
  dr.rounded_rectangle((x+55,680,x+195,850),radius=10,fill='#E1E8D9')
  text(im,'PDF',x+74,738,40,GREEN)
  text(im,name,x+55,915,45,GREEN,maxw=920);text(im,detail+' · '+lang,x+55,1000,28,MUTED,False)
 lines(im,'12 Seiten je PDF in zwei Papierformaten.' if de else '12 pages per PDF in two paper sizes.',410,1240,42,CREAM)
 lines(im,'Gleicher Inhalt in beiden Dateien.\nDigitales Produkt – kein gedrucktes Buch.\nZum Lesen, Ausdrucken und handschriftlichen Planen.' if de else 'The same content in both files.\nDigital product — no printed book included.\nRead, print and complete your plan by hand.',410,1390,36,'#CED8C5',False,1.7)
 save(im,out,'06_Lieferumfang',de)
 with zipfile.ZipFile(P/f'Etsy-Bilder-{lang}.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(out.glob('*.jpg')):z.write(f,lang+'/'+f.name)
 print(lang,'six 3000 × 2250 listing images created')
