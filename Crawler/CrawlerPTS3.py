import datetime
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

PTS_url = 'https://news.pts.org.tw/'
#NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

#  ******************************************************************************
#  * Function: parser web page with url
#  *
#  * Description:
#  *  as title
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  soup: for web parser
#  *
#  ******************************************************************************
def get_soup_with_url_for_web_parser(url):
    #print(url)
    response = requests.get(url)
    if response.status_code != 200:
        print("invaild url:",response.status_code)
        return None
        
    time.sleep(1)#add delay to avoid block  
    soup = BeautifulSoup(response.text, 'html.parser')     

    return soup

#  ******************************************************************************
#  * Function: check_time_with_today_date
#  *
#  * Description:
#  *  This function check_time_with_today_date
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  True:  date is today
#  *  False: date is not today
#  *
#  ******************************************************************************
def check_date_with_today(date,today):
    date = date.replace('年', ' ').replace('月', ' ').replace('日', '')
    date = date.split(' ')
    if int(date[1]) < 10:
        date[1]='0'+ date[1]
    if int(date[2]) < 10:
        date[2]='0'+ date[2]     
    date = date[0] + '-' + date[1] + '-' + date[2]

    if date != today:
        return False

    return True

#  ******************************************************************************
#  * Function: web_garbage_filter
#  *
#  * Description:
#  *  This function filter web garbage
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *   nstr: garbage filtered result
#  *   
#  *
#  ******************************************************************************
def web_garbage_filter(ostr):
    
    # g_list = []

    nstr = ostr 
    #check garbage with g_list
    # for g in g_list: 
    #     idx = nstr.find(g[0]) #find garbage by tag
    #     while idx > 0 :
    #         if g[1] == 0:
    #             nstr = nstr[:idx] # remove tail due to garbage
    #         else :
    #             nstr = nstr[:idx] + nstr[idx+g[1]:] #remove garbage
    #         idx = nstr.find(g[0]) #find garbage by tag

    nstr = " ".join(nstr.split()) #remove /r /n

    return nstr

#  ******************************************************************************
#  * Function: get_post_from_category
#  *
#  * Description:
#  *  This function get content from every news link
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  None
#  *
#  ******************************************************************************
def get_today_new_from_link(new_link,today):
    new = list()
    soup = get_soup_with_url_for_web_parser(new_link)

    new_time = soup.find('div','maintype-wapper').getText()
    new_time = new_time.split('\n')[1]
    if check_date_with_today(new_time, today) == False:
        return new
    
    title = soup.find('h2').getText().rstrip()
    new.append({'TITLE':title})

    content = web_garbage_filter(soup.find('div','article_content').getText())
    new.append({'CONTENT':content})

    #print(new)
    return new

#  ******************************************************************************
#  * Function: check_new_link_available
#  *
#  * Description:
#  *  This function check link is available or not
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  link:  available link
#  *  None:  unavailable link
#  *
#  ******************************************************************************
def check_new_link_available(url):
    
    link = url
    idx = link.find('article')
    if idx < 0:
        return None    
  
    return link

#  ******************************************************************************
#  * Function: get_post_from_category
#  *
#  * Description:
#  *  This function get new post from category of news page
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  None
#  *
#  ******************************************************************************
def get_post_from_category(category_link,today):
    post = list()
    soup = get_soup_with_url_for_web_parser(category_link)

    articles = soup.find_all('div', 'new-wrap new-wrap1 bd-box', 'text-title')
    moreNews = soup.find_all('div', 'news-right-list')
    articles.extend(moreNews)

    for article in articles:
        nlink = check_new_link_available(article.find('a').get('href'))
        #print(nlink)
        if nlink == None:
            continue
        new = get_today_new_from_link(nlink, today)
        if new == []:
            return post

        post.extend(new)

    #print(post)
    return post

#  ******************************************************************************
#  * Function: get_pts_news_from_pages
#  *
#  * Description:
#  *  This function get PTS news from web page
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  None
#  *
#  ******************************************************************************
def get_pts_news_from_pages(url,today):

    articles = [('政經', 'https://news.pts.org.tw/subcategory/9'),  
                ('環境生態', 'https://news.pts.org.tw/subcategory/10'),
                ('全球', 'https://news.pts.org.tw/subcategory/11'),
                ('生活綜合', 'https://news.pts.org.tw/subcategory/12'),                
                ('文教科技', 'https://news.pts.org.tw/subcategory/13'),
                ('社會', 'https://news.pts.org.tw/subcategory/14'),
                # ('Foreign', 'https://news.pts.org.tw/subcategory/35'),
                ] 
           
    posts = list()
    for article in articles:
        category = article[0]
        category_link = article[1]
        post = get_post_from_category(category_link, today) 
        time.sleep(1) #add delay to avoid block
        # posts.append([today,category,category_link])
        posts.append({'CATEGORY': category})
        posts.extend(post)
    
    #print(posts, file=open("posts.txt", "w", encoding='UTF-8'))
    return posts

#  ******************************************************************************
#  * main program entry
#  *
#  * Description:
#  *  main program entry for test
#  *
#  * Parameters: 
#  *  None
#  *
#  * Return value: 
#  *  None
#  *
#  ******************************************************************************
if __name__ == '__main__':
    
    #tStart = time.time()#start_time
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    all_news = get_pts_news_from_pages(PTS_url,today)
    fileName = today + "_pts_news.txt"
    #print(all_news, file=open(fileName, "w", encoding='UTF-8'))
    thefile = open(fileName, 'w', encoding='utf-8')
    for item in all_news:
        thefile.write("%s\n" % item)

    #tEnd = time.time()#end_time
    #print("It cost %f sec" %(tEnd - tStart))
