from pathlib import Path
from collections import Counter
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json, csv, hashlib, base64

root=Path(__file__).resolve().parent
source=root/'kartu-01-11-nov2026.json'
out=root
rows=json.loads(source.read_text(encoding='utf-8-sig'))
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
assert len(rows)==121
assert len({(r['source'],r['source_card']) for r in rows})==121
assert all(r['source'] and r['source_card'] and r['verification'] for r in rows)
def prize(r): return 'umrah' if 'umrah' in r['prize'].lower() else 'zamzam'
counts=Counter((prize(r),r['code'],int(r['date'][-2:])) for r in rows)
totals=Counter(prize(r) for r in rows)
assert totals=={'umrah':11,'zamzam':110}
for d in range(1,12):
    assert sum(v for (p,c,day),v in counts.items() if p=='umrah' and day==d)==1
    assert sum(v for (p,c,day),v in counts.items() if p=='zamzam' and day==d)==10
umrah=Counter({c:sum(counts['umrah',c,d] for d in range(1,12)) for c in {r['code'] for r in rows}})
assert +umrah=={'EG':3,'PK':3,'BD':3,'MA':1,'SY':1}
assert {c:counts['zamzam',c,8] for c in ['IN','EG','SA','PK','BD']}=={'IN':2,'EG':3,'SA':3,'PK':1,'BD':1}
for day,expected in [(10,{'PK':3,'EG':2,'BD':1,'YE':1,'PH':1,'IN':1,'AF':1}),(11,{'EG':4,'PK':3,'BD':2,'TD':1})]:
    assert {c:n for (p,c,d),n in counts.items() if p=='zamzam' and d==day}==expected
assert counts['umrah','BD',10]==1 and counts['umrah','PK',11]==1
codes=sorted({r['code'] for r in rows},key=lambda c:(-sum(r['code']==c for r in rows),c))
flags_path=root/'flag-assets.json'
flags={r['code'].upper():Image.open(BytesIO(base64.b64decode(r['data']))).convert('RGBA') for r in json.loads(flags_path.read_text())}
assert set(codes)<=set(flags)
zamzam_codes=[c for c in codes if sum(counts['zamzam',c,d] for d in range(1,12))>0]
assert len(zamzam_codes)==13 and not {'MA','SY'} & set(zamzam_codes)
S=2; W,H=924,1260
im=Image.new('RGB',(W*S,H*S),'#0e1b2c'); draw=ImageDraw.Draw(im)
def text(x,y,t,size=20,bold=False,fill='#f1f7ff',anchor='la'):
    font=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',size*S)
    draw.text((x*S,y*S),t,font=font,fill=fill,anchor=anchor)
palette=['#172c3c','#165564','#176b78','#45f4e5','#d6ff58']
def color(n): return palette[0 if n==0 else 1 if n==1 else 2 if n<=3 else 3 if n<=5 else 4]
def box(x,y,size,n):
    draw.rounded_rectangle((x*S,y*S,(x+size)*S,(y+size)*S),radius=4*S,fill=color(n))
text(48,26,'Nusuk Challenge',34,True,fill='#45f4e5')
text(48,75,'Pemenang per negara | 1-11 November 2026',21,fill='#a8bdd2')
X,STEP,SIZE=204,52,36
rendered=[]
for p,title,top in [('umrah','Umrah',132),('zamzam','Zamzam',514)]:
    countries=sorted([c for c in codes if umrah[c]>0],key=lambda c:(-umrah[c],c)) if p=='umrah' else zamzam_codes
    text(48,top,title,28,True,fill='#45f4e5')
    text(W-48,top,f'{totals[p]} pemenang',20,True,fill='#d6ff58',anchor='ra')
    text(48,top+50,'Negara',16,fill='#a8bdd2')
    text(W-48,top+50,'Total',16,fill='#a8bdd2',anchor='ra')
    for d in range(1,12):text(X+(d-1)*STEP+SIZE/2,top+50,f'{d:02}',18,True,anchor='ma')
    for i,c in enumerate(countries):
        y=top+84+i*42
        flag=flags[c].copy(); flag.thumbnail((43*S,27*S),Image.Resampling.LANCZOS)
        im.paste(flag,(48*S,(y+3)*S),flag)
        text(108,y+3,c,21,True)
        text(W-48,y+3,str(sum(counts[p,c,d] for d in range(1,12))),21,True,anchor='ra')
        for d in range(1,12):
            n=counts[p,c,d];x=X+(d-1)*STEP
            rendered.append({'hadiah':p,'kode_negara':c,'tanggal':f'2026-11-{d:02}','jumlah':n})
            box(x,y,SIZE,n)
            text(x+SIZE/2,y+SIZE/2,str(n),20 if n else 15,bool(n),'#07111f' if n>=4 else '#f1f7ff' if n else '#a8bdd2','mm')
    y=top+84+len(countries)*42+12
    text(48,y,'Per hari',16,fill='#a8bdd2')
    for d in range(1,12):text(X+(d-1)*STEP+SIZE/2,y,str(sum(counts[p,c,d] for c in countries)),17,True,anchor='ma')
    text(W-48,y,str(totals[p]),17,True,anchor='ra')
draw.line((48*S,480*S,(W-48)*S,480*S),fill='#23485e',width=S)
text(48,1200,'121 kartu terverifikasi | 1 kartu = 1 pemenang',16,fill='#a8bdd2')
for k,(n,label) in enumerate([(0,'0'),(1,'1'),(2,'2-3'),(4,'4-5'),(6,'6+')]):
    x=510+k*74;box(x,1196,21,n);text(x+27,1198,label,15,fill='#a8bdd2')
text(48,1230,'Sumber: Aplikasi Nusuk',14,fill='#a8bdd2')
stem='Pemenang-Nusuk-01-11-November-2026-NKL'
im.save(out/f'{stem}.png',dpi=(200,200))
im.save(out/f'{stem}.pdf','PDF',resolution=200)
with (out/'agregat-grafik.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['hadiah','kode_negara','tanggal','jumlah']);writer.writeheader();writer.writerows(rendered)
validation={'source':source.name,'source_sha256':source_hash,'rows':len(rows),'unique_source_cards':121,'totals':dict(totals),'umrah_country_totals':dict(+umrah),'daily':{f'2026-11-{d:02}':{p:sum(counts[p,c,d] for c in codes) for p in ['umrah','zamzam']} for d in range(1,12)},'rendered_cells':len(rendered),'rendered_total':sum(r['jumlah'] for r in rendered),'flag_assets_source':'Prior chart flag assets plus PH and TD from flagcdn.com via BrowserOS neo on 12 November 2026','source_unchanged':source_hash==hashlib.sha256(source.read_bytes()).hexdigest(),'chart':f'{stem}.png','chart_sha256':hashlib.sha256((out/f'{stem}.png').read_bytes()).hexdigest(),'scope':'Baseline audit99 retained; 22 new cards transcribed visually from screenshots supplied 12 November.'}
assert validation['rendered_total']==121 and validation['source_unchanged']
validation.update(theme='NKL dark navy, teal and lime',palette=palette,zamzam_country_rows=len(zamzam_codes),zamzam_country_codes=zamzam_codes,footer='Sumber: Aplikasi Nusuk',image_dimensions=list(im.size))
(out/'validasi.json').write_bytes(json.dumps(validation,indent=2).encode('utf-8'))
print(json.dumps(validation,indent=2))
