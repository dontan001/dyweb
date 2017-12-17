
import requests
from lxml import etree
import json

# 爬取正在热映的影片及链接
# 爬取更多热门电影
# 爬取电影细节（名称，评价，数据列表）

# step 3
def get_movie_info(id, url):
    html = requests.get(url).text
    sel = etree.HTML(html)
    title = sel.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
    year  = sel.xpath('//*[@id="content"]/h1/span[2]/text()')[0].strip('()')
    movie_info = sel.xpath('string(//*[@id="info"])')
    # print(movie_info)
    movie_info_list = [(item.split(':')[0], item.split(':')[1]) for item in movie_info.split('\n') if item]
    score = sel.xpath('//div[@class="rating_self clearfix"]/strong/text()')
    reviews = ''
    # reviews = get_movie_reviews()
    return title,year,movie_info,movie_info_list, reviews

# step 4
def get_movie_reviews(id):
    url = 'https://movie.douban.com/subject/{0}/reviews'.format(id)
    html = requests.get(url, headers = headers).text
    sel = etree.HTML(html)
    ids = sel.xpath('//div[@class="short-content"]/a/@id')
    id_lists = [id.split('-')[1] for id in ids]

    reply_values = []
    for reply_id in id_lists:
        nurl = 'https://movie.douban.com/j/review/{0}/full'.format(reply_id)
        headers['Referer'] = url
        html = requests.get(nurl, headers=headers).text
        reply_json = json.loads(html)
        # sel = etree.fromstring(reply_json['html'])
        reply_values.append(reply_json['html'])
    return reply_values

# step 1
start_url='https://movie.douban.com'
headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cookie':'bid=Nl42E_jRY_M; ps=y; ue="1009137312@qq.com"; dbcl2="75923736:x/Apl9tb01g"; ck=PyvI; frodotk="291c7dac73e5e4f47b5579055bb1aedc"; _vwo_uuid_v2=52053C1F6F1A9631D3FE4D9D09E75C5D|e5563e1af066f10ae86c0d55b1ec340f; ap=1; __utmt=1; __utma=30149280.650418482.1513498620.1513498620.1513498620.1; __utmb=30149280.2.10.1513498620; __utmc=30149280; __utmz=30149280.1513498620.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utmv=30149280.7592; push_noty_num=0; push_doumail_num=0',
    'Host':'movie.douban.com',
    'Referer':'https://accounts.douban.com/login?alias=1009137312%40qq.com&redir=https%3A%2F%2Fmovie.douban.com%2F&source=movie&error=1013'
}
html = requests.get(url=start_url, headers=headers).text
sel = etree.HTML(html)
ele = sel.xpath('//li[@class="ui-slide-item"]/ul/li[2]/a/@href')[0:37]
for u in ele:
    get_movie_info(u.split('/')[-2],u)

# step 2
# 得到分类标签，然后依次请求
tags_url = 'https://movie.douban.com/j/search_tags?type=movie&source='
# 注意： header中referer已经变化
headers['Referer']='https://movie.douban.com/explore'
tags_html = requests.get(url=tags_url, headers=headers).text
tag_dict = json.loads(tags_html)

for k in tag_dict['tags']:
    page_start=0
    tag_name = k
    while True:
        movie_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag={0}&sort=recommend&page_limit=20&page_start={1}'.format(tag_name, page_start)
        movie_html = requests.get(movie_url).text
        movie_dict = json.loads(movie_html)
        for i in movie_dict['subjects']:
            movie_id = i['id']
            movie_url = i['url']
            get_movie_info(movie_id, movie_url)
        if len(movie_dict['subjects']) != 20:
            break
