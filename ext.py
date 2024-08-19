import os 
import filetype
import shutil
res_dir = "result"
files = os.listdir(res_dir)
target='extractedimgs'
for fi in files:
    print(fi)
    os.mkdir(os.path.join(target,fi))
    fi_dir=os.path.join(res_dir,fi)
    num=0
    datas=os.listdir(fi_dir)
    datas.sort(key=lambda x:int(x.split('_')[1]))
    for data in datas:
        data_dir=os.path.join(fi_dir,data)
        for txt in os.listdir(data_dir):
            #print(txt)
            txt_dir=os.path.join(data_dir,txt)
            txttype=filetype.guess(txt_dir)
            if txttype==None:
                pass
            else:
                txttype=txttype.extension
            if txttype=="jpg":
                num=num+1
                new_dir=os.path.join(target,fi,str(num)+'.jpg')
                #new_dir
                print(txt_dir)
                #print(new_dir)
                shutil.copyfile(txt_dir,new_dir)