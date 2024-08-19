import os
import json
papersAddr = "./arxivs"
for paper in os.listdir(papersAddr):
    paperAddr = os.path.join(papersAddr,paper)
    picContext_pairs = []
    resultjson = paperAddr+'/result.json'
    textconAddr = paperAddr + '/cleancontext.json'
    cleancontext = []
    with open(resultjson,'r') as jsonfile:
        picContext_pairs = json.load(jsonfile)       
    for pair in picContext_pairs:
        segment = {}
        num_pic = 0
        if pair["type"] == "title":
            segment["type"] = "title"
            segment["text"] = pair["text"]            
            cleancontext.append(segment)
        if pair["type"] == "text":
            segment["type"] = "text"
            segment["text"] = pair["text"]
            cleancontext.append(segment)
        if pair["type"] == "figure":
            segment["type"] = "figure"
            num_pic = num_pic+1
            segment["num"] = num_pic
            cleancontext.append(segment)
    with open(textconAddr,'w') as file:
        json.dump(cleancontext,file,indent=2)

     