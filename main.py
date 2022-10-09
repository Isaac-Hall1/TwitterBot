from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tweepy
import datetime
from dotenv import load_dotenv

load_dotenv()

consumer_key = 'consumer_key'

consumer_secret = 'consumer_secret'

access_token = 'access_token'

access_token_secret = 'access_token_secret'
def OAuth():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    except:
        return None

oauth = OAuth()
api = tweepy.API(oauth)


my_listNames = [[],[],[],[]]
popStreamers = []
def Streamers() -> list:
    url = "https://www.twitch.tv/directory/all?sort=VIEWER_COUNT"
    options = Options()
    options.headless = True
    s = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options = options)
    driver.get(url)
    count = 3
    for i in range(2,5):
        timein = 1
        Name = WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div[{i}]/div/div/div/article/div[1]/div/div[1]/div[1]/a/p'))).text
        Views = WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div[{i}]/div/div/div/article/div[2]/div[5]/a/div/div[3]/div'))).text
        if len(Views) > 13:
            Views = Views[0:5]
        elif len(Views) == 13:
            Views = Views[0:4]
        elif len(Views) == 12:
            Views = Views[0:3]
        else:
            Views = Views[0:2]
        if Name in my_listNames[0]:
            tindex = my_listNames[0].index(Name)
            my_listNames[1][tindex] += count
            try:
                my_listNames[2][tindex] = ((my_listNames[2][tindex] + float(Views)) / 2)
            except:
                print("error")
            my_listNames[3][tindex] += 1
        else:
            my_listNames[0].append(Name)
            my_listNames[1].append(count)
            my_listNames[2].append(float(Views))
            my_listNames[3].append(timein)
            
        count -= 1
    driver.quit()
    return my_listNames
def popStreamer():
    #determines most popular streamer based off of points, I could use a for loop to make this easier but I dont feel like it
    popStreamers.clear()
    maxnum = max(my_listNames[1])
    index = my_listNames[1].index(maxnum)
    del my_listNames[1][index]
    my_listNames[1].insert(index , 0)
    maxnum2 = max(my_listNames[1])
    index2 = my_listNames[1].index(maxnum2)
    del my_listNames[1][index]
    my_listNames[1].insert(index, maxnum)
    if maxnum == maxnum2:
        if my_listNames[2][index] > my_listNames[2][index2]:
            index = index
        else:
            index = index2
    popStreamers.append(my_listNames[0][index])
    popStreamers.append(my_listNames[2][index])
    popStreamers.append(my_listNames[3][index])
    del my_listNames[1][index]
    my_listNames[1].insert(index , 0)
    return popStreamers


while True:
    my_listNames = [[],[],[],[]]
    popStreamers = []
    while True:
        now = datetime.datetime.now()
        print(now.strftime('%H:%M:%S'))
        if now.strftime('%H:%M:%S') >= '05:50:00' and now.strftime('%H:%M:%S') <= '05:59:59':
            break
        Streamers()
        now = datetime.datetime.now()
        print(my_listNames)
        time.sleep(300)
        now = datetime.datetime.now()
        
        
        

    while True:
        
        now = datetime.datetime.now()
        time.sleep(.1)
        if now.strftime("%H:%M:%S") == '06:00:00':

            api.update_status('Todays Data set was based off of: ' + str(datetime.date.today() - datetime.timedelta(days=1)))
            my_list = []
            for i in range(3):
                popStreamer()
                dude = popStreamers[2] / 12
                if len(str(dude)) > 4:
                    my_list.append("Streamer Name: " + popStreamers[0] + '\n' + "Average Views in Top 3: " + str(popStreamers[1])[0:6] + "K Viewers" + '\n' + "Uptime in Top 3: " + str(dude)[0:4] + " Hours" + '\n' + 'Link: '+ f'https://www.twitch.tv/{popStreamers[0]}' +"\n" + "#twitch #streamer" + '\n')
                else:
                    my_list.append("Streamer Name: " + popStreamers[0] + '\n' + "Average Views in Top 3: " + str(popStreamers[1])[0:6] + "K Viewers" + '\n' + "Uptime in Top 3: " + str(dude) + " Hours"  + "\n" + 'Link: '+ f'https://www.twitch.tv/{popStreamers[0]}' + '\n' + "#twitch #streamer" + '\n')
                s = '\n'
                s = s.join(my_list)
                print(s)
                try:
                    api.update_status(str(i + 1) + '\n' + s)
                except:
                    api.update_status("Streamer Name: " + popStreamers[0] + '\n' + "Average Views in Top 3: " + str(popStreamers[1])[0:6] + "K Viewers" + '\n' + "Uptime in Top 3: " + str(dude) + " Hours"  + "\n" + 'Link: '+ f'https://www.twitch.tv/{popStreamers[0]}' + '\n')
                my_list.clear()  
            break

       


