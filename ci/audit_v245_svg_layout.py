#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, re
import xml.etree.ElementTree as ET
from PIL import ImageFont

NUM=r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?'

def mul(a,b):
    # SVG affine [a c e; b d f; 0 0 1]
    a1,b1,c1,d1,e1,f1=a; a2,b2,c2,d2,e2,f2=b
    return (a1*a2+c1*b2, b1*a2+d1*b2, a1*c2+c1*d2, b1*c2+d1*d2, a1*e2+c1*f2+e1, b1*e2+d1*f2+f1)

def pt(m,x,y):
    a,b,c,d,e,f=m; return (a*x+c*y+e,b*x+d*y+f)

def parse_transform(s):
    m=(1,0,0,1,0,0)
    if not s: return m
    for name,args in re.findall(r'([A-Za-z]+)\s*\(([^)]*)\)',s):
        v=[float(x) for x in re.findall(NUM,args)]
        if name=='matrix' and len(v)>=6: t=tuple(v[:6])
        elif name=='translate': t=(1,0,0,1,v[0],v[1] if len(v)>1 else 0)
        elif name=='scale': t=(v[0],0,0,v[1] if len(v)>1 else v[0],0,0)
        elif name=='rotate':
            ang=math.radians(v[0]); c=math.cos(ang); s=math.sin(ang); r=(c,s,-s,c,0,0)
            if len(v)>=3:
                cx,cy=v[1],v[2]; t=mul(mul((1,0,0,1,cx,cy),r),(1,0,0,1,-cx,-cy))
            else: t=r
        elif name=='skewX':
            t=(1,0,math.tan(math.radians(v[0])),1,0,0)
        elif name=='skewY':
            t=(1,math.tan(math.radians(v[0])),0,1,0,0)
        else: continue
        m=mul(m,t)
    return m

def bbox_transform(m,b):
    x0,y0,x1,y1=b
    ps=[pt(m,x0,y0),pt(m,x1,y0),pt(m,x0,y1),pt(m,x1,y1)]
    xs=[p[0] for p in ps]; ys=[p[1] for p in ps]
    return (min(xs),min(ys),max(xs),max(ys))

def parse_style(svg_text):
    classes={}
    for st in re.findall(r'<style[^>]*>(.*?)</style>',svg_text,flags=re.S):
        for sel,body in re.findall(r'\.([\w-]+)\s*\{([^}]*)\}',st):
            props={}
            for k,v in re.findall(r'([\w-]+)\s*:\s*([^;]+)',body): props[k.strip()]=v.strip()
            classes[sel]=props
    return classes

def float_attr(e,k,default=0):
    try:return float(re.findall(NUM,e.attrib.get(k,str(default)))[0])
    except:return float(default)

def path_bbox(d):
    vals=[float(x) for x in re.findall(NUM,d or '')]
    if len(vals)<2:return None
    xs=vals[0::2]; ys=vals[1::2]
    return (min(xs),min(ys),max(xs),max(ys)) if ys else None

def shape_bbox(e):
    tag=e.tag.rsplit('}',1)[-1]
    if tag=='rect':
        x=float_attr(e,'x');y=float_attr(e,'y');w=float_attr(e,'width');h=float_attr(e,'height');return(x,y,x+w,y+h)
    if tag=='circle':
        x=float_attr(e,'cx');y=float_attr(e,'cy');r=float_attr(e,'r');return(x-r,y-r,x+r,y+r)
    if tag=='ellipse':
        x=float_attr(e,'cx');y=float_attr(e,'cy');rx=float_attr(e,'rx');ry=float_attr(e,'ry');return(x-rx,y-ry,x+rx,y+ry)
    if tag=='line':
        x1=float_attr(e,'x1');y1=float_attr(e,'y1');x2=float_attr(e,'x2');y2=float_attr(e,'y2');return(min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2))
    if tag in ('polyline','polygon'):
        vals=[float(x) for x in re.findall(NUM,e.attrib.get('points',''))];xs=vals[0::2];ys=vals[1::2];return(min(xs),min(ys),max(xs),max(ys)) if ys else None
    if tag=='path': return path_bbox(e.attrib.get('d',''))
    return None

def intersects(a,b,pad=0):
    return not (a[2] <= b[0]+pad or a[0] >= b[2]-pad or a[3] <= b[1]+pad or a[1] >= b[3]-pad)

