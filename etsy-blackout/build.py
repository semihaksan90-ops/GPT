from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import fitz, zipfile, json
OUT=Path(__file__).parent
for name,file in [('Regular','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFont(TTFont('Editorial','/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
GREEN='#173F35'; CREAM='#F6F2E9'; INK='#20382F'; MUTED='#54645B'; ORANGE='#BF542E'
DATA={
'de':{
 'sub':'Dein Notfallplan für zu Hause','tag':'VORBEREITEN. ORDNEN. RUHIG HANDELN.',
 'desc':'Ein kompakter Ratgeber mit druckbaren Checklisten und Platz für deinen persönlichen Haushaltsplan.',
 'topics':'WASSER / VORRÄTE / HYGIENE / KOMMUNIKATION',
 'pages':[
 ('So nutzt du diesen Plan','Ein überschaubarer Anfang',[
 ('Dein Ziel','Bereite deinen Haushalt schrittweise auf einen Stromausfall vor. Beginne mit dem, was du schon hast, und ergänze gezielt. Dieses Heft ist ein Planungshelfer; es verspricht keine Versorgung für eine bestimmte Anzahl von Tagen.'),
 ('Deine erste Runde','Gehe die Themen Wasser, Essen, Licht, Hygiene und Kontakt durch. Fülle die Arbeitsblätter aus und bewahre einen Ausdruck bei deinen Vorräten auf. Besprich den Plan mit allen im Haushalt.'),
 ('Individuelle Bedürfnisse','Berücksichtige Kinder, ältere Menschen, Menschen mit Behinderungen, Haustiere und medizinische Geräte. Wer auf strombetriebene Hilfsmittel angewiesen ist, braucht vorab einen abgestimmten Ersatz- und Evakuierungsplan mit dem Versorgungsteam.'),
 ('Grenzen und Hilfe','Offizielle Anweisungen vor Ort haben Vorrang. Bei unmittelbarer Gefahr suche Hilfe und verlasse gefährdete Bereiche. In Deutschland und der EU gilt 112; außerhalb der EU prüfe die örtliche Notrufnummer. Dieses Heft ersetzt keine medizinische Beratung oder Erste-Hilfe-Ausbildung.')],
 ['Vorräte und Notfalltasche an einem bekannten Ort lagern','Alle im Haushalt kennen den Plan und den Treffpunkt','Plan alle sechs Monate und nach Veränderungen prüfen']),
 ('Wenn der Strom ausfällt','Die ersten Schritte',[
 ('Zuerst Sicherheit','Nutze eine Taschenlampe. Prüfe, ob jemand verletzt ist oder dringend Unterstützung braucht. Bei Rauch, Gasgeruch oder anderer unmittelbarer Gefahr bring dich in Sicherheit und verständige die zuständige Notfallstelle von einem sicheren Ort.'),
 ('Lage klären','Prüfe gefahrlos, ob auch die Umgebung betroffen ist. Nutze ein batteriebetriebenes Radio und offizielle Meldungen. Gehe nicht an beschädigte Leitungen und öffne keine elektrischen Anlagen.'),
 ('Haushalt stabilisieren','Halte Kühl- und Gefriergeräte geschlossen. Schalte Kochgeräte und empfindliche Elektronik aus. Lass eine elektrische Lampe eingeschaltet, damit du erkennst, wenn die Versorgung zurückkehrt.'),
 ('Kontakt und Energie','Informiere deine vereinbarte Kontaktperson, soweit das Netz verfügbar ist. Nutze kurze Nachrichten, senke die Displayhelligkeit und halte eine geladene Powerbank bereit. Belege Notrufleitungen nicht mit allgemeinen Auskunftsfragen.')],
 ['Alle Personen im Haushalt berücksichtigen','Offizielle Informationen verfolgen','Kühlgeräte geschlossen lassen','Vereinbarten Kontakt- und Treffpunktplan nutzen']),
 ('Wasser organisieren','Trinken und Hygiene getrennt planen',[
 ('Bedarf aufschreiben','Notiere Personen, Planungstage und deinen täglichen Trink- und Kochwasserbedarf. Orientiere dich an aktuellen Empfehlungen deiner örtlichen Behörden. Hitze, Krankheit und besondere Bedürfnisse können mehr Wasser erfordern. Hygiene und Haustiere kommen zusätzlich dazu.'),
 ('Sicher lagern','Nutze original verschlossene Flaschen oder saubere, lebensmittelechte Behälter für Trinkwasser. Lagere sie kühl, dunkel und fern von Chemikalien. Beschrifte selbst befüllte Behälter und prüfe Vorräte regelmäßig.'),
 ('Warnungen ernst nehmen','Bei einer Trinkwasserwarnung gelten die örtlichen Vorgaben. Abkochen entfernt keine chemischen Verunreinigungen. Haushaltsfilter machen nicht jedes Wasser sicher; beachte die ausdrücklich angegebenen Leistungen und Grenzen des Herstellers.'),
 ('Praktisch verteilen','Stelle Trinkwasser an einem gut erreichbaren Ort bereit. Kennzeichne Nichttrinkwasser eindeutig und halte es getrennt. Nutze keine Behälter, die zuvor Kraftstoff, Reiniger oder andere gefährliche Stoffe enthielten.')],
 ['Trinkwasserbedarf auf dem Vorratsblatt berechnen','Zusatzbedarf für Hygiene und Tiere erfassen','Saubere Behälter und einen Vorratswechsel einplanen']),
 ('Essen ohne Strom','Ein Vorrat, der zu deinem Alltag passt',[
 ('Einfach auswählen','Bevorzuge haltbare Lebensmittel, die dein Haushalt bereits mag und verträgt. Ergänze verzehrfertige Speisen, einen manuellen Dosenöffner und Lebensmittel, die wenig oder kein Wasser benötigen. Allergien und spezielle Ernährung gehören in deinen Plan.'),
 ('Kühlung schützen','Halte Türen von Kühl- und Gefriergeräten geschlossen und nutze ein Gerätethermometer. Ob Lebensmittel noch sicher sind, hängt von Temperatur, Dauer und Lebensmittelart ab. Prüfe aktuelle behördliche Tabellen, statt pauschal alles weiterzuverwenden.'),
 ('Keine Geschmacksprobe','Krankmachende Keime sind nicht zuverlässig an Geruch oder Aussehen erkennbar. Probiere verdächtige Lebensmittel nicht, um ihre Sicherheit zu testen. Im Zweifel entsorge leicht verderbliche Ware.'),
 ('Sicher zubereiten','Plane möglichst ohne offenes Feuer. Grills, Holzkohle und kraftstoffbetriebene Generatoren gehören niemals in Wohnräume, Garagen oder Keller. Auch ein offenes Fenster macht sie dort nicht sicher. Brennstoffbetriebene Campingkocher nur im Freien und nach Herstellerangaben verwenden.')],
 ['Drei einfache Mahlzeiten ohne Strom planen','Manuellen Dosenöffner bereitlegen','Mindesthaltbarkeit und Vorratswechsel notieren']),
 ('Hygiene und Gesundheit','Sauber bleiben und Hilfe vorbereiten',[
 ('Hände und Abfall','Plane Seife, sauberes Wasser, Toilettenpapier, Hygieneartikel und geeignete Abfallbeutel ein. Wasche Hände besonders nach Toilettengängen und vor dem Essen. Befolge lokale Hinweise zur Wassernutzung und Abfallentsorgung.'),
 ('Toilette und Abwasser','Bei Ausfall von Wasser oder Abwasser kläre die örtlichen Vorgaben. Spüle nicht weiter, wenn Abwasser zurückstaut. Bereite eine geeignete Ersatzlösung vor und halte Ausscheidungen von Lebensmitteln und Wasserquellen fern.'),
 ('Medikamente','Führe eine aktuelle Medikamentenliste mit Kontaktdaten von Praxis und Apotheke. Kläre Vorrat, Kühlanforderungen und einen Versorgungsplan im Voraus. Dosierungen nicht selbst verändern; für kühlpflichtige Mittel gelten produktspezifische Vorgaben.'),
 ('Erste Hilfe vorbereiten','Halte ein zugängliches Erste-Hilfe-Set bereit und erneuere deine Kenntnisse in einem anerkannten Kurs. Speichere wichtige Gesundheitsinformationen auch auf Papier. Bei schweren Beschwerden oder Verletzungen professionelle Hilfe anfordern.')],
 ['Persönliche Hygiene- und Pflegeprodukte ergänzen','Medikamenten- und Geräteplan mit Fachpersonen klären','Erste-Hilfe-Set prüfen und Kurs auffrischen']),
 ('Wärme, Licht und Kontakt','Risiken klein halten',[
 ('Licht ohne Flamme','Bevorzuge LED-Taschenlampen und Stirnlampen. Halte passende Batterien bereit. Prüfe Rauchwarnmelder und gegebenenfalls CO-Warnmelder nach Herstellerangaben. Ein CO-Warnmelder ersetzt niemals eine sichere Nutzung von Geräten.'),
 ('Temperatur im Blick','Nutze bei Kälte mehrere Kleidungsschichten und Decken. Bei Hitze meide direkte Sonne und starke körperliche Belastung. Suche rechtzeitig einen sicheren anderen Ort auf, wenn die Wohnung für deinen Haushalt zu kalt oder zu heiß wird.'),
 ('Kohlenmonoxid vermeiden','Betreibe kraftstoffbetriebene Generatoren ausschließlich draußen, weit entfernt von Fenstern, Türen und Lüftungsöffnungen nach Hersteller- und Behördenvorgaben. Nicht in Hausinstallationen einspeisen: Dafür ist fachgerecht installierte Umschalttechnik erforderlich.'),
 ('Verbunden bleiben','Notiere einen Treffpunkt in der Nähe und eine Alternative außerhalb des Viertels. Vereinbare eine Kontaktperson außerhalb der Region. Besprich Unterstützung mit Nachbarn freiwillig und ohne sensible Daten unnötig weiterzugeben.')],
 ['Taschenlampe nachts griffbereit lagern','Radio und Batterien testen','Treffpunkt und Kontaktperson eintragen'])],
 'plan':'Mein Haushaltsplan','plan_sub':'Gemeinsam ausfüllen und zugänglich aufbewahren.',
 'fields':['Haushalt / Anzahl Personen / Haustiere','Kontaktperson außerhalb der Region / Telefon','Treffpunkt in der Nähe','Alternativer Treffpunkt / sicherer Ausweichort','Besondere Bedürfnisse / vereinbarte Unterstützung','Notruf / Praxis / Apotheke / wichtige Telefonnummern','Ort von Vorräten, Radio und Erste-Hilfe-Set','Geprüft am / nächster Prüftermin'],
 'stock':'Vorräte und Aufgaben','stock_sub':'Gezielt ergänzen statt wahllos einkaufen.',
 'headers':['Bereich / Artikel','Vorhanden','Ergänzen / prüfen'],
 'rows':['Trink- und Kochwasser','Hygienewasser / Haustiere','Verzehrfertige Lebensmittel','Spezielle Ernährung','Dosenöffner / Geschirr','Lampen / Batterien','Radio / Powerbanks','Hygiene / Abfallbeutel','Erste Hilfe / persönliche Pflege','Medikamente: Versorgungsplan','Dokumente / Bargeld','Notfalltasche / Kleidung'],
 'calc':'Wasserplanung: ____ Personen × ____ Tage × ____ Liter pro Tag = ____ Liter. Zusatzbedarf: ____ Liter. Annahmen mit örtlichen Empfehlungen abgleichen.',
 'tasks':'Meine nächsten drei Aufgaben',
 'ref':'Quellen und nächste Schritte','refsub':'Aktuelle Hinweise haben Vorrang.',
 'refs_intro':'Die folgenden offiziellen Anlaufstellen bieten weiterführende Empfehlungen. Prüfe vor der Nutzung aktuelle Inhalte und die Vorgaben für deinen Wohnort. Diese deutsche Fassung dient der allgemeinen Haushaltsplanung. Ergänze regionale Kontaktdaten und beachte die örtlichen Regeln.',
 'last':'Vor dem nächsten Stromausfall',
 'finalchecks':['Plan mit allen Personen im Haushalt besprechen','Radio und Lampen ausprobieren; Powerbanks laden','Kontaktliste und Treffpunkte gemeinsam prüfen','Neue Vorräte nach hinten, ältere nach vorn stellen','Datum zur nächsten Überprüfung eintragen'],
 'notice':'Allgemeiner Planungsratgeber, keine individuelle medizinische oder technische Beratung. Keine Garantie für die Bewältigung einer bestimmten Ausfalldauer. Keine Verbindung zu den genannten Behörden. Ausgabe 1.0 · 2026.',
 'print':'Druckhinweis: Bei 100 % / tatsächlicher Größe drucken. Für handschriftliche Einträge vorgesehen; keine interaktiven PDF-Formularfelder.'},
'en':{
 'sub':'Your household power outage plan','tag':'PREPARE. ORGANIZE. STAY CALM.',
 'desc':'A practical guide with printable checklists and space to build your own household plan.',
 'topics':'WATER / FOOD / HYGIENE / COMMUNICATION',
 'pages':[
 ('Make this plan yours','Start with a manageable step',[
 ('Your goal','Prepare your household for a power outage in practical stages. Start with what you already own and fill specific gaps. This booklet is a planning tool; it does not promise supplies or safety for a fixed number of days.'),
 ('Your first review','Work through water, food, lighting, hygiene and communication. Complete the worksheets and keep a printed copy with your supplies. Discuss the plan with everyone in your household.'),
 ('Individual needs','Plan separately for children, older adults, disabilities, pets and medical equipment. Anyone relying on powered medical devices needs a backup and evacuation plan agreed in advance with their care and equipment providers.'),
 ('Limits and help','Follow current local official instructions. Seek help and leave unsafe areas when there is immediate danger. Write your local emergency number on the household plan. This booklet does not replace medical advice or recognized first aid training.')],
 ['Keep supplies and a grab bag in a known location','Make sure everyone knows the plan and meeting place','Review every six months and after household changes']),
 ('When the power goes out','Your first actions',[
 ('Check safety first','Use a flashlight. Check whether anyone is injured or needs urgent support. If you notice smoke, a gas smell or another immediate hazard, move to safety and contact the appropriate emergency service from a safe location.'),
 ('Understand the situation','If safe, check whether nearby properties are affected. Use a battery-powered radio and official updates. Stay away from damaged power lines and do not open electrical equipment.'),
 ('Stabilize the household','Keep refrigerators and freezers closed. Switch off cooking appliances and sensitive electronics. Leave one safe light switched on so you can see when power returns.'),
 ('Conserve communication power','Contact your agreed person if networks are available. Use brief messages, reduce screen brightness and keep a charged power bank ready. Do not call emergency lines for general outage information.')],
 ['Account for everyone in the household','Follow official updates','Keep cold appliances closed','Use the agreed contact and meeting plan']),
 ('Organize your water','Plan drinking and hygiene needs separately',[
 ('Write down your needs','Record the number of people, planning days and daily drinking and cooking water needs. Use current local authority recommendations. Heat, illness and individual needs may increase requirements. Add hygiene water and pet needs separately.'),
 ('Store safely','Use factory-sealed bottles or clean containers approved for drinking water. Store in a cool, dark place away from chemicals. Label containers you fill yourself and check your stock regularly.'),
 ('Take advisories seriously','Follow local instructions during a drinking water advisory. Boiling does not remove chemical contamination. Household filters do not make all water safe; check the manufacturer’s stated capabilities and limitations.'),
 ('Make access practical','Keep drinking water accessible. Clearly label non-drinking water and store it separately. Never use containers that previously held fuel, cleaners or other hazardous substances.')],
 ['Calculate drinking and cooking water on the supply sheet','Add hygiene and pet needs','Plan clean containers and stock rotation']),
 ('Food without power','Supplies that fit your everyday life',[
 ('Choose simple options','Favor shelf-stable foods your household already eats and tolerates. Include ready-to-eat meals, a manual can opener and foods needing little or no water. Account for allergies and special diets.'),
 ('Protect cold storage','Keep refrigerator and freezer doors closed and use an appliance thermometer. Food safety depends on temperature, time and food type. Check current official food safety tables rather than assuming all stored food is safe.'),
 ('Never taste-test safety','Harmful bacteria cannot reliably be detected by smell or appearance. Do not taste questionable food to decide whether it is safe. When in doubt, discard perishable food.'),
 ('Prepare meals safely','Plan meals without open flames where possible. Never use grills, charcoal or generators inside a home, garage or basement. An open window does not make indoor use safe. Use fuel-burning camping stoves outdoors only and follow the manufacturer’s instructions.')],
 ['Plan three easy meals without electricity','Keep a manual can opener available','Record expiry checks and stock rotation']),
 ('Hygiene and health','Plan for cleanliness and care',[
 ('Hands and waste','Include soap, clean water, toilet paper, personal hygiene items and suitable waste bags. Wash hands especially after toilet use and before eating. Follow local instructions for water use and waste collection.'),
 ('Toilets and wastewater','If water or sewage service fails, check local guidance. Stop flushing if sewage backs up. Prepare an appropriate alternative and keep human waste away from food and water sources.'),
 ('Medication planning','Keep an up-to-date medication list and contact details for your clinician and pharmacy. Discuss supplies, cooling requirements and continuity of care in advance. Do not change doses yourself; temperature-sensitive medicines have product-specific requirements.'),
 ('Prepare for first aid','Keep an accessible first aid kit and refresh skills through a recognized course. Store essential health information on paper as well as digitally. Seek professional help for serious symptoms or injuries.')],
 ['Add personal hygiene and care products','Agree medication and equipment plans with professionals','Check the first aid kit and refresh training']),
 ('Warmth, light and contact','Reduce avoidable risks',[
 ('Choose flameless lighting','Use LED flashlights and headlamps where possible. Store suitable batteries. Check smoke alarms and, where appropriate, carbon monoxide alarms according to manufacturer instructions. An alarm never replaces safe appliance use.'),
 ('Watch the temperature','Use layers and blankets in cold conditions. In hot weather, avoid direct sun and strenuous activity. Move to a safe alternative location early if your home becomes too hot or cold for your household.'),
 ('Prevent carbon monoxide exposure','Operate fuel-powered generators outdoors only, far from doors, windows and vents, following manufacturer and local authority guidance. Never feed power into household wiring without professionally installed transfer equipment.'),
 ('Stay connected','Choose a nearby meeting place and an alternative outside your neighborhood. Agree on an out-of-area contact. Arrange voluntary support with neighbors while protecting private information.')],
 ['Keep a flashlight within reach at night','Test the radio and batteries','Write down meeting places and a contact person'])],
 'plan':'My household plan','plan_sub':'Complete together and keep accessible.',
 'fields':['Household / number of people / pets','Out-of-area contact / phone','Nearby meeting place','Alternative meeting place / safe place to stay','Individual needs / agreed support','Local emergency number / clinician / pharmacy','Location of supplies, radio and first aid kit','Reviewed on / next review date'],
 'stock':'Supplies and next actions','stock_sub':'Fill specific gaps instead of buying at random.',
 'headers':['Category / item','In stock','Add / review'],
 'rows':['Drinking and cooking water','Hygiene water / pets','Ready-to-eat food','Special dietary needs','Can opener / utensils','Lights / batteries','Radio / power banks','Hygiene / waste bags','First aid / personal care','Medication continuity plan','Documents / cash','Grab bag / clothing'],
 'calc':'Water planning: ____ people × ____ days × ____ liters per day = ____ liters. Additional needs: ____ liters. Check assumptions against local guidance.',
 'tasks':'My next three actions',
 'ref':'Resources and next steps','refsub':'Current official instructions take priority.',
 'refs_intro':'These official resources provide further guidance. Check current content and the rules for your location before use. This English edition is a general international version; add your local emergency numbers and regional requirements.',
 'last':'Before the next outage',
 'finalchecks':['Discuss the plan with everyone in your household','Test lights and radio; charge power banks','Check the contact list and meeting places together','Put new supplies behind older stock','Schedule the next review'],
 'notice':'General planning guidance, not individual medical or technical advice. No guarantee of coping with a specific outage duration. Not affiliated with the authorities listed. Edition 1.0 · 2026.',
 'print':'Printing: use 100% / actual size. Designed for handwritten entries; no interactive PDF form fields.'}
}
RES=[('BBK · Deutschland / Germany','https://www.bbk.bund.de/'),('Ready.gov · Power outages','https://www.ready.gov/power-outages'),('Ready.gov · Emergency supplies','https://www.ready.gov/kit'),('FoodSafety.gov · Food safety during outages','https://www.foodsafety.gov/food-safety-charts/food-safety-during-power-outage'),('CDC · Carbon monoxide prevention','https://www.cdc.gov/carbon-monoxide/about/')]
class Book:
 def __init__(self,path,size,d,lang):
  self.c=canvas.Canvas(str(path),pagesize=size,pageCompression=1);self.size=size;self.d=d;self.lang=lang;self.n=0
  self.c.setTitle('BLACKOUT READY | '+d['sub']);self.c.setAuthor('BLACKOUT READY');self.c.setSubject('Illustrated household preparedness guide | Edition 2')
 def txt(self,t,x,y,w=507,size=10,color=INK,bold=False,serif=False):
  st=ParagraphStyle('p',fontName='Editorial' if serif else ('Bold' if bold else 'Regular'),fontSize=size,leading=size*1.45,textColor=HexColor(color))
  p=Paragraph(t,st);_,h=p.wrap(w,800)
  if y-h<53 and y>55:raise ValueError(f'Overflow page {self.n}: {t[:50]} -> {y-h}')
  p.drawOn(self.c,x,y-h);return y-h
 def photo(self,key,x,y,w,h):
  from reportlab.lib.utils import ImageReader
  img=ImageReader(str(OUT/'images'/f'{key}.jpg')); iw,ih=img.getSize();sc=max(w/iw,h/ih)
  c=self.c;c.saveState();clip=c.beginPath();clip.rect(x,y,w,h);c.clipPath(clip,stroke=0)
  c.drawImage(img,x+(w-iw*sc)/2,y+(h-ih*sc)*0.32,width=iw*sc,height=ih*sc);c.restoreState()
 def begin(self,title=None,sub=None,white=False):
  self.n+=1;c=self.c;c.saveState()
  scale=min(self.size[0]/595,self.size[1]/842)
  c.translate((self.size[0]-595*scale)/2,(self.size[1]-842*scale)/2);c.scale(scale,scale)
  c.setFillColor(HexColor('#FFFFFF' if white else CREAM));c.rect(0,0,595,842,fill=1,stroke=0)
  if title:
   c.bookmarkPage(f'page-{self.n}');c.addOutlineEntry(title,f'page-{self.n}',level=0)
   self.txt('BLACKOUT READY',44,805,size=9,bold=True,color=GREEN)
   self.txt('HAUSHALTSVORSORGE' if self.lang=='de' else 'HOUSEHOLD PREPAREDNESS',345,805,w=210,size=7.4,color=MUTED)
   c.setStrokeColor(HexColor('#CBD3C7'));c.line(44,780,551,780)
   self.txt(f'{self.n-1:02d} /',44,758,size=10,color=ORANGE,bold=True)
   end=self.txt(title,44,733,w=510,size=26,serif=True)
   self.txt(sub,44,end-8,w=510,size=10,color=MUTED)
  c.setStrokeColor(HexColor('#D3D7CD'));c.line(44,46,551,46)
  self.txt('BLACKOUT READY  /  '+('DEUTSCH' if self.lang=='de' else 'ENGLISH'),44,32,size=7,color=MUTED)
  self.txt(f'{self.n:02d} / 12',505,32,w=48,size=7,color=MUTED)
 def end(self):self.c.restoreState();self.c.showPage()
 def check(self,items,y,x=58,w=475,size=9):
  for t in items:
   self.c.setStrokeColor(HexColor(GREEN));self.c.setLineWidth(.7);self.c.rect(x,y-11,8,8,stroke=1,fill=0)
   y=self.txt(t,x+19,y,w=w-22,size=size)-9
  return y
 def render(self):
  d=self.d;c=self.c;de=self.lang=='de';self.begin()
  c.setFillColor(HexColor(GREEN));c.rect(0,100,595,742,fill=1,stroke=0)
  self.txt('DER HAUSHALTSGUIDE / AUSGABE 02.1' if de else 'THE HOUSEHOLD GUIDE / EDITION 02.1',44,799,size=8.5,color='#C5D0BA',bold=True)
  self.txt('BLACKOUT',39,747,size=65,color=CREAM,bold=True)
  self.txt('READY',39,660,size=65,color=CREAM,bold=True)
  c.setFillColor(HexColor(ORANGE));c.rect(44,553,54,4,fill=1,stroke=0)
  self.txt(d['sub'],44,530,w=490,size=21,color=CREAM,serif=True)
  self.photo('household',0,100,595,372)
  self.txt(d['topics'],44,80,size=8.2,color=GREEN,bold=True)
  self.end()
  # An actionable contents page.
  self.begin('Dein Plan auf einen Blick' if de else 'Your plan at a glance','Weniger suchen. Besser vorbereitet sein.' if de else 'Less searching. Better preparation.')
  self.txt(d['desc'],44,632,size=12,w=490)
  y=563
  toc=[(3,d['pages'][0][0]),(4,d['pages'][1][0]),(5,d['pages'][2][0]),(6,d['pages'][3][0]),(7,d['pages'][4][0]),(8,d['pages'][5][0]),(9,d['plan']),(10,d['stock']),(11,'Der kleine Praxistest' if de else 'A simple practice session'),(12,d['ref'])]
  for pn,t in toc:
   c.linkRect('',f'page-{pn}',(44,y-26,551,y+4),relative=1,thickness=0)
   self.txt(t,44,y,w=440,size=11);self.txt(f'{pn:02d}',520,y,w=32,size=10,bold=True,color=ORANGE)
   c.setStrokeColor(HexColor('#D3D7CD'));c.line(44,y-26,551,y-26);y-=37
  self.txt('SO STARTET IHR' if de else 'START HERE',44,163,size=9,bold=True,color=ORANGE)
  self.txt('Einmal gemeinsam durchlesen. Die drei Arbeitsblätter ausfüllen. Vorräte prüfen und den nächsten Termin festlegen.' if de else 'Read it together. Complete the three worksheets. Check your supplies and set a date for the next review.',44,141,size=10)
  self.end()
  keys=['household','household','water','pantry','water','household']
  for idx,(title,sub,sections,checks) in enumerate(d['pages']):
   self.begin(title,sub);self.photo(keys[idx],44,485,507,151)
   for col in range(2):
    x=44+col*266;y=460
    for j in range(2):
     heading,body=sections[col*2+j]
     self.txt(f'0{col*2+j+1}',x,y,w=28,size=8,color=ORANGE,bold=True)
     y=self.txt(heading,x+27,y+2,w=214,size=11,bold=True)-7
     y=self.txt(body,x,y,w=241,size=10)-20
    if y<167:raise ValueError(('Column overlaps checks',title,y))
   c.setFillColor(HexColor('#E7EBE0'));c.roundRect(44,63,507,98,6,fill=1,stroke=0)
   self.txt('KURZ-CHECK' if de else 'QUICK CHECK',58,151,size=7.8,color=ORANGE,bold=True)
   self.check(checks,133,size=8.3)
   self.end()
  self.begin(d['plan'],d['plan_sub'],white=True);y=636
  for i,field in enumerate(d['fields']):
   c.setFillColor(HexColor('#F3F5EF'));c.roundRect(44,y-55,507,55,3,stroke=0,fill=1)
   self.txt(field,55,y-7,w=485,size=9,bold=True);c.setStrokeColor(HexColor('#C3CEC1'));c.line(55,y-43,540,y-43);y-=65
  self.txt('Nur notwendige Angaben eintragen. Ausdruck sicher aufbewahren.' if de else 'Include only necessary information. Store the printed plan securely.',44,95,size=8,color=MUTED)
  self.end()
  self.begin(d['stock'],d['stock_sub'],white=True);y=635;xs=[44,292,388,551];ww=[248,96,163]
  c.setFillColor(HexColor(GREEN));c.rect(44,y-31,507,31,stroke=0,fill=1)
  for i,h in enumerate(d['headers']):self.txt(h,xs[i]+10,y-8,w=ww[i]-16,size=8.5,color=CREAM,bold=True)
  y-=31
  for idx,row in enumerate(d['rows']):
   c.setFillColor(HexColor('#F1F4ED' if idx%2==0 else '#FFFFFF'));c.rect(44,y-29,507,29,stroke=0,fill=1)
   self.txt(row,54,y-7,w=231,size=8.8)
   c.setStrokeColor(HexColor('#D5DDD0'));c.setLineWidth(.4)
   for x in xs:c.line(x,y,x,y-29)
   c.line(44,y-29,551,y-29);y-=29
  y=self.txt(d['calc'],44,y-17,size=8.8)-20
  self.txt(d['tasks'],44,y,size=11,bold=True)
  for i in range(3):
   y-=30;self.txt(f'0{i+1}',44,y+11,w=24,size=8,color=ORANGE,bold=True);c.line(75,y,551,y)
  self.end()
  self.begin('Der kleine Praxistest' if de else 'A simple practice session','20 Minuten gemeinsam planen – ohne den Strom abzuschalten.' if de else 'Spend 20 minutes planning together — leave the power on.',white=True)
  y=634
  practice=[('01 / Finden' if de else '01 / Locate','Kann jede Person Lampe, Radio und Erste-Hilfe-Set finden? Prüft die Geräte und die passenden Batterien gemeinsam.' if de else 'Can everyone locate a flashlight, radio and first aid kit? Check the equipment and matching batteries together.'),('02 / Besprechen' if de else '02 / Discuss','Geht eine Mahlzeit ohne Strom durch. Wie erreicht ihr eure Kontaktperson? Wer unterstützt Kinder, Tiere oder andere Personen mit besonderem Bedarf?' if de else 'Talk through a meal without electricity. How will you reach your contact person? Who supports children, pets or anyone with additional needs?'),('03 / Verbessern' if de else '03 / Improve','Haltet Lücken fest und verteilt Aufgaben. Testet dabei keine medizinischen Geräte, Heizungen oder elektrischen Anlagen durch Abschalten.' if de else 'Record gaps and assign actions. Do not test medical equipment, heating or electrical systems by switching them off.')]
  for heading,body in practice:
   y=self.txt(heading,44,y,size=12,bold=True,color=GREEN)-7;y=self.txt(body,44,y,size=10)-24
  labels=['Das hat funktioniert','Das fehlt noch','Wer kümmert sich bis wann?','Unser nächster Prüftermin'] if de else ['What worked','What is missing','Who will do what, by when?','Our next review date']
  for label in labels:
   self.txt(label,44,y,size=9,bold=True);c.setStrokeColor(HexColor('#BDCCBA'));c.line(44,y-43,551,y-43);y-=64
  self.end()
  self.begin(d['ref'],d['refsub']);y=self.txt(d['refs_intro'],44,632,size=10)-20
  for idx,(label,url) in enumerate(RES):
   if de:label=['BBK · Notfallvorsorge in Deutschland','Ready.gov · Stromausfälle (englisch)','Ready.gov · Notfallvorräte (englisch)','FoodSafety.gov · Lebensmittel bei Stromausfall (englisch)','CDC · Schutz vor Kohlenmonoxid (englisch)'][idx]
   y=self.txt(label,44,y,size=9.5,bold=True)-3;y=self.txt('<link href="'+url+'">'+url+'</link>',44,y,size=8,color=GREEN)-12
  y=self.txt(d['last'],44,y-6,size=13,serif=True)-12;y=self.check(d['finalchecks'],y,x=44,size=8.6)-8
  notice=d['notice'].replace('1.0','2.1')
  y=self.txt(notice,44,y,size=8,color=MUTED)-10;y=self.txt(d['print'],44,y,size=8,color=MUTED)-10
  self.txt('Bilder: KI-generierte redaktionelle Illustrationen.' if de else 'Images: AI-generated editorial illustrations.',44,y,size=7.5,color=MUTED)
  self.end();assert self.n==12;c.save()
for lang,d in DATA.items():
 for fmt,size in [('A4',(595.276,841.89)),('US-Letter',(612,792))]:Book(OUT/f'Blackout-Ready_{lang.upper()}_{fmt}.pdf',size,d,lang).render()
 for page in range(12):
  doc=fitz.open(OUT/f'Blackout-Ready_{lang.upper()}_A4.pdf');doc[page].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(OUT/f'preview_{lang}_{page+1:02}.png'))
(OUT/'content.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2))
print('Created four 12-page illustrated PDFs.')
