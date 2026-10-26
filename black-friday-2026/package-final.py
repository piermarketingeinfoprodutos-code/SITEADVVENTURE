from pathlib import Path
from html.parser import HTMLParser
import shutil,re,hashlib,zipfile,json

root=Path(__file__).parent
name='Página Black Friday 2026 versão final Adventure'
destination=root.parent/'entrega-final'/name
destination.mkdir(parents=True,exist_ok=True)
files=['index.html','style.css','final.css','final-app.js','calculo.js','config.js','LEIA-ME-PUBLICACAO.txt']
assets=['logo-campanha.png','gabriel-sorriso-recortado.png','gabriel-serio.jpeg','estrutura-contabil.png','janeiro-2027.png','advogado-comparativo.png','best-lawyers-2020-2026.png','carimbo-30-off.svg','fonts/anton.ttf','fonts/manrope.ttf','fonts/anton-OFL.txt','fonts/manrope-OFL.txt']
for f in files:
    shutil.copy2(root/f,destination/f)
for f in assets:
    target=destination/'assets'/f;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(root/'assets'/f,target)
original=destination/'assets/originais/gabriel-sorriso-original.jpg'
original.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/'assets/gabriel-sorriso-original.jpg',original)
class References(HTMLParser):
    def __init__(self):super().__init__();self.refs=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('src','href') and v and not v.startswith(('#','http','mailto:','tel:')):self.refs.append(v)
parser=References();content=(destination/'index.html').read_text(encoding='utf-8');parser.feed(content)
assert len(re.findall(r'<section\b',content))==15
assert not re.search(r'sem juros|2020 a 2024|class="timeline"|data-preview',content,re.I)
assert not re.search(r'[CG]:[\\/]|file://|localhost|127\.0\.0\.1',content)
hero=re.search(r'<section class="hero">.*?</section>',content,re.S).group(0)
assert not re.search(r'R\$|data-installment|data-total|cash-price',hero)
refs=parser.refs[:]
for f in ['style.css','final.css']:
    for value in re.findall(r'url\([\'"]?([^\)\'\"]+)',(destination/f).read_text(encoding='utf-8')):
        if not value.startswith(('http','data:')): refs.append(value)
missing=[f for f in refs if not (destination/f).is_file()]
assert not missing,missing
manifest=[]
for f in sorted(destination.rglob('*')):
    if f.is_file() and f.name!='MANIFESTO-SHA256.txt':manifest.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(destination).as_posix())
(destination/'MANIFESTO-SHA256.txt').write_text('\n'.join(manifest)+'\n',encoding='utf-8')
archive=root.parent/(name+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(destination.rglob('*')):
        if f.is_file():z.write(f,Path(name)/f.relative_to(destination))
with zipfile.ZipFile(archive) as z: assert z.testzip() is None
print(json.dumps({'archive':str(archive.resolve()),'directory':str(destination.resolve()),'files':len(manifest)+1,'bytes':archive.stat().st_size,'local_references_verified':len(refs)},ensure_ascii=False))
