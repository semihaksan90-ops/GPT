"""Build English catalog, artwork archives, listing images and download instructions."""
from pathlib import Path
from io import BytesIO
import csv,json,zipfile,math,hashlib,argparse,shutil
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
P=Path(__file__).resolve().parent
F='/usr/share/fonts/truetype/dejavu/'
for n,f in [('Regular','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf')]:pdfmetrics.registerFont(TTFont(n,F+f))
NAVY='#102C3B';CREAM='#FBF5E5';GOLD='#B98B36';INK='#20353D';MUTED='#52656A'
M=json.loads((P/'source/motifs.json').read_text())
A={x['id']:x for x in M}
TOTAL=len(M);PER_PART=40;PART_COUNT=(TOTAL+PER_PART-1)//PER_PART;INDEX_PAGES=(TOTAL+19)//20
def art(n,size):
 m=A[f'{n:03d}'];im=Image.open(P/'JPG'/m['filename']).convert('RGB');im=im.resize((size,size),Image.Resampling.LANCZOS);return im

def txt(c,t,x,y,w=507,size=10,color=INK,bold=False):
 st=ParagraphStyle('p',fontName='Bold' if bold else 'Regular',fontSize=size,leading=size*1.45,textColor=HexColor(color));p=Paragraph(t,st);_,h=p.wrap(w,800)
 if y-h<30:raise ValueError(('Text overflow',t[:50],y-h))
 p.drawOn(c,x,y-h);return y-h

