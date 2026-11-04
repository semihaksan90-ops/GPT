from pathlib import Path
from PIL import Image,ImageStat
from zipfile import ZipFile
import json,hashlib,csv,re
import fitz
P=Path(__file__).resolve().parent
specs=json.loads((P/'source/motifs.json').read_text());rows=json.loads((P/'source/export-manifest.json').read_text())
assert len(specs)==len(rows)==200
assert [x['id'] for x in rows]==[f'{n:03d}' for n in range(1,201)]
assert len(list((P/'JPG').glob('*.jpg')))==200
hashes=[];sizes=[];near=[];perceptual=[]
for m,r in zip(specs,rows):
 p=P/'JPG'/m['filename'];h=hashlib.sha256(p.read_bytes()).hexdigest();hashes.append(h);assert h==r['sha256']
 with Image.open(p) as im:
  assert im.mode=='RGB' and im.size==(3000,3000)
  assert im.info.get('icc_profile') and all(abs(a-300)<1 for a in im.info['dpi'])
  std=ImageStat.Stat(im.resize((100,100))).stddev;assert min(std)>30,'Blank or nearly blank image'
  thumb=im.convert('L').resize((9,8));pix=[thumb.getpixel((x,y)) for y in range(8) for x in range(9)];bits=0
  for y in range(8):
   for x in range(8):bits=(bits<<1)|int(pix[y*9+x]>pix[y*9+x+1])
  perceptual.append((m['id'],bits))
 sizes.append(p.stat().st_size)
assert len(set(hashes))==200,'Duplicate JPG bytes found'
baseline=json.loads((P/'source/initial-100-manifest.json').read_text())
assert len(baseline)==100
assert {r['id']:r['sha256'] for r in rows[:100]}=={r['id']:r['sha256'] for r in baseline},'An original design was modified'
assert len({(m['city'].casefold(),m['title'].casefold()) for m in specs})==200,'Repeated main subject in the motif list'
for i,(ida,ha) in enumerate(perceptual):
 for idb,hb in perceptual[i+1:]:
  if (ha^hb).bit_count()<5:near.append([ida,idb,(ha^hb).bit_count()])
archive_names=[];archive_members=[];archive_total=0
for part in range(1,11):
 p=P/'downloads'/f'Heritage-in-Glass-Part-{part:02d}.zip'
 assert p.stat().st_size<99_000_000
 with ZipFile(p) as z:
  assert z.testzip() is None
  jpgs=[n for n in z.namelist() if n.endswith('.jpg')];assert len(jpgs)==20
  expected=['JPG/'+m['filename'] for m in specs[(part-1)*20:part*20]];assert jpgs==expected
  for name,r in zip(jpgs,rows[(part-1)*20:part*20]):assert hashlib.sha256(z.read(name)).hexdigest()==r['sha256']
  if part==1:assert all(n in z.namelist() for n in ['Read-Me.txt','License.txt','Design-Index.pdf','Design-List.csv'])
  archive_members+=jpgs
 archive_names.append(p.name);archive_total+=p.stat().st_size
assert len(archive_members)==len(set(archive_members))==200
with (P/'Design-List.csv').open(encoding='utf-8-sig') as f:assert len(list(csv.DictReader(f)))==200
idx=fitz.open(P/'Design-Index.pdf');assert len(idx)==10
index_text=''.join(pg.get_text() for pg in idx)
for m in specs:assert m['id']+' /' in index_text and m['city'] in index_text
normalized_index=' '.join(index_text.split())
for m in specs:assert ' '.join(m['title'].split()) in normalized_index,('Missing index label',m['id'])
for pg in idx:
 for b in pg.get_text('blocks'):
  assert b[0]>=0 and b[1]>=0 and b[2]<=pg.rect.width+1 and b[3]<=pg.rect.height+1
pdf=fitz.open(P/'Buyer-Download-Guide.pdf');assert len(pdf)==3
links=pdf[0].get_links()+pdf[1].get_links();assert len(links)==10
assert all(l['uri'].endswith(f'Heritage-in-Glass-Part-{i:02d}.zip') for i,l in enumerate(links,1))
for pg in pdf:
 for b in pg.get_text('blocks'):assert b[0]>=0 and b[1]>=0 and b[2]<=pg.rect.width+1 and b[3]<=pg.rect.height+1
for p in (P/'etsy').glob('*.jpg'):
 with Image.open(p) as im:assert im.size==(3000,2250) and im.mode=='RGB';im.verify()
assert len(list((P/'etsy').glob('*.jpg')))==6
with ZipFile(P/'Seller-Kit-EN.zip') as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.endswith('.jpg')])==6
 assert 'Buyer-Download-Guide.pdf' in z.namelist()
listing=(P/'Etsy-Listing-EN.txt').read_text();title=listing.split('TITLE\n',1)[1].split('\n',1)[0];assert len(title)<=140
rawtags=listing.split('TAGS\n',1)[1].strip();tags=[x.strip() for x in rawtags.split(',')];assert len(tags)==13 and max(map(len,tags))<=20
review=json.loads((P/'source/artwork-review.json').read_text());assert len(review)==200
assert len({r['pixels_sha256'] for r in review})==200,'Duplicate original artwork pixels found'
manual=json.loads((P/'source/visual-review.json').read_text())
for ida,idb,distance in near:
 matches=[r for r in manual['pairs'] if set(r['ids'])=={ida,idb}]
 assert len(matches)==1,'Unreviewed similarity candidate'
 for key in [ida,idb]:assert matches[0]['jpg_sha256'][key]==next(r['sha256'] for r in rows if r['id']==key),'Visual review is stale'
report={'result':'Technical file checks passed','designs':200,'unique_jpg_hashes':len(set(hashes)),'unique_original_pixel_hashes':len({r['pixels_sha256'] for r in review}),'source_dimensions':sorted({(r['source_width'],r['source_height']) for r in rows}),'export_dimensions':[3000,3000],'profile':'RGB/sRGB','dpi_metadata':300,'resized_from_generated_originals':True,'initial_100_retained_byte_for_byte':True,'archive_parts':archive_names,'total_archive_bytes':archive_total,'index_pages':10,'guide_pages':3,'listing_images':6,'perceptual_similarity_candidates':near,'visually_reviewed_candidates':manual['pairs'],'unresolved_similarity_candidates':[],'visual_review':'All 200 artworks and six listing images reviewed','source_edge_flags':[r['id'] for r in review if r['edge_review_needed']],'not_verified':['Physical print and sublimation results','Exact historical or architectural fidelity','Current Etsy policy and uploader constraints','Buyer-only access control; GitHub links are public']}
(P/'Validation-Report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
