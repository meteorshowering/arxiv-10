# this program is used to fetch and download papers from arxiv
import arxiv
import json
import os
import time
import requests
# 定义搜索条件
search_terms = "scientific visualization"  # 你感兴趣的关键词
date_from = "2019-07-01"  # 起始日期，格式为 'YYYY-MM-DD'
date_to = "2024-07-22"    # 结束日期，格式为 'YYYY-MM-DD'

# 构建查询字符串，添加时间限制条件
query = f"{search_terms} AND submittedDate:[{date_from} TO {date_to}]"

# 执行搜索
search = arxiv.Search(
    query=query,
    max_results=10  # 限制返回结果数量
)

# 遍历搜索结果
# with open("id-list.txt",'a') as f:
#     for result in search.results():
#     # print(f"Title: {result.title}")
#     # print(f"Authors: {result.authors}")
#     # print(f"Published: {result.published.strftime('%Y-%m-%d')}")  # 格式化日期输出
#     # print(f"Abstract: {result.summary}")
#     # print(f"PDF Link: {result.pdf_url}\n")
#         f.writelines(result.pdf_url)

data=[]
for result in search.results():
    pubtime = result.published.strftime('%Y-%m-%d')
    authors = []
    for i in result.authors:
         authors.append(i.name)
    datum={
        "id":result.get_short_id(),
        "title":result.title,
        "url":result.pdf_url,
        "pubtime":pubtime,
        "authors":authors,
        "abstract":result.summary,

    }
    data.append(datum)
    response = requests.get(result.pdf_url)
    pdf_addr = "./arxivs/"+datum["id"]
    if not os.path.exists(pdf_addr):
            os.makedirs(pdf_addr)
    with open(pdf_addr+"/"+datum["id"]+".json","w") as f:
        json.dump(datum,f,indent = 2)
    # 检查请求是否成功
    if response.status_code == 200:
        # 以二进制写模式打开文件
        with open(pdf_addr+"/"+datum["id"]+".pdf", "wb") as file:
            file.write(response.content)
        print(f"PDF文件已下载: {result.title}.pdf")
    else:
        print(f"下载失败，状态码：{response.status_code}")
with open("arxivs.json",'w') as f:
    json.dump(data,f,indent=2)



