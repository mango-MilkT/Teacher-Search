import requests
import re
import os
from lxml import etree

kws = ['optic']
dirname = ''
for kw in kws:
    dirname = dirname + kw + '+'
dirname = dirname[:-1]
dirpath = './teacherLib/' + dirname
if not os.path.exists('./teacherLib'):
    os.mkdir('./teacherLib')
if not os.path.exists(dirpath):
    os.mkdir(dirpath)
url = 'https://www.eee.hku.hk/people/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}
params = {}
if not os.path.exists('./teacher.html'):
    page_text = requests.get(url=url,headers=headers).text
    file_name = 'teacher.html'
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(page_text)
parser = etree.HTMLParser(encoding="utf-8")
selector = etree.parse('teacher.html',parser=parser)

pattern = re.compile('people/(.*)/')
cnt = 0
for i in range(1,57):
    r1 = selector.xpath('//*[@id="filter-container-people"]/figure[%d]/a/@href'%i)[0]
    name = re.search(pattern, r1).group(1)
    page_text = requests.get(url=r1,headers=headers).text
    second_selector = etree.HTML(page_text)
    r2 = second_selector.xpath('//*[@id="project-box"]/div[2]/div//text()')
    str = ''
    for txt in r2:
        str = str + txt
    for kw in kws:
        if (kw in str):
            print('I found one!')
            cnt = cnt + 1
            file_name = dirpath + '/' + name + '.html'
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(page_text) 
        continue
print('Download complete. Found %d teachers.'%cnt)
