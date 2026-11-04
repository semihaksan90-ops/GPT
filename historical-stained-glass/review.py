from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
P=Path(__file__).resolve().parent
M=json.loads((P/'source/motifs.json').read_text());out=P/'review';out.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
fontb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',21)
records=[]
for group in range((len(M)+19)//20):
 im=Image.new('RGB',(1800,1580),'#E4DFD1');d=ImageDraw.Draw(im);d.text((20,15),f'DESIGNS {group*20+1:03d}–{group*20+20:03d}',font=fontb,fill='#102C3B')
 for i,m in enumerate(M[group*20:(group+1)*20]):
  x=20+(i%5)*356;y=65+(i//5)*375
  log=P/'source/generated'/f"{m['id']}.json"
  if log.exists():
   r=json.loads(log.read_text());path=Path(r['path'])
   with Image.open(path) as src:
    w,h=src.size;gray=src.convert('L');dark=gray.point(lambda x:255 if x<65 else 0);bbox=dark.getbbox()
    clipped=bool(bbox and (bbox[0]<2 or bbox[1]<2 or bbox[2]>w-2 or bbox[3]>h-2))
    records.append({'id':m['id'],'size':[w,h],'dark_bbox':bbox,'edge_review_needed':clipped,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pixels_sha256':hashlib.sha256(src.convert('RGB').tobytes()).hexdigest()})
    thumb=src.convert('RGB');thumb.thumbnail((330,330));im.paste(thumb,(x,y))
  else:d.rectangle((x,y,x+330,y+330),fill='#CBC7BB');d.text((x+20,y+140),'NOT GENERATED',font=font,fill='#514E44')
  d.text((x,y+334),m['id']+' / '+m['city'],font=font,fill='#102C3B')
  title=m['title'];d.text((x,y+355),title[:35],font=font,fill='#52656A')
 im.save(out/f'Contact-{group+1:02d}.jpg',quality=92)
(P/'source/artwork-review.json').write_text(json.dumps(records,indent=2))
print('Review records:',len(records),'Edge flags:',[x['id'] for x in records if x['edge_review_needed']])
