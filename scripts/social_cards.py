#!/usr/bin/env python3
"""Deterministic social cards; only built at publication time."""
import json
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];public=root/'public'
fontroot=root/'assets/fonts'
for item in json.loads((public/'content-index.json').read_text())['items']:
    im=Image.new('RGB',(1200,630),'#f6f3ed');d=ImageDraw.Draw(im)
    title=ImageFont.truetype(str(fontroot/'DejaVuSerif.ttf'),64)
    label=ImageFont.truetype(str(fontroot/'DejaVuSans.ttf'),20)
    d.rectangle((0,0,1200,10),fill='#ac174d')
    d.text((65,53),'BRENNENSTUHL / ON SECURITY',font=label,fill='#ac174d')
    lines=[];line=''
    for word in item['title'].split():
        trial=(line+' '+word).strip()
        if d.textlength(trial,font=title)>1065 and line:lines.append(line);line=word
        else:line=trial
    lines.append(line)
    if len(lines)>5:
        title=ImageFont.truetype(str(fontroot/'DejaVuSerif.ttf'),48)
        lines=[];line=''
        for word in item['title'].split():
            trial=(line+' '+word).strip()
            if d.textlength(trial,font=title)>1065 and line:lines.append(line);line=word
            else:line=trial
        lines.append(line)
    y=145
    for line in lines:d.text((65,y),line,font=title,fill='#20232a');y+=title.size+14
    d.line((65,540,1135,540),fill='#d5d0c7',width=2)
    d.text((65,568),'Jan Brennenstuhl',font=label,fill='#20232a')
    d.text((850,568),'janbrennenstuhl.eu',font=label,fill='#5b6268')
    dest=public/urlsplit(item['canonical_url']).path.lstrip('/')/'social.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest,optimize=True)
print('Generated social cards.')
