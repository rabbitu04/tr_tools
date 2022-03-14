import requests
import traceback

from datetime import datetime, date, timedelta
from pymongo import MongoClient
from random import randint, sample
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

# DB
mongo = MongoClient('mongodb://localhost:27017')
db = mongo['travian']

player_ids = [player['player_id'] for player in db.players.find()]

# time
now = datetime.now()
date = str(now.date())
date_8_before = str((now - timedelta(days=8)).date())
hour = now.hour

sleep(randint(0, 600))

# selenium
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome = webdriver.Chrome('/root/tr-tools/crawler/chromedriver', options=chrome_options)

def check_cmp():
    try:
        cmp_btn = chrome.find_element_by_class_name('cmpboxbtnyes')
        cmp_btn.click()
        sleep(5)
        return True
    except:
        return False


def check_continue():
    try:
        continue_btn = chrome.find_element_by_link_text('» continue')
        continue_btn.click()
        sleep(5)
        return True
    except:
        return False


def login():
    for i in range(3):
        try:
            print('test login', i)
            sleep(1)
            chrome.get('https://ttq.x2.europe.travian.com/login.php')
        except:
            pass
        else:
            break

    name = chrome.find_element_by_name('name')
    password = chrome.find_element_by_name('password')
    submit = chrome.find_element_by_name('s1')
    
    #####
    name.send_keys()
    password.send_keys()
    #####
    check_cmp()
    submit.click()


def crawl(player_id):

    print('crawling data of player', player_id)

    chrome.get('https://ttq.x2.europe.travian.com/profile/' + str(player_id))
    if check_cmp() or check_continue():
        chrome.get('https://ttq.x2.europe.travian.com/profile/' + str(player_id))
    
    sleep(1)

    player_name = chrome.find_element_by_class_name('titleInHeader').text
    if player_name == 'Nothing here!':
        print('player "' + str(player_id) +'" NOT EXISTS!!!')
        db.players.delete_one({'player_id': player_id})
        return

    # get basic data
    alliance = chrome.find_element_by_xpath('//table[@id="details"]/tbody/tr[2]/td').text
    db.player_basic_data.insert_one({
        'player_id': player_id,
        'name': player_name,
        'alliance': alliance,
        'date': date,
        'hour': hour,
    })

    # get inhabitants of each village
    coordinates = chrome.find_elements_by_class_name('coords')
    inhabitants = chrome.find_elements_by_class_name('inhabitants')

    for i in range(len(coordinates)):
        db.inhabitants_record.insert_one({
            'player_id': player_id,
            'date': date,
            'hour': hour,
            'coordinate': str(coordinates[i].text),
            'inhabitant': int(str(inhabitants[i].text)),
        })
    # get off/def/exp
    data = chrome.find_elements_by_class_name('greyInfo')
    db.off_point.insert_one({
        'player_id': player_id,
        'point': int(data[1].text.split(' ')[0][1:]),
        'date': date,
        'hour': hour,
    })
    db.def_point.insert_one({
        'player_id': player_id,
        'point': int(data[2].text.split(' ')[0][1:]),
        'date': date,
        'hour': hour,
    })
    db.exp.insert_one({
        'player_id': player_id,
        'exp': int(data[3].text.split(' ')[0][1:]),
        'date': date,
        'hour': hour,
    })

    return


try:
    print('-' * 10, str(date), str(hour), '-' * 10)

    login()

    for id in sample(player_ids, len(player_ids)):
        crawl(id)

    # delete data 7 days before
    db.inhabitants_record.delete_many({
        'date': date_8_before,
        'hour': hour,
    })
    db.player_basic_data.delete_many({
        'date': date_8_before,
        'hour': hour,
    })
    db.off_point.delete_many({
        'date': date_8_before,
        'hour': hour,
    })
    db.def_point.delete_many({
        'date': date_8_before,
        'hour': hour,
    })
    db.exp.delete_many({
        'date': date_8_before,
        'hour': hour,
    })

except Exception as e:
    print('ERROR at', now, ':', e)
    traceback.print_exc()

finally:
    chrome.quit()
    print()