def audit_file(path, ta_font, en_font):
    txt=path.read_text(); classes=parse_style(txt); root=ET.fromstring(txt)
    vb=[float(x) for x in re.findall(NUM,root.attrib.get('viewBox',''))]
    if len(vb)!=4:return {'file':path.name,'error':'missing viewBox'}
    vx,vy,vw,vh=vb; view=(vx,vy,vx+vw,vy+vh)
    is_ta=path.name.endswith(('_ta.svg','_t.svg')); font_path=ta_font if is_ta else en_font
    shapes=[]; texts=[]
    def walk(e,parent_m=(1,0,0,1,0,0),inherited=None):
        inherited=dict(inherited or {})
        cls=e.attrib.get('class','').split()
        for c in cls: inherited.update(classes.get(c,{}))
        for k in ('font-size','font-family','text-anchor','font-weight'):
            if k in e.attrib: inherited[k]=e.attrib[k]
        m=mul(parent_m,parse_transform(e.attrib.get('transform')))
        sb=shape_bbox(e)
        if sb is not None:
            shapes.append((e.tag.rsplit('}',1)[-1],bbox_transform(m,sb)))
        if e.tag.rsplit('}',1)[-1]=='text':
            size=float(re.findall(NUM,inherited.get('font-size','20'))[0])
            font=ImageFont.truetype(font_path,max(1,round(size)))
            anchor=e.attrib.get('text-anchor',inherited.get('text-anchor','start'))
            base_x=float_attr(e,'x'); base_y=float_attr(e,'y')
            runs=[]
            direct=(e.text or '').strip()
            if direct:runs.append((direct,base_x,base_y,anchor))
            current_y=base_y
            for ch in list(e):
                if ch.tag.rsplit('}',1)[-1]!='tspan':continue
                t=''.join(ch.itertext()).strip()
                if not t:continue
                x=float_attr(ch,'x',base_x)
                if 'y' in ch.attrib: current_y=float_attr(ch,'y')
                elif 'dy' in ch.attrib: current_y += float_attr(ch,'dy')
                runs.append((t,x,current_y,ch.attrib.get('text-anchor',anchor)))
            boxes=[]
            for t,x,y,anc in runs:
                l,tb,r,bb=font.getbbox(t)
                w=r-l
                x0=x if anc=='start' else x-w/2 if anc=='middle' else x-w
                b=(x0,y-size*0.85,x0+w,y+size*0.22)
                boxes.append(bbox_transform(m,b))
            if boxes:
                ub=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
                texts.append({'text':' / '.join(r[0] for r in runs),'bbox':ub,'fontSize':size})
        for c in list(e): walk(c,m,inherited)
    walk(root)
    overflow=[]; overlap=[]
    for t in texts:
        b=t['bbox']
        if b[0]<view[0]-0.5 or b[1]<view[1]-0.5 or b[2]>view[2]+0.5 or b[3]>view[3]+0.5:
            overflow.append(t)
        hits=[]
        for kind,sb in shapes:
            if kind=='rect' and abs(sb[0]-view[0])<1 and abs(sb[1]-view[1])<1 and abs(sb[2]-view[2])<1 and abs(sb[3]-view[3])<1: continue
            if intersects(b,sb,pad=1): hits.append({'shape':kind,'bbox':sb})
        if hits: overlap.append({'text':t['text'],'bbox':b,'shapes':hits[:8]})
    return {'file':path.name,'viewBox':view,'textCount':len(texts),'overflow':overflow,'overlapLeads':overlap}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('raw_dir'); ap.add_argument('--ta-font',required=True); ap.add_argument('--en-font',required=True); ap.add_argument('--out',required=True)
    a=ap.parse_args(); raw=Path(a.raw_dir)
    results=[audit_file(p,a.ta_font,a.en_font) for p in sorted(raw.glob('*.svg')) if p.name.endswith(('_ta.svg','_en.svg','_t.svg','_e.svg'))]
    out={'files':len(results),'overflowCount':sum(len(r.get('overflow',[])) for r in results),'overlapLeadCount':sum(len(r.get('overlapLeads',[])) for r in results),'results':results}
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n'); print(json.dumps({'files':out['files'],'overflowCount':out['overflowCount'],'overlapLeadCount':out['overlapLeadCount']},indent=2))
if __name__=='__main__':main()
