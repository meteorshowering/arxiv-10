import cv2
import os
import layoutparser as lp
from paddleocr import PPStructure,draw_structure_result,save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from PIL import Image
import json

table_engine = PPStructure(show_log=True)
figure_count = 0
figures_info = []
paper_result = []
def single_page_process(img_path,figure_folder):
    global table_engine
    global figures_info
    global figure_count

    page_num =(img_path.split('_')[1]).split('.')[0]
    #below is the process on a single page of a pdf
    img = cv2.imread(img_path)
    result = table_engine(img)    #get layout
    # save_structure_res(result, os.path.join(save_folder,"qlora"),os.path.basename(img_path).split('.')[0])
    # 保存在每张图片对应的子目录下
    h, w, _ = img.shape
    res = sorted_layout_boxes(result, w)   #这个函数是左右分栏的处理函数，厉害，效果很好
    #print(res)  #sort之后的结果是list

    #以下代码用来把table\figure作为图片存下来
    figure_per_page = 0
    res_useful =[]
    # below is process on single region parsered by paddle-ppstructure on a certain page 
    concat_fig_flag = 0
    for region in res:
        useful_info={}
        useful_info['type'] = region['type']
        useful_info['bbox'] = region['bbox']
        useful_info['text'] = ''
        if (type(region['res']).__name__=='list'):
            for i in range(len(region['res'])):
                useful_info['text'] += region['res'][i]['text'] + '.'
        else:
            print(region['res'])
        res_useful.append(useful_info)
        paper_result.append(useful_info)
    for i in range(len(res_useful)):
        # if res_useful[i]['type'] == 'table' or res_useful[i]['type'] == 'figure':
        if res_useful[i]['type'] == 'figure':
            if concat_fig_flag == 1:
                concat_fig_flag =0
                continue
            figure_info = {}
            figure_count += 1
            figure_per_page += 1
            figure_img = img[res_useful[i]['bbox'][1]:res_useful[i]['bbox'][3],res_useful[i]['bbox'][0]:res_useful[i]['bbox'][2]]
            figure_addr = figure_folder+'/'+str(figure_count)+'.jpg'
            figure_info['figure_per_eassy'] = figure_count
            figure_info['page'] = page_num
            figure_info['figure_per_page'] = figure_per_page
            figure_info['addr'] = figure_addr
            figure_info['context'] = ''
            if i >= (len(res_useful)-1):
                pass
            else:
                if res_useful[i+1]['type'] == 'figure':
                    concat_fig_flag = 1
                    figure_img = img[res_useful[i]['bbox'][1]:res_useful[i+1]['bbox'][3],res_useful[i]['bbox'][0]:res_useful[i+1]['bbox'][2]]
                elif res_useful[i+1]['type'] == 'figure_caption' or res_useful[i+1]['type'] == 'text' or res_useful[i+2]['type'] == 'reference':
                    figure_info['context'] += res_useful[i+1]['text']+'\n'
            if i >= (len(res_useful)-2):
                pass
            else:
                if res_useful[i+2]['type'] == 'text' or res_useful[i+2]['type'] == 'figure_caption' or res_useful[i+2]['type'] == 'reference':
                    if "figure" in res_useful[i+2]['text'] or "Figure" in res_useful[i+2]['text'] or "Fig" in res_useful[i+2]['text']:
                        figure_info['context'] += res_useful[i+2]['text']
            cv2.imwrite(figure_addr,figure_img)
            figures_info.append(figure_info)
    return True
def main():
    pdfimg_dir = './imgs'
    for pdf in os.listdir(pdfimg_dir):
        img_dir = os.path.join(pdfimg_dir,pdf)
        figure_folder = 'arxivs/'+pdf
        if not os.path.exists(figure_folder):
            os.makedirs(figure_folder)
        imgs = os.listdir(img_dir)
        imgs.sort(key=lambda x:int((x.split('_')[1]).split('.')[0]))
        global figures_info
        global figure_count
        global paper_result
        for img in imgs:
            img_path = os.path.join(img_dir,img)    #pdf to imgs
            single_page_process(img_path,figure_folder)
        figures_info_addr = figure_folder+'/figures_info.json'
        paper_result_addr = figure_folder + '/result.json'
        with open(figures_info_addr,'w') as jsonfile:
            json.dump(figures_info,jsonfile,indent=2)
        with open(paper_result_addr,'w') as jsonfi:
            json.dump(paper_result,jsonfi,indent=2)
        figure_count = 0
        figures_info = []
        paper_result = []


main()

#以下代码用来在图片上画region框框，以及ocr的结果
# font_path = 'doc/fonts/simfang.ttf' # PaddleOCR下提供字体包
# im_show = draw_structure_result(img, result,font_path=font_path)
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')

# convert_info_doc(img, res, save_folder, os.path.basename(img_path).split('.')[0])



# image = cv2.imread('imgs/CLIP/images_3.img')
# image = image[..., ::-1]

# # 加载模型
# model = lp.PaddleDetectionLayoutModel(config_path="lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
#                                 threshold=0.5,
#                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
#                                 enforce_cpu=False ,
#                                 enable_mkldnn=True)
# # 检测
# layout = model.detect(image)

# # 显示结果
# show_img = lp.draw_box(image, layout, box_width=3, show_element_type=True)


