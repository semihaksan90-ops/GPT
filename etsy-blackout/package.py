from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import fitz,zipfile,shutil
P=Path(__file__).resolve().parent
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(s,bold=True):return ImageFont.truetype(F if bold else R,s)
def page(doc,i,w):
 pix=doc[i].get_pixmap(matrix=fitz.Matrix(2,2));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);h=round(w*im.height/im.width);return im.resize((w,h),Image.Resampling.LANCZOS)
for lang in ['DE','EN']:
 de=lang=='DE';doc=fitz.open(P/f'Blackout-Ready_{lang}_A4.pdf')
 specs=[('cover',[0,4], 'VORBEREITET. MIT PLAN.' if de else 'PREPARED. WITH A PLAN.', 'Bebilderter Haushaltsratgeber & Checklisten' if de else 'Illustrated household guide & checklists'),('inside',[4,5], 'KLAR. PRAKTISCH. ÜBERSICHTLICH.' if de else 'CLEAR. PRACTICAL. ORGANIZED.', 'Wasser, Vorräte, Hygiene & Kommunikation' if de else 'Water, food, hygiene & communication'),('worksheets',[8,9,10], 'DEIN PERSÖNLICHER PLAN' if de else 'MAKE THE PLAN YOURS', 'Drei Arbeitsblätter zum handschriftlichen Ausfüllen' if de else 'Three worksheets to complete by hand'),('contents',[1,3], '12 SEITEN FÜR DEINEN HAUSHALT' if de else '12 PAGES FOR YOUR HOUSEHOLD', 'Wissen ordnen. Vorräte prüfen. Gemeinsam planen.' if de else 'Organize information. Check supplies. Plan together.'),('formats',[0,8], 'A4 + US LETTER' if de else 'A4 + US LETTER', 'Eine Sprache · zwei Papierformate · gleicher Inhalt' if de else 'One language · two paper sizes · the same content')]
 for name,pages,title,sub in specs:
  im=Image.new('RGB',(2400,1800),'#EDEAE0');dr=ImageDraw.Draw(im)
  dr.rectangle((0,0,2400,298),fill='#173F35');dr.text((104,48),'BLACKOUT READY',font=font(25),fill='#D6DFC9')
  dr.text((100,101),title,font=font(61),fill='#F6F2E9');dr.text((104,205),sub,font=font(32,False),fill='#D6DFC9')
  w=805 if len(pages)==2 else 720;gap=65 if len(pages)==2 else 38
  total=len(pages)*w+(len(pages)-1)*gap;x=(2400-total)//2
  for idx,i in enumerate(pages):
   pg=page(doc,i,w);y=354 if len(pages)==2 else 375
   dr.rectangle((x+14,y+14,x+w+14,y+pg.height+14),fill='#C6CBBC');im.paste(pg,(x,y));x+=w+gap
  dr.rectangle((0,1630,2400,1800),fill='#F6F2E9')
  dr.text((104,1665),('DEUTSCH' if de else 'ENGLISH')+'  /  12 '+('SEITEN' if de else 'PAGES')+'  /  A4 + US LETTER',font=font(34),fill='#173F35')
  dr.text((104,1724), 'DIGITALER DOWNLOAD · KEIN PHYSISCHER ARTIKEL' if de else 'DIGITAL DOWNLOAD · NO PHYSICAL PRODUCT',font=font(24,False),fill='#54645B')
  im.save(P/f'Etsy_{lang}_{name}.jpg',quality=94)
for lang in ['DE','EN','Bilingual']:
 files=sorted(P.glob('Blackout-Ready_*.pdf' if lang=='Bilingual' else f'Blackout-Ready_{lang}_*.pdf'))
 with zipfile.ZipFile(P/f'BLACKOUT-READY-{lang}.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in files:z.write(f,f.name)
with zipfile.ZipFile(P/'Etsy-Verkaufsmaterial.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(P.glob('Etsy_*.jpg')):z.write(f,f.name)
 z.write(P/'Etsy-Texte.md','Etsy-Texte.md')
# Assemble a fresh seller folder; this is generated output, not a user source directory.
out=P.parent.parent/'Etsy-Blackout-Ready-Edition-2'
out.mkdir(exist_ok=True)
for sub in ['Deutsch','English','Etsy-Verkaufsmaterial','Bearbeitbare-Quelldateien/images']:(out/sub).mkdir(parents=True,exist_ok=True)
for lang,sub in [('DE','Deutsch'),('EN','English')]:
 for f in P.glob(f'Blackout-Ready_{lang}_*.pdf'):shutil.copy2(f,out/sub/f.name)
for f in P.glob('Etsy_*.jpg'):shutil.copy2(f,out/'Etsy-Verkaufsmaterial'/f.name)
shutil.copy2(P/'Etsy-Texte.md',out/'Etsy-Verkaufsmaterial/Etsy-Texte.md')
for name in ['build.py','package.py','content.json','requirements.txt','FONT-LICENSE.txt']:
 shutil.copy2(P/name,out/'Bearbeitbare-Quelldateien'/name)
for f in (P/'images').glob('*.jpg'):shutil.copy2(f,out/'Bearbeitbare-Quelldateien/images'/f.name)
(out/'LIES-MICH.txt').write_text('BLACKOUT READY — Ausgabe 2\n\nDeutsch / English: Je 12 Seiten, jeweils A4 und US Letter.\nEtsy-Verkaufsmaterial: 10 Produktbilder und deutsche/englische Beschreibungstexte.\nBearbeitbare-Quelldateien: Generator, Bilddateien und Textdaten, nicht für Käufer.\n\nNeu: fotografisches Cover, drei KI-generierte Motive, zweispaltige Kapitel, Inhaltsverzeichnis, drei Arbeitsblätter.\nDie PDFs sind für handschriftliche Einträge gedacht, keine interaktiven Formularfelder.\n\nVor Verkauf: Sicherheitshinweise anhand aktueller offizieller Empfehlungen prüfen. Produktbilder/Illustrationen sind KI-generiert. Keine Veröffentlichung auf Etsy erfolgt.\n\nQuelldateien: Python 3 mit Paketen aus requirements.txt und DejaVu-Sans-/Serif-Schriftdateien in den in build.py hinterlegten Linux-Pfaden. In build.py die Texte im DATA-Abschnitt bearbeiten; content.json ist ein exportierter Textstand. Dann build.py ausführen. package.py erstellt neue Produktbilder und ZIPs.\n',encoding='utf-8')
archive=shutil.make_archive(str(P.parent/'Etsy-Blackout-Ready'),'zip',root_dir=out.parent,base_dir=out.name)
print(archive)
