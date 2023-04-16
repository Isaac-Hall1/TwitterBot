from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tweepy
import datetime
import heapq
import random
from dotenv import load_dotenv

load_dotenv()

consumer_key = 'ReamiuPpfGUeLWdVgAFBcOiAy'

consumer_secret = 'SBG0IsoimcMcWU9ba59J2L1mN3DUwWhKWnTX9naiZJPiWo5P1N'

access_token = '1539834620639956992-qzET7o3aTHrC6qWrriey0iiq7Nb9Lp'

access_token_secret = 'nbTtjYaTn21aceZV009SGCToPGHiFejwcqW1AvXllIYtN'
def OAuth():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    except:
        return None

oauth = OAuth()
api = tweepy.API(oauth)
class streamerInfo():
    score = 0
    name = ""
    views = 0.0
    time = 0
    def __init__(self, name, views, time):
        self.name = name
        self.views = views
        self.time = time
    def addTime(self, addTime: int):
        self.time += addTime
    def addViews(self,viewNumber: float):
        self.views = float(self.views) + viewNumber / 2
    def getName(self):
        return self.name
    def getViews(self):
        return -float(self.views)
    def getTime(self):
        return self.time


popStreamers = []
backingArray = []
nodupes = dict()
def Streamers():
    url = "https://www.twitch.tv/directory/all?sort=VIEWER_COUNT"
    options = Options()
    options.headless = True
    s = Service('/Users/isaac/Documents/drivers/chromedriver')
    driver = webdriver.Chrome(service=s, options = options)
    driver.get(url)
    size = 0
    time = 1
    for i in range(2,5):
        Name = WebDriverWait(driver,70).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div[{i}]/div/div/div/article/div[1]/div/div[1]/div[1]/a/p'))).text
        Views = WebDriverWait(driver,70).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="browse-root-main-content"]/div[4]/div/div[1]/div[{i}]/div/div/div/article/div[2]/div[5]/a/div/div[3]/div'))).text
        if len(Views) > 13:
            Views = Views[0:5]
        elif len(Views) == 13:
            Views = Views[0:4]
        elif len(Views) == 12:
            Views = Views[0:3]
        else:
            Views = Views[0:2]
        # if a streamer has already been recorded, just adds to that streamers value's
        if Name in nodupes.keys():
            for i in range(size):
                if(backingArray[i].getName() == Name):
                    backingArray[i].addViews(Views)
                    backingArray[i].addTime(time)
                    return
        else:
            # creates a new streamer and builds the heap
            counter = random.randrange(100000)
            streamer = streamerInfo(Name, Views, time)
            nodupes[Name] = streamer
            heapq.heappush(backingArray,(streamer.getViews(),counter,streamer))
            print(nodupes)
            size += 1
            
    driver.quit()
    return
def popStreamer():
    #determines most popular streamer based off of points, I could use a for loop to make this easier but I dont feel like it
    popStreamers.clear()
    for i in range(3):
        popStreamers.append(heapq.heappop(backingArray)[1])
    return popStreamers

    


while True:
    popStreamers = []
    while True:
        now = datetime.datetime.now()
        print(now.strftime('%H:%M:%S'))
        if now.strftime('%H:%M:%S') >= '05:50:00' and now.strftime('%H:%M:%S') <= '05:59:59':
            break
        Streamers()
        now = datetime.datetime.now()
        print(backingArray)
        time.sleep(10)
        now = datetime.datetime.now()
        
        
        

    while True:
        now = datetime.datetime.now()
        time.sleep(.1)
        if now.strftime("%H:%M:%S") == '06:00:00':
            api.update_status('Todays Data set was based off of: ' + str(datetime.date.today() - datetime.timedelta(days=1)))
            my_list = []
            popStreamer()
            for i in range(3):
                time =  popStreamers[i].getTime() / 12
                # makes view counts look better, sometimes the floats get rlly long
                if len(str(time)) > 4:
                    my_list.append("Streamer Name: " + popStreamers[i].getName() + '\n' + "Average Views in Top 3: " + str(popStreamers[1].getViews())[0:6] + "K Viewers" + '\n' + "Uptime in Top 3: " + str(time)[0:4] + " Hours" + '\n' + 'Link: '+ f'https://www.twitch.tv/{popStreamers[0].getName()}' +"\n" + "#twitch #streamer" + '\n')
                else:
                    my_list.append("Streamer Name: " + popStreamers[i].getName() + '\n' + "Average Views in Top 3: " + str(popStreamers[1].getViews())[0:6] + "K Viewers" + '\n' + "Uptime in Top 3: " + str(time) + " Hours"  + "\n" + 'Link: '+ f'https://www.twitch.tv/{popStreamers[0].getName()}' + '\n' + "#twitch #streamer" + '\n')
                # organizes tweet into a readable format
                s = '\n'
                s = s.join(my_list)
                print(s)
                try:
                    api.update_status(str(i + 1) + '\n' + s)
                except:
                    api.update_status("Streamer Name: " + popStreamers[0] + '\n' + "Average Views in Top 3: " + str(popStreamers[1])[0:6] + "K Viewers" + '\n' + "Uptime in Top 3: " + str(time) + " Hours"  + "\n" + 'Link: '+ f'https://www.twitch.tv/{popStreamers[0]}' + '\n')
            my_list.clear()  
            break

       


