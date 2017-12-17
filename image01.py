# from selenium import webdriver
# driver=webdriver.Chrome(executable_path=r'D:\Driver\chromedriver.exe') # 载入浏览器
# # 文件下载
# driver.get('https://image.baidu.com/')
# driver.find_element_by_id('kw').send_keys('洞庭湖')
# driver.find_element_by_class_name('s_btn').click()
# # 1.找到img节点
# element=driver.find_elements_by_xpath('//')
# # 2.模拟滚轮操作
# # 3.进行下载
# # 4.修改下载地址
import requests  #请求网页的模块
import json      #解析json模块
import time      #时间模块
import urllib.request as rq  #另外一个请求网页数据模块
# 1.让用户输入关键词
#word=input('请输入要下载的图片的关键词：')
word='长腿美女'
pn=10  #初始化pn变量
# 2.执行死循环
while True:
    #（1）拼接请求地址链接，加入用户输入的关键词以及开始的索引下标
    # ajax call， 30 pictures per page
    url='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={0}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={0}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn={1}&rn=30&gsm=5a&1513478876621='.format(word,pn)
    print(url)
    # （2）请求链接，得到网页源代码
    html=requests.get(url).text # 请求得到网页的源代码
    # （3）解析返回json字符串
    img_dict=json.loads(html) #对于源代码进行json的解析（原因html是一个json格式的字符串）（json解析的结果为一个字典）
    # 解析得到图片url，执行下载操作
    # （4）遍历字典中的data属性，从而得到每一个图片的信息
    for item in img_dict['data']:
        try:
            # (5)取出图片的网页路径
            # 得到每一个item元素的图片路径
            if 'replaceUrl' in item and item['replaceUrl']:
                middleURL = item['middleURL']
            elif 'hoverURL' in item and item['hoverURL']:
                middleURL = item['hoverURL']
            else:
                break
            # （6）设置本地存储的路径
            filename='images/'+word+'_'+str(time.time())+'.jpg'
            # 执行下载
            # url      网页文件的路径
            # filename 保存到你的电脑里的文件名（完整的路径）
            # （7）执行下载
            rq.urlretrieve(middleURL,filename)
        except Exception as ex:
            print(item)
    # 判断机制，判断pn是否小于displayNum
    # 如果小于正常执行，如果大于，则跳出循环
    # 101810
    # pn=101790+30->101820
    # 3.判断pn是否超过了数据的总条数，如果超过则跳出循环
    if pn>100:
        break
    else:
        pn = pn + 30
        time.sleep(10)
