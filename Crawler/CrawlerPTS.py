import csv
import time
import datetime
import urllib.parse
import requests
from bs4 import BeautifulSoup

PTS_url = 'https://news.pts.org.tw/'
#NOT_EXIST = BeautifulSoup('<a>?¬æ?å·²è¢«?ªé™¤</a>', 'lxml').a

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
    time.sleep(1)#add delay to avoid block  
    soup = BeautifulSoup(response.text, 'html.parser')     

    return soup

#  ******************************************************************************
#  * Function: get_post_from_category
#  *
#  * Description:
#  *  This function get content with every news line
#  *
#  * Parameters: 
#  *
#  *
#  * Return value: 
#  *  None
#  *
#  ******************************************************************************
def get_new_from_link(new_link):
    new = list()
    soup = get_soup_with_url_for_web_parser(new_link)    
    new.append({
        soup.find('div','list-news-time').getText(),
        soup.find('div','article-content').getText().rstrip(),
        new_link,    
    })
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
def get_post_from_category(category_link):
    post = list()
    soup = get_soup_with_url_for_web_parser(category_link)  
    articles = soup.find_all('h2', 'list-news-title')    
    for article in articles:
        tmp = article.find('a')
        new = get_new_from_link(tmp.get('href'))            
        post.append(tmp.getText().strip())
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
def get_pts_news_from_pages(url):
    soup = get_soup_with_url_for_web_parser(PTS_url) 
    articles = soup.find_all('li', 'category-item')
    #print(articles, file=open("articles.txt", "w", encoding='UTF-8'))
    posts = list()
    for article in articles:
        tmp = article.find('a')
        post = get_post_from_category(tmp.get('href')) 
        time.sleep(3)#add delay to avoid block
        posts.append({
            tmp.getText().strip(),
            tmp.get('href'),
        })
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
    #today = datetime.datetime.now().strftime("%Y-%m-%d")
    all_news = get_pts_news_from_pages(PTS_url)
    print(all_news, file=open("all_news.txt", "w", encoding='UTF-8'))
    #tEnd = time.time()#end_time
    #print("It cost %f sec" %(tEnd - tStart))