def catalog(preview=False):
 path=P/('review/Index-Preview.pdf' if preview else 'Design-Index.pdf');c=canvas.Canvas(str(path),pagesize=(595.276,841.89),pageCompression=1);c.setTitle('Heritage in Glass — 200 Design Index');c.setAuthor('Heritage in Glass')
 for part in range(1 if preview else INDEX_PAGES):
  c.setFillColor(HexColor(CREAM));c.rect(0,0,596,843,fill=1,stroke=0)
  txt(c,'HERITAGE IN GLASS',44,807,size=9,bold=True,color=NAVY)
  txt(c,f'DESIGN INDEX / {part*20+1:03d}–{part*20+20:03d}',44,780,size=18,bold=True)
  txt(c,'Historic cities & landmarks · Circular stained-glass-style artwork',44,749,size=8.5,color=MUTED)
  for i,m in enumerate(M[part*20:(part+1)*20]):
   x=44+(i%4)*129;y=718-(i//4)*130
   im=art(int(m['id']),321);b=BytesIO();im.save(b,format='JPEG',quality=88)
   c.drawImage(ImageReader(BytesIO(b.getvalue())),x,y-107,width=107,height=107)
   txt(c,m['id']+' / '+m['city'],x,y-110,w=121,size=7.5,bold=True)
   txt(c,m['title'],x,y-122,w=121,size=6.6,color=MUTED)
  txt(c,f'ARCHIVE PART {part//2+1:02d} OF {PART_COUNT:02d}',44,46,size=7,color=MUTED)
  txt(c,f'{part+1} / {INDEX_PAGES}',512,46,w=50,size=7,color=MUTED);c.showPage()
 c.save();return path

def ft(s,b=True):return ImageFont.truetype(F+('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'),s)
def label(im,t,x,y,size=44,color=INK,b=True,w=None):
 d=ImageDraw.Draw(im);f=ft(size,b)
 while w and d.textbbox((0,0),t,font=f)[2]>w and size>18:size-=1;f=ft(size,b)
 box=d.textbbox((x,y),t,font=f)
 assert box[0]>=0 and box[2]<=3000 and box[1]>=0 and box[3]<=2250,(t,box)
 d.text((x,y),t,font=f,fill=color)

def block(im,t,x,y,size=44,color=INK,b=True,spacing=1.3):
 for line in t.split('\n'):label(im,line,x,y,size,color,b);y+=round(size*spacing)
 return y

def base(dark=False):
 im=Image.new('RGB',(3000,2250),NAVY if dark else CREAM);d=ImageDraw.Draw(im)
 d.line((390,225,2610,225),fill=GOLD,width=3)
 label(im,'HERITAGE IN GLASS',390,140,33,CREAM if dark else NAVY)
 label(im,'HISTORIC LANDMARK COLLECTION',1920,150,23,GOLD,w=690)
 return im

def footer(im,dark=False):
 d=ImageDraw.Draw(im);d.line((390,1950,2610,1950),fill=GOLD,width=2)
 label(im,'DIGITAL ARTWORK ONLY · NO PHYSICAL COASTERS INCLUDED',390,1995,28,CREAM if dark else INK,w=2220)
 label(im,'200 JPG designs · 3000 × 3000 pixel exports · English guide & index',390,2055,26,'#CCD7DC' if dark else MUTED,False,w=2220)

def tile(im,n,x,y,size):im.paste(art(n,size),(x,y))

def marketing(hero_only=False):
 out=P/'etsy';out.mkdir(exist_ok=True)
 # Hero: large, true artwork samples and a direct offer.
 im=base(True)
 block(im,'200\nSTAINED GLASS\nCOASTER DESIGNS',390,345,83,CREAM)
 block(im,'Historic cities.\nRemarkable architecture.\nJewel-toned circular artwork.',390,770,40,'#D7E0E3',False,1.55)
 d=ImageDraw.Draw(im);d.rounded_rectangle((390,1100,1290,1190),radius=45,fill=GOLD)
 label(im,'200 JPGs  /  3000 × 3000 PX',435,1123,32,NAVY,w=815)
 label(im,'Round art on ivory square canvases',390,1255,31,CREAM,False,w=1050)
 label(im,'Personal & physical-product use',390,1320,31,CREAM,False,w=1050)
 tile(im,1,1530,340,950);tile(im,69,1300,1255,520);tile(im,140,1920,1255,520)
 footer(im,True);im.save(out/'01_Hero.jpg',quality=95,subsampling=0)
 if hero_only:return out
 # Selection: twelve different samples, not 100 thumbnails too small to see.
 im=base();label(im,'A WORLD OF HISTORIC INSPIRATION',390,300,63,w=2220)
 label(im,'12 examples from the 200-design collection',390,410,34,MUTED,False)
 picks=[1,20,26,43,69,77,81,96,114,140,152,179]
 for i,n in enumerate(picks):
  x=405+(i%4)*565;y=550+(i//4)*435
  tile(im,n,x,y,365)
  m=A[f'{n:03d}'];label(im,m['id']+' / '+m['city'],x,y+372,24,w=520)
 footer(im);im.save(out/'02_Collection-Preview.jpg',quality=95,subsampling=0)
 # Detail panel: real file crops rendered at high resolution.
 im=base();label(im,'COLOR, TEXTURE & ARCHITECTURE',390,300,63,w=2220)
 label(im,'Dark outlines, decorative borders and luminous glass-style color',390,410,32,MUTED,False,w=2220)
 tile(im,26,470,560,1020)
 tile(im,81,1600,560,920)
 label(im,'Colosseum · Rome',470,1640,36)
 label(im,'Kinkaku-ji · Kyoto',1600,1535,36)
 label(im,'AI-generated decorative interpretations',470,1770,30,MUTED,False)
 label(im,'Not documentary or exact architectural reconstructions',470,1825,28,MUTED,False,w=2100)
 footer(im);im.save(out/'03_Artwork-Detail.jpg',quality=95,subsampling=0)
 # File facts: precise, verifiable and clear about the JPEG background.
 im=base();label(im,'KNOW EXACTLY WHAT YOU GET',390,300,70,w=2220)
 tile(im,69,1710,590,860)
 facts=[('200 UNIQUE DESIGNS','One JPG for each numbered motif.'),('3000 × 3000 PX EXPORTS','Digitally resized from AI-generated originals.'),('RGB / sRGB JPG','300 DPI metadata; raster artwork.'),('ROUND ART, SQUARE CANVAS','Warm ivory corners; not transparent.'),('BONUS INDEX & DESIGN LIST','Match thumbnail IDs to filenames.')]
 for i,(head,body) in enumerate(facts):
  y=550+i*240;label(im,head,390,y,33,NAVY,w=1240);label(im,body,390,y+73,28,MUTED,False,w=1240)
 label(im,'No SVG · No PNG · No editable layers',1710,1530,27,MUTED,False,w=900)
 footer(im);im.save(out/'04_File-Details.jpg',quality=95,subsampling=0)
 # Practical process and exact delivery route.
 im=base();label(im,'DOWNLOAD. CHOOSE. CREATE.',390,300,80,w=2220)
 label(im,'Delivered through a PDF guide with links to five ZIP parts',390,430,33,MUTED,False,w=2220)
 for i,(head,body,n) in enumerate([('01 / DOWNLOAD','Get all five parts. Extract the ZIP files.',1),('02 / CHOOSE','Find your motif in the numbered index.',114),('03 / PREPARE','Size to your blank and print a test.',96)]):
  x=390+i*755;tile(im,n,x+30,630,615);label(im,head,x,1320,34,w=710);label(im,body,x,1400,26,MUTED,False,w=710)
 block(im,'Adjust size, bleed and color settings for your own printer and blank.\nPhysical print results depend on your equipment and materials.',390,1660,30,MUTED,False,1.65)
 footer(im);im.save(out/'05_How-to-Use.jpg',quality=95,subsampling=0)
 # Physical use permissions without invented exclusivity guarantees.
 im=base(True);label(im,'CREATE PHYSICAL PRODUCTS',390,300,80,CREAM,w=2220)
 label(im,'Personal projects and physical products for sale are permitted.',390,440,34,'#CCD7DC',False,w=2220)
 tile(im,32,450,650,750);tile(im,51,1740,650,750)
 label(im,'INCLUDED PERMISSION',450,1530,34,GOLD)
 label(im,'Personal projects & physical end products',450,1610,31,CREAM,False,w=2130)
 label(im,'NOT INCLUDED',450,1720,31,GOLD)
 label(im,'Digital resale, file sharing or exclusive ownership',450,1780,30,CREAM,False,w=2130)
 footer(im,True);im.save(out/'06_Usage-and-License.jpg',quality=95,subsampling=0)
 return out

def parts():
 folder=P/'downloads';folder.mkdir(exist_ok=True)
 paths=[]
 for part in range(PART_COUNT):
  name=f'Heritage-in-Glass-Part-{part+1:02d}.zip';path=folder/name
  with zipfile.ZipFile(path,'w',zipfile.ZIP_STORED) as z:
   for m in M[part*PER_PART:(part+1)*PER_PART]:z.write(P/'JPG'/m['filename'],'JPG/'+m['filename'])
   if part==0:
    for name in ['Design-Index.pdf','Design-List.csv','Read-Me.txt','License.txt']:z.write(P/name,name)
  assert path.stat().st_size<99_000_000,'GitHub single-file delivery limit exceeded; archive needs repartitioning.'
  with zipfile.ZipFile(path) as z:assert z.testzip() is None
  paths.append(path)
 return paths

def guide(ref='main'):
 links=[f'https://github.com/semihaksan90-ops/GPT/raw/{ref}/historical-stained-glass/downloads/Heritage-in-Glass-Part-{i:02d}.zip' for i in range(1,PART_COUNT+1)]
 path=P/'Buyer-Download-Guide.pdf';c=canvas.Canvas(str(path),pagesize=(595.276,841.89),pageCompression=1);c.setTitle('Heritage in Glass — Download Your 200 Designs');c.setAuthor('Heritage in Glass')
 for group,picks in enumerate([[1,26,69,81]]):
  c.setFillColor(HexColor(CREAM));c.rect(0,0,596,843,fill=1,stroke=0)
  txt(c,'HERITAGE IN GLASS',44,800,size=11,bold=True,color=NAVY)
  txt(c,'Your 200-design collection' if group==0 else 'Continue your download',44,756,size=25,bold=True)
  txt(c,'Historic cities & landmarks · ALL FIVE DOWNLOAD PARTS',44,707,size=10,color=MUTED)
  for n,x in zip(picks,[44,175,306,437]):
   im=art(n,345);b=BytesIO();im.save(b,format='JPEG',quality=88);c.drawImage(ImageReader(BytesIO(b.getvalue())),x,545,115,115)
  txt(c,'Download all five parts',44,510,size=16,bold=True)
  txt(c,'Each ZIP holds 40 different JPGs. Download all five parts to obtain all 200 designs. The Design Index, Design List, Read-Me and License are in Part 01. Open this PDF in a viewer that allows web links.',44,478,size=10)
  y=400
  for j in range(5):
   i=group*5+j+1;url=links[i-1]
   c.setFillColor(HexColor(NAVY));c.roundRect(44,y-44,507,44,5,fill=1,stroke=0)
   txt(c,f'DOWNLOAD PART {i:02d}   /   DESIGNS {(i-1)*PER_PART+1:03d}–{i*PER_PART:03d}',58,y-11,w=480,size=11,color=CREAM,bold=True)
   c.linkURL(url,(44,y-44,551,y),relative=0,thickness=0);y-=60
  txt(c,'Download ZIP files to a computer or a device with ZIP extraction support. Extract them before opening the JPGs. If a link opens a hosting page, choose the download option. No physical products are included.',44,92,size=8.5,color=MUTED)
  txt(c,f'{group+1} / 2',515,43,w=45,size=7,color=MUTED);c.showPage()
 c.setFillColor(HexColor(CREAM));c.rect(0,0,596,843,fill=1,stroke=0)
 txt(c,'BEFORE YOU PRINT',44,800,size=22,bold=True)
 y=747
 info=[('Your files','200 RGB/sRGB JPG exports, 3000 × 3000 pixels, with 300 DPI metadata. The circular artwork is flattened onto an ivory square background; it is not a transparent PNG or an SVG.'),('Size to your own blank','Match the outer circle, not simply the square canvas width, to your blank or supplier template. Adjust bleed and positioning for your own process. Print a plain-paper test before final production.'),('Color and production','Follow your equipment, ink, transfer and blank supplier settings. Mirror only when your process requires it. No physical print or sublimation test was performed during file preparation.'),('Usage','The included terms allow personal projects and physical products for sale. Digital file resale, sharing and redistribution are not permitted. No exclusivity is promised. Read License.txt before use.'),('Decorative interpretation','These AI-generated artworks are stylized interpretations, not exact architectural surveys or historically verified reconstructions. No affiliation with depicted sites is implied.')]
 for title,body in info:
  y=txt(c,title,44,y,size=12,bold=True)-7;y=txt(c,body,44,y,size=10)-20
 txt(c,'2 / 2',515,43,w=45,size=7,color=MUTED)
 c.save();(P/'download-links.json').write_text(json.dumps({'ref':ref,'parts':links},indent=2));return path

def seller_kit():
 path=P/'Seller-Kit-EN.zip'
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted((P/'etsy').glob('*.jpg')):z.write(f,'Etsy-Images/'+f.name)
  for name in ['Etsy-Listing-EN.txt','SELLER-READ-ME.txt','Buyer-Download-Guide.pdf','Quality-Notes.txt']:
   z.write(P/name,name)
  z.write(P/'Design-Index.pdf','Design-Index.pdf')
 return path

def main():
 args=argparse.ArgumentParser();args.add_argument('--ref',default='main');ns=args.parse_args()
 missing=[m['id'] for m in M if not (P/'JPG'/m['filename']).exists()]
 if missing:raise RuntimeError(f'Cannot publish a 200-design bundle: {len(missing)} JPGs are still missing.')
 catalog();marketing();paths=parts();guide(ns.ref);seller_kit()
 print('Built 200-design collection, 5 archive parts, English index, 6 listing images, buyer guide and seller kit.')
 for path in paths:print(path.name,f'{path.stat().st_size/1024/1024:.1f} MiB')
if __name__=='__main__':main()
