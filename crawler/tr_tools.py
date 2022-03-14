import sys
from random import choice
from selenium.webdriver import Chrome
from time import sleep


class TravianTool(object):
    chrome = Chrome('./chromedriver')

    url_login                   = 'https://finals.travian.com/login.php'
    url_target_alliance_members = 'https://finals.travian.com/alliance/%s/profile?st=members'
    url_sending_troop           = 'https://finals.travian.com/build.php?newdid=%s&id=39&tt=2&gid=16'
    
    def __init__(self, name, password, village_newdid, scout_id='t4', target_alliance_id='0'): 
        self.name               = name
        self.password           = password
        self.village_newdid     = village_newdid
        self.scout_id           = scout_id
        self.target_alliance_id = target_alliance_id
        
        self.url_target_alliance_members = self.url_target_alliance_members % target_alliance_id
        self.url_sending_troop           = self.url_sending_troop % village_newdid
    
    def finish(self):
        self.chrome.quit()
        
    def check_using_cookie(self):
        class_name = 'cmpboxbtnyes'
        try:
            btn = self.chrome.find_element_by_class_name(class_name)
            btn.click()
        except:
            pass

    def login(self):
        self.chrome.get(self.url_login)
        sleep(3)
        self.check_using_cookie()
        name = self.chrome.find_element_by_name('name')
        name.send_keys(self.name)
        password = self.chrome.find_element_by_name('password')
        password.send_keys(self.password)
        submit = self.chrome.find_element_by_id('s1')
        submit.click()
    
    def send_troops(self, x=0, y=0, t1=0, t2=0, t3=0, t4=0, t5=0, t6=0, t7=0, t8=0, t9=0, t10=0, t11=0, sending_case=2):
        # sending case: 2=支援 / 3=攻擊 / 4=搶奪
        self.chrome.get(self.url_sending_troop)
        if t1:
            input_t1 = self.chrome.find_element_by_name('troops[0][t1]')
            input_t1.send_keys(t1)
        if t2:
            input_t2 = self.chrome.find_element_by_name('troops[0][t2]')
            input_t2.send_keys(t2)
        if t3:
            input_t3 = self.chrome.find_element_by_name('troops[0][t3]')
            input_t3.send_keys(t3)
        if t4:
            input_t4 = self.chrome.find_element_by_name('troops[0][t4]')
            input_t4.send_keys(t4)
        if t5:
            input_t5 = self.chrome.find_element_by_name('troops[0][t5]')
            input_t5.send_keys(t5)
        if t6:
            input_t6 = self.chrome.find_element_by_name('troops[0][t6]')
            input_t6.send_keys(t6)
        if t7:
            input_t7 = self.chrome.find_element_by_name('troops[0][t7]')
            input_t7.send_keys(t7)
        if t8:
            input_t8 = self.chrome.find_element_by_name('troops[0][t8]')
            input_t8.send_keys(t8)
        if t9:
            input_t9 = self.chrome.find_element_by_name('troops[0][t9]')
            input_t9.send_keys(t9)
        if t10:
            input_t10 = self.chrome.find_element_by_name('troops[0][t10]')
            input_t10.send_keys(t10)
        if t11:
            input_t11 = self.chrome.find_element_by_name('troops[0][t11]')
            input_t11.send_keys(t11)
            
        input_x = self.chrome.find_element_by_name('x')
        input_x.send_keys(x)
        input_y = self.chrome.find_element_by_name('y')
        input_y.send_keys(y)

        input_sending_case = self.chrome.find_elements_by_name('c')[sending_case - 2]
        input_sending_case.click()

        submit = self.chrome.find_element_by_name('s1')
        submit.click()
        sleep(1)
            
    def send_scout(self, scout_num=1, x=0, y=0, scout_type=1):
        # scout_type: 1=資源 / 2=軍事
        if self.scout_id == 't3':
            self.send_troops(x=x, y=y, t3=scout_num, sending_case=3)
        else:
            self.send_troops(x=x, y=y, t4=scout_num, sending_case=3)
        
        input_scout_type = self.chrome.find_elements_by_name('troops[0][spy]')[scout_type - 1]
        input_scout_type.click()
        
        submit = self.chrome.find_element_by_id('btn_ok')
        submit.click()

    def auto_scouting(self):
        coord_list = list()
        sleep_choice = [3, 4, 5, 6, 7]
        self.login()
        self.chrome.get(self.url_target_alliance_members)
        player_num = len(self.chrome.find_elements_by_class_name('playerName')) - 1
        for i in range(player_num):
            self.chrome.get(self.url_target_alliance_members)
            btn_player = self.chrome.find_elements_by_class_name('playerName')[i].find_element_by_tag_name('a')
            print(btn_player.text)
            btn_player.click()
            for coord in self.chrome.find_elements_by_class_name('coords'):
                text_coord = coord.text
                text_coord = text_coord.replace('\u202c', '').replace('\u202d', '').replace('(', '').replace(')', '').replace('−', '-')
                x, y = text_coord.split('|')
                coord_list.append((x, y))
        print('Total %s villages' % len(coord_list))
        for ind, coord in enumerate(coord_list):
            self.send_scout(x=coord[0], y=coord[1])
            print('\r', ind, end='')
            sleep(choice(sleep_choice))
            
    
if __name__ == '__main__':
    ##### Setting #####
    data = {
        'name'              : '',
        'password'          : '',
        'village_newdid'    : '78286',
        'scout_id'          : 't4',
        'target_alliance_id': '44',
    }
    ###################
    tt = TravianTool(
        name=data['name'],
        password=data['password'],
        village_newdid=data['village_newdid'],
        scout_id=data['scout_id'],
        target_alliance_id=data['target_alliance_id']
    )
    
    if len(sys.argv) == 1:
        print('Please input command')
    else:
        if sys.argv[1] == 'auto_scouting':
            tt.auto_scouting()
        print('Work Complete!!!')
        input()
    
    tt.finish()
