import os
import sys
try:
    import cv2
    import easyocr
    from rich import print
except:
    os.system('pip install easyocr')
    os.system('pip install rich')
    os.system('pip install open-cv2')
    import cv2
    import easyocr
    from rich import print

print('''
[bold green]
          
>>=========================<<
||   ____   _______     __ ||
||  (    ) (_   (_ \   / _)||
||  / /\ \   | |  \ \_/ /  ||
|| ( (__) )  | |   \   /   ||
||  )    (   | |   / _ \   ||
|| /  /\  \ _| |__/ / \ \_ ||
||/__(  )__/____(__/   \__)||
>>=========================<<     
          
         [/bold green] ''')


def set_new_var(text):
    print(f'[bold blue] [ ? ] [/bold blue][bold yellow]{text} [Y]es/[N/o: (Enter For default)[/bold yellow]',end='')
    d=input('')
    if d!='':
        return d
    else:
        return None



#=========================== تنظیمات =============================
data_dir    = 'data' #نام پوشه دیتا
tmp=set_new_var("Enter data_dir: ")
if tmp:data_dir=tmp

output_file = 'recognized_texts_easyocr.txt' #نام فایل خروجی
tmp=set_new_var("Enter output file: ")
if tmp:output_file=tmp

LANGS       = ['fa']   # زبان فارسی
GPU=False
tmp=set_new_var("Enter GPU: ")
if tmp:GPU=bool(tmp)


#=================================================================




def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def recognize_with_easyocr(data_folder, output_path):
    reader = easyocr.Reader(LANGS, gpu=GPU)
    files = sorted([f for f in os.listdir(data_folder)
                    if f.lower().endswith(('.png','.jpg','.jpeg'))],
                   key=lambda x: int(os.path.splitext(x)[0]))
    
    with open(output_path, 'w', encoding='utf-8') as fout:
        for fname in files:
            path = os.path.join(data_folder, fname)
            img = preprocess_image(path)
            results = reader.readtext(img, detail=0, paragraph=True)
            text = ' '.join(results).strip()
            if not text:
                text = '<متن قابل تشخیص نیست>'
            fout.write(f"{fname} → {text}\n")
            print(f"✔ {fname}: {text}")
    print(f"\n✨ پایان. نتایج در «{output_path}» ذخیره شد.")

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    if not os.path.isdir(data_dir):
        print(f"خطا: پوشه داده «{data_dir}» وجود ندارد.")
        sys.exit(1)
    recognize_with_easyocr(data_dir, output_file)
