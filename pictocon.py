# this program is mainly used to use llm to generate conclusion given the picture and its context.
import ollama
import os 
import json
papersAddr = "./arxivs"

prompT = 'use three key words in English academic style to describe the main idea, in the form of "1.***,2.***,3.***"'
for paper in os.listdir(papersAddr):
    paperAddr = os.path.join(papersAddr,paper)
    picContext_pairs = []
    figinfoAddr = paperAddr+'/figures_info.json'
    with open(figinfoAddr,'r') as jsonfile:
         picContext_pairs = json.load(jsonfile)       
    for pair in picContext_pairs:
        picAddr = pair["addr"]
        context = pair["context"]
        res = ollama.chat(
            model="llava:7b",
            messages=[
                {
                    'role': 'user',
                    'content': 'Here is a image and some infomation related to it:' + context+ prompT,
                    'images': [picAddr]
                }
            ]
        )
        content = res['message']['content']
        pair['generate'] = content
    with open(paperAddr+'/figurein.json','w') as jsonfile:
         json.dump(picContext_pairs,jsonfile,indent=2)
        
