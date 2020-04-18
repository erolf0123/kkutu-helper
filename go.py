import sqlite3,time,re,collections
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
kuutu_db = sqlite3.connect("kkutu.db")
cur = kuutu_db.cursor()
driver = webdriver.Chrome('/Users/erolf0123/Desktop/web/KKUTU-HELPER/chromedriver')
driver.get('https://kkutu.co.kr/login?before=https://kkutu.co.kr')

def input_db():
    r = open('db_end.txt', mode = 'r')
    for line in r:
        check = 0
        a = line.strip()
        row = cur.execute("select * from test where word = '"+str(a)+"'")
        for i in row:
            check = 1
            break
        if check == 0:
            cur.execute("insert into test values('"+str(a)+"','"+str(len(a))+"','0')")
            kuutu_db.commit()
    r.close()
    exit()

while 1:
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    word = soup.find_all('div','ellipse history-item expl-mother')
    if len(word) > 0:
        for div in soup.find_all("div",{'class':'history-mean'}):
            div.decompose()
        for div in soup.find_all("label",{'class':"history-class"}):
            div.decompose()
        for div in soup.find_all("div",{'class':'expl'}):
            div.decompose()
        for div in soup.find_all("label",{'class':'word-m3-body'}):
            div.decompose()
        word = soup.find_all('div','ellipse history-item expl-mother')
        word = word[0].text
        check = 0
        row = cur.execute("select * from test where word = '"+str(word)+"'")
        for i in row:
            cur.execute("update test set use = 1 where word = '"+str(word)+"'")
            check = 1
            break
        if check == 0:
            cur.execute("insert into test values('"+str(word)+"','"+str(len(word))+"','1')")
            kuutu_db.commit()
            print(word +" 단어가 database에 저장되었습니다.")

    soup2 = BeautifulSoup(driver.page_source, 'lxml')
    soup_turn = soup2.find_all('div','game-input')
    while str(soup_turn).find('block') >= 0:
        word = soup.select('#GameBox > div > div.game-head > div.jjoriping > div > div.jjo-display.ellipse')
        word = word[0].text
        word = word.replace(")", "")
        word = word.replace("(", "")
        print(word)
        kkk = cur.execute("SELECT * FROM test WHERE use=0 AND word LIKE '" + word[-1] + "%' ORDER BY leng DESC LIMIT 1") #cgiosy 
        for kk in kkk:
            driver.find_element_by_xpath('/html/body/div[3]/div[32]/div/input').send_keys(kk[0])
            cur.execute("update test set use = 1 where word ='"+kk[0]+"'")
            kuutu_db.commit()
            driver.find_element_by_xpath('/html/body/div[3]/div[32]/div/button').click()
            break
        time.sleep(0.15)
        soup2 = BeautifulSoup(driver.page_source, 'lxml')
        soup_turn = soup2.find_all('div','game-input')
    if len(word) == 0:
        cur.execute("update test set use = 0 where use = 1")
        kuutu_db.commit()
kuutu_db.close()