from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.by import By

#активация с STRAVA
def user_strava(email, password_l, executable_path):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options, executable_path=executable_path)
    browser.get('https://www.strava.com/login')
    time.sleep(2)
    login = browser.find_element_by_xpath('//*[@id="email"]')
    login.click()
    login.send_keys(email)
    password = browser.find_element_by_xpath('//*[@id="password"]')
    password.click()
    password.send_keys(password_l)
    go = browser.find_element_by_xpath('//*[@id="login-button"]')
    go.click()
    time.sleep(5)
    user_info = browser.find_element_by_xpath('//*[@id="athlete-profile"]')
    id = user_info.get_attribute('innerHTML').split('/athletes/')[1].split('"')[0]
    name = user_info.get_attribute('innerHTML').split('athlete-name">')[1].split('</div')[0]
    count_followers = user_info.get_attribute('innerHTML').split('Подписчики')[1].split('-text">')[1].split('</b')[0]
    count_followings = user_info.get_attribute('innerHTML').split('Подписки')[1].split('-text">')[1].split('</b')[0]
    count_trains = user_info.get_attribute('innerHTML').split('Тренировки')[1].split('-text">')[1].split('</b')[0]
    browser.quit()
    return {'id':id, 'name':name, 'count_followers':count_followers, 'count_followings':count_followings, 'count_trains':count_trains}

#Анализ своих KPI
def user_strava_feature(email, password_l, executable_path):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(executable_path=executable_path)
    browser.get('https://www.strava.com/login')
    time.sleep(2)
    login = browser.find_element_by_xpath('//*[@id="email"]')
    login.click()
    login.send_keys(email)
    password = browser.find_element_by_xpath('//*[@id="password"]')
    password.click()
    password.send_keys(password_l)
    go = browser.find_element_by_xpath('//*[@id="login-button"]')
    go.click()
    time.sleep(5)
    user_info = browser.find_element_by_xpath('//*[@id="athlete-profile"]')
    avatar = user_info.get_attribute('innerHTML').split('class="avatar-img" src="')[1].split('">')[0]
    id = user_info.get_attribute('innerHTML').split('/athletes/')[1].split('"')[0]
    name = user_info.get_attribute('innerHTML').split('athlete-name">')[1].split('</div')[0]
    count_followers = user_info.get_attribute('innerHTML').split('Подписчики')[1].split('-text">')[1].split('</b')[0]
    count_followings = user_info.get_attribute('innerHTML').split('Подписки')[1].split('-text">')[1].split('</b')[0]
    count_trains = user_info.get_attribute('innerHTML').split('Тренировки')[1].split('-text">')[1].split('</b')[0]
    last_train = user_info.get_attribute('innerHTML').split('Последняя тренировка')[1].split('<time class="timestamp" datetime="')[1].split(' UTC"')[0]
    browser.quit()
    return {'avatar':avatar, 'id':id, 'name':name, 'count_followers':count_followers, 
            'count_followings':count_followings, 'count_trains':count_trains, 'last_train':last_train
            }
#Сбор записей из ленты активности
def news_scroll (email, password_l, executable_path, num):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options, executable_path=executable_path)
    browser.get('https://www.strava.com/login')
    time.sleep(2)
    login = browser.find_element_by_xpath('//*[@id="email"]')
    login.click()
    login.send_keys(email)
    password = browser.find_element_by_xpath('//*[@id="password"]')
    password.click()
    password.send_keys(password_l)
    go = browser.find_element_by_xpath('//*[@id="login-button"]')
    go.click()
    time.sleep(5)
    browser.get('https://www.strava.com/dashboard/following/'+str(num))
    time.sleep(2)
    #news = browser.find_element_by_xpath('//*[@id="dashboard-feed"]')
    list_news = []
    i = 3
    while i<num:
        try:
            list_news.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[1]/div['+str(i)+']').get_attribute('innerHTML'))
            # if browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[1]/div['+str(i)+']/div[3]/div[1]/div[2]').get_attribute('innerHTML').find('Показать все зачеты')==-1:
                # browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[1]/div['+str(i)+']/div[3]/div[1]/div[2]/button[1]').click()
                # #print (browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[1]/div['+str(i)+']/div[3]/div[1]/div[2]/button[1]').get_attribute('innerHTML'))
            i = i+1
        except:
            #list_news.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[1]/div['+str(i)+']/div[4]/div[1]/div[2]').get_attribute('innerHTML'))
            i = i+1
    return list_news