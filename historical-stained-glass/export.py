"""Convert individually generated artworks to documented, consistently sized JPG exports."""
from pathlib import Path
from PIL import Image,ImageCms
import json,hashlib,csv,sys
P=Path(__file__).resolve().parent
specs=json.loads((P/'source/motifs.json').read_text())
settings=json.loads((P/'source/export-settings.json').read_text())
profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
rows=[]
for m in specs:
 log=P/'source/generated'/f"{m['id']}.json"
 if not log.exists():continue
 r=json.loads(log.read_text());src=Path(r['path']);out=P/'JPG'/m['filename']
 with Image.open(src) as im:
  size=im.size
  if size[0]!=size[1]:raise RuntimeError(f"Non-square original {m['id']}: {size}; needs review, not automatic cropping.")
  if not out.exists() or src.stat().st_mtime>out.stat().st_mtime:
   im=im.convert('RGB').resize((3000,3000),Image.Resampling.LANCZOS)
   im.save(out,quality=settings['quality'],subsampling=settings['subsampling'],optimize=True,dpi=(300,300),icc_profile=profile)
 with Image.open(out) as im:assert im.mode=='RGB' and im.size==(3000,3000)
 row={k:m[k] for k in ['id','city','title','region','filename']}
 row.update({'source_width':size[0],'source_height':size[1],'export_width':3000,'export_height':3000,'export_dpi':300,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'method':'AI-generated original; resized JPG export','jpeg_quality':settings['quality'],'jpeg_subsampling':settings['subsampling']})
 rows.append(row)
(P/'source/export-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
if rows:
 with (P/'Design-List.csv').open('w',newline='',encoding='utf-8-sig') as f:
  fields={'id':'Design ID','city':'City','title':'Landmark','region':'Region','filename':'Filename','source_width':'Original width (px)','source_height':'Original height (px)','export_width':'JPG width (px)','export_height':'JPG height (px)'}
  w=csv.DictWriter(f,fieldnames=list(fields.values()));w.writeheader();w.writerows({label:r[key] for key,label in fields.items()} for r in rows)
print(f'{len(rows)}/{len(specs)} JPG exports prepared; {sum(x["bytes"] for x in rows)/1024/1024:.1f} MiB.')
if '--complete' in sys.argv:assert len(rows)==len(specs)
