from pathlib import Path
from PIL import Image
D=Path(__file__).parent
base=Path('C:/Users/paulr/.codex/codex-remote-attachments/01a16758-475a-7f73-add3-8ae91c534e09/EF52C7EA-AF24-4E37-BE81-73F369795A57')
for i in range(1,11):
    im=Image.open(base/f'{i}-写真{i}.jpg')
    w,h=im.size
    for k,(left,right) in {'FG':(int(w*.55),w),'D':(int(w*.30),int(w*.59))}.items():
        crop=im.crop((left,0,right,h));crop=crop.resize((crop.width*2,crop.height*2))
        crop.save(D/'_private'/f'photo_{i}_{k}.png')
print('Inspection crops saved for 10 source images; original images unchanged.')
