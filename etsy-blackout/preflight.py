"""Inspect the built deliverables, not just generator return codes."""
from pathlib import Path
import fitz,json,hashlib,re
from PIL import Image
from zipfile import ZipFile
P=Path(__file__).resolve().parent
report={'edition':'2.1','pdfs':[],'images':[],'zips':[],'limitations':['Live authority and Etsy pages blocked by proxy (403); their content and currency not verified.','No physical print test.','No Etsy upload, live crop or checkout test.']}
for lang in ['DE','EN']:
 docs=[]
 for fmt,expected_size in [('A4',(595.276,841.89)),('US-Letter',(612,792))]:
  path=P/f'Blackout-Ready_{lang}_{fmt}.pdf';d=fitz.open(path);docs.append(d)
  assert len(d)==12 and not d.is_encrypted
  for pg in d:
   assert abs(pg.rect.width-expected_size[0])<.01 and abs(pg.rect.height-expected_size[1])<.01
   assert len(pg.get_text())>100 and '\ufffd' not in pg.get_text()
   assert not list(pg.widgets() or [])
   for b in pg.get_text('blocks'):
    assert b[0]>=-1 and b[1]>=-1 and b[2]<=pg.rect.width+1 and b[3]<=pg.rect.height+1,(path.name,pg.number,b[:4])
   for info in pg.get_image_info():
    a,b,c,e,_,_=info['transform'];assert abs(a/info['width']-e/info['height'])<.0001,'Distorted image'
   assert f'{pg.number+1:02d} / 12' in pg.get_text()
  assert '2.1' in d[-1].get_text() and '02.1' in d[0].get_text()
  assert len(d.get_toc())==11 and [x[2] for x in d.get_toc()]==list(range(2,13))
  links=d[1].get_links();assert len(links)==10
  for link,target in zip(links,range(3,13)):
   dest=d.xref_object(link['xref']);assert re.search(r'/Dest\s*\[\s*'+str(d.page_xref(target-1))+r'\s+0\s+R',dest)
  assert len(d[-1].get_links())==5
  fonts={span['font'] for pg in d for b in pg.get_text('dict')['blocks'] if b['type']==0 for ln in b['lines'] for span in ln['spans']}
  for f in d[0].get_fonts():
   if 'DejaVu' in f[3]:assert len(d.extract_font(f[0])[3])>1000
  assert fonts=={'DejaVuSans','DejaVuSans-Bold','DejaVuSerif'}
  text=''.join(pg.get_text() for pg in d)
  assert ('Die drei Arbeitsblätter' if lang=='DE' else 'the three worksheets') in text
  assert ('nur im Freien' if lang=='DE' else 'outdoors only') in text
  report['pdfs'].append({'file':path.name,'pages':len(d),'bytes':path.stat().st_size,'fonts_embedded':True,'proportions':'uniform','contents_links':10,'bookmarks':11,'external_links_embedded':5,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 assert [pg.get_text() for pg in docs[0]]==[pg.get_text() for pg in docs[1]],'Paper formats differ in text'
 for i,path in enumerate(sorted((P/'Etsy-Bilder'/lang).glob('*.jpg')),1):
  assert path.name.startswith(f'{i:02d}_')
  with Image.open(path) as im:assert im.size==(3000,2250) and im.mode=='RGB';im.verify()
  report['images'].append({'file':str(path.relative_to(P)),'pixels':[3000,2250],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 assert len(list((P/'Etsy-Bilder'/lang).glob('*.jpg')))==6
 with ZipFile(P/f'Etsy-Upload-{lang}.zip') as z:
  names=z.namelist();assert len([n for n in names if n.startswith('Kundendateien/')])==2
  assert all(n.endswith('.pdf') for n in names if n.startswith('Kundendateien/'))
  assert len([n for n in names if n.startswith('Produktbilder/')])==6
  assert z.testzip() is None
 for name in [f'BLACKOUT-READY-{lang}.zip',f'Etsy-Bilder-{lang}.zip',f'Etsy-Upload-{lang}.zip']:
  with ZipFile(P/name) as z:assert z.testzip() is None
  report['zips'].append(name)
for path in [P/'BLACKOUT-READY-Bilingual.zip',P/'Etsy-Verkaufsmaterial.zip',P.parent/'Etsy-Blackout-Ready.zip']:
 with ZipFile(path) as z:assert z.testzip() is None
 report['zips'].append(path.name)
with ZipFile(P.parent/'Etsy-Blackout-Ready.zip') as z:
 assert len([n for n in z.namelist() if '/Etsy-Verkaufsmaterial/' in n and n.endswith('.jpg')])==12
 assert len([n for n in z.namelist() if n.endswith('.pdf')])==4
 assert any(n.endswith('VOR-DEM-UPLOAD.md') for n in z.namelist())
listing=(P/'Etsy-Texte.md').read_text();assert 'KI-Unterstützung' in listing and 'AI assistance' in listing
for row in listing.splitlines():
 if row.startswith(('Titel:','Title:')):assert len(row.split(': ',1)[1])<=140
 if row.startswith(('Tags (Vorschläge):','Suggested tags:')):
  tags=[s.strip() for s in row.split(': ',1)[1].split(',')];assert len(tags)==13 and max(map(len,tags))<=20
report['result']='PASS: technical and editorial checks; live-source review remains outstanding'
(P/'preflight-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(report['result']);print('4 PDFs / 48 pages; 12 listing images; 9 archives; embedded fonts; navigation; uniform scaling; content parity.')
