"""Restore working JPG files from the delivered archive parts after a fresh checkout."""
from pathlib import Path
from zipfile import ZipFile
import json
P=Path(__file__).resolve().parent
names={m['filename'] for m in json.loads((P/'source/motifs.json').read_text())}
out=P/'JPG';out.mkdir(exist_ok=True)
seen=set()
for part in range(1,6):
 with ZipFile(P/'downloads'/f'Heritage-in-Glass-Part-{part:02d}.zip') as z:
  for name in z.namelist():
   if not name.startswith('JPG/') or not name.endswith('.jpg'):continue
   leaf=name.split('/',1)[1]
   assert leaf in names and '/' not in leaf and '\\' not in leaf
   path=out/leaf
   if not path.exists():path.write_bytes(z.read(name))
   seen.add(leaf)
assert seen==names
print('All 200 JPG working files are available in JPG/.')
