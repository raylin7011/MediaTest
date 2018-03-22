import datetime
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

LTN_url = 'http://news.ltn.com.tw/list/breakingnews/'
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
    
    g_list = [#('googletag', 85 ), #garbage tag, garbage len
              ('var disable_onead_inread', 1121 ),
              ("(function", 390),
              ("$(\'.text", 0),
              ("if(!(gdt >=", 0),
             ]

    nstr = ostr 
    #check garbage with g_list
    for g in g_list: 
        idx = nstr.find(g[0]) #find garbage by tag
        while idx > 0 :
            if g[1] == 0:
                nstr = nstr[:idx] # remove tail due to garbage
            else :
                nstr = nstr[:idx] + nstr[idx+g[1]:] #remove garbage
            idx = nstr.find(g[0]) #find garbage by tag

    nstr = " ".join(nstr.split()) #remove /r /n

    return nstr

#  ******************************************************************************
#  * Function: get_entertainment_new_from_link
#  *
#  * Description:
#  *  This function get content from entertainment news link
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  None
#  *
#  ******************************************************************************
def get_entertainment_new_from_link(new_link,today):
    new = list()
    soup = get_soup_with_url_for_web_parser(new_link)
    
    new_time = soup.find('div','date').getText().rstrip()
    new_time = new_time.replace('/', '-').split(' ')[0]
    if check_date_with_today(new_time, today) == False:
        return new

    content = web_garbage_filter(soup.find('div','news_content').getText())
    new.append({'CONTENT':content})

    #print(new)
    return new

#  ******************************************************************************
#  * Function: get_sport_new_from_link
#  *
#  * Description:
#  *  This function get content from sport news link
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  None
#  *
#  ******************************************************************************
def get_sport_new_from_link(new_link,today):
    new = list()
    soup = get_soup_with_url_for_web_parser(new_link)
    
    new_time = soup.find('div','c_time').getText().rstrip()
    new_time = new_time.replace('/', '-').split(' ')[0]
    if check_date_with_today(new_time, today) == False:
        return new

    content = web_garbage_filter(soup.find('div','news_p').getText())
    new.append({'CONTENT':content})

    #print(new)
    return new

#  ******************************************************************************
#  * Function: get_general_new_from_link
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
def get_general_new_from_link(new_link,today):
    new = list()
    soup = get_soup_with_url_for_web_parser(new_link)
    
    new_time = soup.find('div','text').find('span').getText().rstrip()
    new_time = new_time.split(' ')[0]
    if check_date_with_today(new_time, today) == False:
        return new

    content = web_garbage_filter(soup.find('div','text').getText())
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
    idx = link.find('breakingnews')
    if idx < 0:
        idx = link.find('newspapers')
        if idx < 0:
            return None

    link =  LTN_url + link[idx:]    
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
def get_post_from_category(category_link, today):
    post = list()
    tmp_link = category_link
    for i in range(1,3):
        if i != 1:
            tmp_link = category_link + str(i)

        soup = get_soup_with_url_for_web_parser(tmp_link)         

        articles = soup.find_all('a', 'tit')

        for article in articles:
            nlink = article.get('href')
            # if nlink == None:
            #     continue
            if category_link.find('sport') > 0 :
                new = get_sport_new_from_link(nlink,today)
            elif category_link.find('entertain') > 0 :
                new = get_entertainment_new_from_link(nlink,today)
            else:
                new = get_general_new_from_link(nlink,today)

            if new == []:
                return post

            title = article.find('p').getText().strip()
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
def get_ltn_news_from_pages(url,today):

    articles = [('政治', 'http://news.ltn.com.tw/list/breakingnews/politics/'),  
                ('生活', 'http://news.ltn.com.tw/list/breakingnews/life/'),
                ('社會', 'http://news.ltn.com.tw/list/breakingnews/society/'),
                ('國際', 'http://news.ltn.com.tw/list/breakingnews/world/'),
                ('財經', 'http://news.ltn.com.tw/list/breakingnews/business/'),
                ('娛樂', 'http://news.ltn.com.tw/list/breakingnews/entertainment/'),
                ('體育', 'http://news.ltn.com.tw/list/breakingnews/sports/'),
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
    
    tStart = time.time()#start_time
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    all_news = get_ltn_news_from_pages(LTN_url,today)
    fileName = today + "_ltn_news.txt"
    #print(all_news, file=open(fileName, "w", encoding='UTF-8'))
    thefile = open(fileName, 'w', encoding='utf-8')
    for item in all_news:
        thefile.write("%s\n" % item)

    #tEnd = time.time()#end_time
    #print("It cost %f sec" %(tEnd - tStart))
