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
    
    # g_list = [('googletag', 85 ), #garbage tag, garbage len
    #           ('(function', 775 ),
    #          ]

    nstr = ostr 
    #check garbage with g_list
    # for g in g_list: 
    #     idx = nstr.find(g[0]) #find garbage by tag
    #     while idx > 0 :
    #         nstr = nstr[:idx] + nstr[idx+g[1]:] #remove garbage
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
    new_time = soup.find('div','list-news-time').getText()
    if check_date_with_today(new_time, today) == False:
        return new

    content = web_garbage_filter(soup.find('div','article-content').getText())
    new.append({'CONTENT':content})

    #print(new)
    return new

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
    if check_date_with_today(soup.find('div','list-news-time').getText(), today) == False:
        return post

    articles = soup.find_all('h2', 'list-news-title')    
    for article in articles:
        tmp = article.find('a')
        new = get_today_new_from_link(tmp.get('href'),today)
        if new == []:
            return post

        title = tmp.getText().strip() 
        post.append({'TITLE':title})
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
    
    soup = get_soup_with_url_for_web_parser(PTS_url) 
    articles = soup.find_all('li', 'category-item')
    #print(articles, file=open("articles.txt", "w", encoding='UTF-8'))
    posts = list()
    for article in articles:
        tmp = article.find('a')
        category = tmp.getText().strip()
        category_link = tmp.get('href')
        post = get_post_from_category(category_link, today) 
        time.sleep(1) #add delay to avoid block
        posts.append({'CATEGORY': category})
        if post != []:
            posts.extend(post)
    
    #print(posts, file=open("posts.txt", "w", encoding='UTF-8'))
    return posts

#  ******************************************************************************
#  * main program entry
#  *
#  * Description:
#  *  main program entry
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
