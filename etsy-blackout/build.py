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
 ('Individuelle Bedürfnisse','Plane für Kinder, ältere Menschen, Behinderungen, Haustiere und medizinische Geräte gesondert. Wer auf strombetriebene Hilfsmittel angewiesen ist, braucht vorab einen abgestimmten Ersatz- und Evakuierungsplan mit dem Versorgungsteam.'),
 ('Grenzen und Hilfe','Offizielle Anweisungen vor Ort haben Vorrang. Bei unmittelbarer Gefahr suche Hilfe und verlasse gefährdete Bereiche. In Deutschland und der EU gilt 112; außerhalb der EU prüfe die örtliche Notrufnummer. Dieses Heft ersetzt keine medizinische Beratung oder Erste-Hilfe-Ausbildung.')],
 ['Vorräte und Notfalltasche an einem bekannten Ort lagern','Alle im Haushalt kennen den Plan und den Treffpunkt','Plan alle sechs Monate und nach Veränderungen prüfen']),
 ('Wenn der Strom ausfällt','Die ersten Schritte',[
 ('Zuerst Sicherheit','Nutze eine Taschenlampe. Prüfe, ob jemand verletzt ist oder dringend Unterstützung braucht. Bei Rauch, Gasgeruch oder anderer unmittelbarer Gefahr bring dich in Sicherheit und verständige die zuständige Notfallstelle von einem sicheren Ort.'),
 ('Lage klären','Prüfe gefahrlos, ob auch die Umgebung betroffen ist. Nutze ein batteriebetriebenes Radio und offizielle Meldungen. Gehe nicht an beschädigte Leitungen und öffne keine elektrischen Anlagen.'),
 ('Haushalt stabilisieren','Halte Kühl- und Gefriergeräte geschlossen. Schalte Kochgeräte und empfindliche Elektronik aus. Lass eine sichere Leuchte eingeschaltet, damit du erkennst, wenn die Versorgung zurückkehrt.'),
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
 ('Sicher zubereiten','Plane möglichst ohne offenes Feuer. Grill, Holzkohle und Generator gehören niemals in Wohnräume, Garage oder Keller. Auch ein offenes Fenster macht sie dort nicht sicher. Campingkocher nur im ausdrücklich zugelassenen Umfeld gemäß Hersteller verwenden.')],
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
 ('Kohlenmonoxid vermeiden','Betreibe Generatoren ausschließlich draußen, weit entfernt von Fenstern, Türen und Lüftungsöffnungen nach Hersteller- und Behördenvorgaben. Nicht in Hausinstallationen einspeisen: Dafür ist fachgerecht installierte Umschalttechnik erforderlich.'),
 ('Verbunden bleiben','Notiere einen Treffpunkt in der Nähe und eine Alternative außerhalb des Viertels. Vereinbare eine Kontaktperson außerhalb der Region. Besprich Unterstützung mit Nachbarn freiwillig und ohne sensible Daten unnötig weiterzugeben.')],
 ['Taschenlampe nachts griffbereit lagern','Radio und Batterien testen','Treffpunkt und Kontaktperson eintragen'])],
 'plan':'Mein Haushaltsplan','plan_sub':'Gemeinsam ausfüllen und zugänglich aufbewahren.',
 'fields':['Haushalt / Anzahl Personen / Haustiere','Kontaktperson außerhalb der Region / Telefon','Treffpunkt in der Nähe','Alternativer Treffpunkt / sicherer Ausweichort','Besondere Bedürfnisse / vereinbarte Unterstützung','Praxis / Apotheke / wichtige lokale Telefonnummern','Ort von Vorräten, Radio und Erste-Hilfe-Set','Geprüft am / nächster Prüftermin'],
 'stock':'Vorräte und Aufgaben','stock_sub':'Gezielt ergänzen statt wahllos einkaufen.',
 'headers':['Bereich / Artikel','Vorhanden','Ergänzen / prüfen'],
 'rows':['Trink- und Kochwasser','Hygienewasser / Haustiere','Verzehrfertige Lebensmittel','Spezielle Ernährung','Dosenöffner / Geschirr','Lampen / Batterien','Radio / Powerbanks','Hygiene / Abfallbeutel','Erste Hilfe / persönliche Pflege','Medikamente: Versorgungsplan','Dokumente / Bargeld','Notfalltasche / Kleidung'],
 'calc':'Wasserplanung: ____ Personen × ____ Tage × ____ Liter pro Tag = ____ Liter. Zusatzbedarf: ____ Liter. Annahmen mit örtlichen Empfehlungen abgleichen.',
 'tasks':'Meine nächsten drei Aufgaben',
 'ref':'Quellen und nächste Schritte','refsub':'Aktuelle Hinweise haben Vorrang.',
 'refs_intro':'Die folgenden offiziellen Anlaufstellen bieten weiterführende Empfehlungen. Prüfe vor der Nutzung aktuelle Inhalte und die Vorgaben für deinen Wohnort. Die englische Ausgabe ist eine allgemeine internationale Fassung; Notrufnummern und regionale Regeln müssen ergänzt werden.',
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
 ('Prepare meals safely','Plan meals without open flames where possible. Never use grills, charcoal or generators inside a home, garage or basement. An open window does not make indoor use safe. Use camping stoves only in the setting explicitly permitted by the manufacturer.')],
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
 ('Prevent carbon monoxide exposure','Operate generators outdoors only, far from doors, windows and vents, following manufacturer and local authority guidance. Never feed power into household wiring without professionally installed transfer equipment.'),
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
  self.c=canvas.Canvas(str(path),pagesize=size); self.size=size; self.d=d; self.lang=lang;self.n=0
  self.c.setTitle('BLACKOUT READY — '+d['sub']); self.c.setAuthor('BLACKOUT READY'); self.c.setSubject('Printable household preparedness guide and planner')
 def txt(self,t,x,y,w=480,size=10.2,color=INK,bold=False):
  st=ParagraphStyle('p',fontName='Bold' if bold else 'Regular',fontSize=size,leading=size*1.5,textColor=HexColor(color))
  p=Paragraph(t,st); _,h=p.wrap(w,800);p.drawOn(self.c,x,y-h);return y-h
 def begin(self,title=None,sub=None):
  self.n+=1;self.c.saveState();self.c.scale(self.size[0]/595,self.size[1]/842)
  c=self.c;c.setFillColor(HexColor(CREAM));c.rect(0,0,595,842,fill=1,stroke=0)
  if title:
   self.txt('BLACKOUT READY',44,806,size=9,bold=True,color=GREEN)
   c.setStrokeColor(HexColor(ORANGE));c.line(44,779,551,779)
   self.txt(f'{self.n-1:02d}',44,755,size=12,color=ORANGE,bold=True)
   self.txt(title,44,725,w=510,size=27,bold=True)
   self.txt(sub,44,675,w=510,size=11,color=MUTED)
  c.setStrokeColor(HexColor('#D3D7CD')); c.line(44,48,551,48)
  self.txt('DEUTSCH' if self.lang=='de' else 'ENGLISH',44,36,size=8,color=MUTED)
  self.txt(f'{self.n:02d} / 10',505,36,w=48,size=8,color=MUTED)
 def end(self): self.c.restoreState();self.c.showPage()
 def check(self,items,y):
  for t in items:
   self.c.setStrokeColor(HexColor(GREEN));self.c.rect(45,y-12,9,9,stroke=1,fill=0)
   y=self.txt(t,65,y,w=475,size=9.4)-10
  return y
 def render(self):
  d=self.d;c=self.c;self.begin();c.setFillColor(HexColor(GREEN));c.rect(0,100,595,742,fill=1,stroke=0)
  self.txt('HOUSEHOLD FIELD GUIDE  /  01',45,791,size=10,color='#C3D1BE',bold=True)
  self.txt('BLACKOUT<br/>READY',40,697,size=66,w=530,color=CREAM,bold=True)
  c.setFillColor(HexColor(ORANGE));c.rect(45,460,78,6,fill=1,stroke=0)
  self.txt(d['sub'],45,432,w=490,size=23,color=CREAM,bold=True)
  self.txt(d['desc'],45,342,w=445,size=12,color='#D7DFD2')
  # Original abstract route motif: four connected preparation points.
  c.setStrokeColor(HexColor('#739584'));c.setLineWidth(2);c.lines([(60,210,205,210),(205,210,350,210),(350,210,495,210)])
  for x,num in [(60,'01'),(205,'02'),(350,'03'),(495,'04')]:
   c.setFillColor(HexColor(GREEN));c.circle(x,210,17,fill=1,stroke=1);self.txt(num,x-10,218,w=30,size=10,color=CREAM,bold=True)
  self.txt(d['topics'],45,158,w=510,size=9,color='#D7DFD2',bold=True)
  self.txt(d['tag'],45,79,w=510,size=10,color=GREEN,bold=True);self.end()
  for title,sub,sections,checks in d['pages']:
   self.begin(title,sub); y=635
   for heading,body in sections:
    y=self.txt(heading,44,y,size=12,bold=True)-5
    y=self.txt(body,44,y,w=505,size=10)-17
   y-=4; self.check(checks,y)
   if y<125: raise RuntimeError((title,y))
   self.end()
  self.begin(d['plan'],d['plan_sub']);y=631
  for field in d['fields']:
   self.txt(field,44,y,size=10,bold=True);c.setStrokeColor(HexColor('#A4B2A5'));c.line(44,y-43,551,y-43);y-=65
  self.end()
  self.begin(d['stock'],d['stock_sub']);y=634
  widths=[245,95,167];xs=[44,289,384,551]
  c.setFillColor(HexColor(GREEN));c.rect(44,y-30,507,30,fill=1,stroke=0)
  for i,h in enumerate(d['headers']):self.txt(h,xs[i]+9,y-7,w=widths[i]-16,size=9,color=CREAM,bold=True)
  y-=30
  for idx,row in enumerate(d['rows']):
   c.setFillColor(HexColor('#E7EBE1' if idx%2==0 else CREAM));c.rect(44,y-29,507,29,fill=1,stroke=0)
   self.txt(row,53,y-7,w=226,size=9)
   for x in xs:c.setStrokeColor(HexColor('#C9D1C3'));c.line(x,y,x,y-29)
   c.line(44,y-29,551,y-29);y-=29
  y=self.txt(d['calc'],44,y-20,w=505,size=9)-20
  self.txt(d['tasks'],44,y,size=12,bold=True)
  for i in range(3):
   y-=32;self.txt(str(i+1)+'.',44,y+10,size=10);c.line(65,y,551,y)
  self.end()
  self.begin(d['ref'],d['refsub']);y=self.txt(d['refs_intro'],44,632,w=505,size=10)-20
  for label,url in RES:
   y=self.txt(label,44,y,size=10,bold=True)-3
   y=self.txt('<link href="'+url+'">'+url+'</link>',44,y,w=505,size=8.2,color=GREEN)-13
  y-=5;y=self.txt(d['last'],44,y,size=13,bold=True)-12;y=self.check(d['finalchecks'],y)-12
  y=self.txt(d['notice'],44,y,w=505,size=8.5,color=MUTED)-10
  self.txt(d['print'],44,y,w=505,size=8.5,color=MUTED);self.end()
  assert self.n==10
  c.save()
for lang,d in DATA.items():
 for fmt,size in [('A4',(595.276,841.89)),('US-Letter',(612,792))]:
  p=OUT/f'Blackout-Ready_{lang.upper()}_{fmt}.pdf';Book(p,size,d,lang).render()
 for page in [0,2,7,8]:
  doc=fitz.open(OUT/f'Blackout-Ready_{lang.upper()}_A4.pdf');pix=doc[page].get_pixmap(matrix=fitz.Matrix(1.5,1.5));pix.save(str(OUT/f'preview_{lang}_{page+1:02}.png'))
(OUT/'content.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2))
print('Created four 10-page PDFs and eight previews.')
