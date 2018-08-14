import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
        print(r.text)
    except:
        return ""

def getStockList(lst, stockURL):
    """
    从东方财富网获取个股信息：股票代码
    http://quote.eastmoney.com/stocklist.html
    """
    """
    研究网页的特点发现，我们想要的信息都存储在a标签中
    """
    html = getHTMLText(stockURL)  # 获取一个页面的文本信息
    soup = BeautifulSoup(html, 'html.parser')  #使用BS4库 解析页面
    a = soup.find_all('a')  # 使用find_all方法，找到所有的a标签
    """
    对a标签进行遍历
    根据股票代码的特点，可以使用正则表达式来获取
    上海的由sh开头，深圳的由sz开头,由六位数组成，
    在链接中寻找这类型的正则表达式，
    中间过程可能出现各种异常
    通过正则表达式获取股票代码信息
    """
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue

    return ""

def getStockInfo(lst, stockURL, fpath):
    """
    从百度股票获取个股信息
    获取股票的列表
    根据股票列表，到相关网站获取价格存储url中
    文件保存路径
    在百度中查看网页源代码，查看价格，
    首先向每个个股信息发起请求
    """
    for stock in lst:
        url = stockURL + stock + ".html"  # 形成访问个股页面的url
        html = getHTMLText(url)
        """
        解析过程可能出现异常
        """
        try:
            if html == "":
                continue
            infoDict = {}  # 记录返回所有的个股信息
            # 然后用BeautifulSoup库解析网页类型
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})  # 解析发现，股票信息都保存在div标签下

            name = stockInfo.find_all(attrs={'class': "bets-name"})[0]
            infoDict.update({'股票名称': name.text.split()[0]})  # 使用split获得股票对应的完整名称

            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val  # 直接赋值给字典

            # with open(fpath,'a',encoding='utf-8') as f:
            with open(fpath,'a') as f:
                f.write(str(infoDict) + '\n')
        except:
            traceback.print_exc()  # 获得错误信息
            continue
    return ""

def main():
    """
    获取股票信息的主体部分
    输出的文件保存在D盘根目录下
    """
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock'
    output_file = 'D:/BaiduStockInfo.txt'
    slist = []
    getStockList(slist, stock_list_url) #获取股票代码
    getStockInfo(slist, stock_info_url, output_file)

main()
# 通过main方法使得整个程序运行
