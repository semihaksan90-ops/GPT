from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import fitz,zipfile,shutil
P=Path(__file__).resolve().parent
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(s,bold=True):return ImageFont.truetype(F if bold else R,s)
def page(doc,i,w):
 pix=doc[i].get_pixmap(matrix=fitz.Matrix(2,2));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);h=round(w*im.height/im.width);return im.resize((w,h),Image.Resampling.LANCZOS)
import runpy
runpy.run_path(str(P/'marketing.py'),run_name='__main__')
for lang in ['DE','EN','Bilingual']:
 files=sorted(P.glob('Blackout-Ready_*.pdf' if lang=='Bilingual' else f'Blackout-Ready_{lang}_*.pdf'))
 with zipfile.ZipFile(P/f'BLACKOUT-READY-{lang}.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in files:z.write(f,f.name)
with zipfile.ZipFile(P/'Etsy-Verkaufsmaterial.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted((P/'Etsy-Bilder').rglob('*.jpg')):z.write(f,str(f.relative_to(P/'Etsy-Bilder')))
 z.write(P/'Bilder-Anleitung.md','Bilder-Anleitung.md')
 z.write(P/'Etsy-Texte.md','Etsy-Texte.md')
# Assemble a fresh seller folder; this is generated output, not a user source directory.
out=P.parent.parent/'Etsy-Blackout-Ready-Geprueft'
out.mkdir(exist_ok=True)
for sub in ['Deutsch','English','Etsy-Verkaufsmaterial/Deutsch','Etsy-Verkaufsmaterial/English','Bearbeitbare-Quelldateien/images']:(out/sub).mkdir(parents=True,exist_ok=True)
for lang,sub in [('DE','Deutsch'),('EN','English')]:
 for f in P.glob(f'Blackout-Ready_{lang}_*.pdf'):shutil.copy2(f,out/sub/f.name)
for lang,sub in [('DE','Deutsch'),('EN','English')]:
 for f in (P/'Etsy-Bilder'/lang).glob('*.jpg'):shutil.copy2(f,out/'Etsy-Verkaufsmaterial'/sub/f.name)
shutil.copy2(P/'Bilder-Anleitung.md',out/'Etsy-Verkaufsmaterial/Bilder-Anleitung.md')
shutil.copy2(P/'Etsy-Texte.md',out/'Etsy-Verkaufsmaterial/Etsy-Texte.md')
shutil.copy2(P/'VOR-DEM-UPLOAD.md',out/'VOR-DEM-UPLOAD.md')
for name in ['build.py','package.py','marketing.py','preflight.py','content.json','requirements.txt','FONT-LICENSE.txt']:
 shutil.copy2(P/name,out/'Bearbeitbare-Quelldateien'/name)
for f in (P/'images').glob('*.jpg'):shutil.copy2(f,out/'Bearbeitbare-Quelldateien/images'/f.name)
(out/'LIES-MICH.txt').write_text('BLACKOUT READY — geprüfte Fassung 2.1\n\nDeutsch / English: Je 12 Seiten, jeweils A4 und US Letter.\nEtsy-Verkaufsmaterial: 12 Produktbilder (je Sprache 1 Hero + 5 weitere Bilder) und deutsche/englische Beschreibungstexte.\nBearbeitbare-Quelldateien: Generator, Bilddateien und Textdaten, nicht für Käufer.\n\nNeu: fotografisches Cover, drei KI-generierte Motive im Heft sowie KI-generierter Hintergrund für die Produktbilder, zweispaltige Kapitel, Inhaltsverzeichnis, drei Arbeitsblätter.\nDie PDFs sind für handschriftliche Einträge gedacht, keine interaktiven Formularfelder.\n\nVor Verkauf: Sicherheitshinweise anhand aktueller offizieller Empfehlungen prüfen. Produktbilder/Illustrationen sind KI-generiert. Keine Veröffentlichung auf Etsy erfolgt.\n\nQuelldateien: Python 3 mit Paketen aus requirements.txt und DejaVu-Sans-/Serif-Schriftdateien in den in build.py hinterlegten Linux-Pfaden. In build.py die Texte im DATA-Abschnitt bearbeiten; content.json ist ein exportierter Textstand. Dann build.py ausführen. package.py erstellt neue Produktbilder und ZIPs.\n',encoding='utf-8')
# One seller upload pack per language, with customer files clearly separated.
listing=(P/'Etsy-Texte.md').read_text()
for lang in ['DE','EN']:
 section=listing.split('# Deutsche Anzeige',1)[1].split('# English listing',1)[0].strip() if lang=='DE' else listing.split('# English listing',1)[1].split('# Optional bilingual bundle',1)[0].strip()
 with zipfile.ZipFile(P/f'Etsy-Upload-{lang}.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(P.glob(f'Blackout-Ready_{lang}_*.pdf')):z.write(f,'Kundendateien/'+f.name)
  for f in sorted((P/'Etsy-Bilder'/lang).glob('*.jpg')):z.write(f,'Produktbilder/'+f.name)
  z.writestr('Listing-'+lang+'.txt',section)
  z.write(P/'VOR-DEM-UPLOAD.md','VOR-DEM-UPLOAD.md')
archive=shutil.make_archive(str(P.parent/'Etsy-Blackout-Ready'),'zip',root_dir=out.parent,base_dir=out.name)
print(archive)
