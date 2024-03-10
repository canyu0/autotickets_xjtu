from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import with_tag_name
import time
from selenium.webdriver.common.keys import Keys
import cv2
import numpy as np
import requests
import base64
badminton_floor1_url="http://202.117.17.144/product/show.html?id=41"#羽毛球文体中心一楼选择场地
tennis_center="http://202.117.17.144/product/show.html?id=55"#网球文体中心
target=tennis_center
global_username=""#输入学号
global_password=""#输入密码
global_date="2022-12-09"#输入预定日期
global_time="20:01-21:00"#输入预定时间



class center:
    def __init__(self):
        self.status=0
        self.login_method=0
        self.flag=0

        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option("detach", True)

        self.driver=webdriver.Chrome(options=self.option)
        self.driver.maximize_window()
        self.driver.get(target)
        time.sleep(3)
        print("a")
    def login(self):
        username=self.driver.find_element(By.CLASS_NAME,'username')
        password=self.driver.find_element(By.CLASS_NAME,'pwd')
        login_button=self.driver.find_element(By.ID,'account_login')
        #self.driver.execute_script(username,)
        username.send_keys(global_username)
        password.send_keys(global_password)
        login_button.click()

    def choose_area(self):
        button_book=self.driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div/a[1]')
        
        print(button_book)
        button_book.click()
        
        button_date=self.driver.find_elements(By.CLASS_NAME,'date')
        button_1=button_date[0]
        for i in button_date:
            if i.text==global_date:
                button_1=i
                i.click()
        index_times=self.driver.find_elements(By.CLASS_NAME,'timer')
        index_time=index_times[0]
        for i in index_times:
            if i.text==global_time:
                index_time=i
                print('='*10)
        button_time=self.driver.find_element(with_tag_name("span").below(index_time))

        select_num=self.driver.find_element(By.ID,'sum')
        button_confirm=self.driver.find_element(By.ID,'reserve')

        while 1:
            button_1=self.driver.find_element(with_tag_name("span").below(button_time))
            str_class=button_time.get_attribute('class')
            #print(str_class)
            if('lock' in str_class):
                pass
            else:
                button_time.click()
                button_confirm.click()
                if(self.driver.title=='西安交通大学统一身份认证网关'):
                    self.flag=1
                    self.login()
                    break
                elif(self.driver.title=='预订-运动场地预订平台'):
                    break
            button_time=self.driver.find_element(with_tag_name("span").below(button_time))


            # time.sleep(1)
            # if select_num.text=='1':
            #     #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #     print("a"*20)
            #     button_confirm.click()
            #     print(self.driver.title)
            #     if(self.driver.title=='西安交通大学统一身份认证网关'):
            #         self.flag=1
            #         self.login()
            #         break
            #     elif(self.driver.title=='预订-运动场地预订平台'):
            #         pass
            # #button_1.click()
            # #button_time=self.driver.find_element(with_tag_name("span").below(button_time))
            # button_time=button_1


    def getpic(self):

        url1=self.driver.find_element(By.ID,'bg-img')
        time.sleep(0.5)
        url=url1.get_attribute('src')
        
        head,encode=url.strip().split(',')
        #print(encode)
        img = base64.urlsafe_b64decode(encode+ '=' * (4 - len(url) % 4))

        with open('temp.jpg', 'wb') as f:
            f.write(img)

    def checkpic(self):
        image_orign = cv2.imread("original.jpg")
        image_temp=cv2.imread("temp.jpg")
        gray_orign = cv2.cvtColor(image_orign,cv2.COLOR_BGR2GRAY)
        gray_temp=cv2.cvtColor(image_temp,cv2.COLOR_BGR2GRAY)
        [iss,jss]=gray_temp.shape
        img_search=np.zeros((iss,jss))

        for i in range(iss-1):
            for j in range(jss-1):
                minus=int(gray_orign[i,j])-int(gray_temp[i,j])
                if minus<0:
                    minus*=-1
                img_search[i,j]=minus

        count=0
        for i in range(iss-1):
            for j in range(jss-1):
                if(img_search[i,j]>5):
                    #print(img_search[i,j],gray_orign[i,j],gray_temp[i,j])
                    count+=1
                else:
                    img_search[i,j]=0
        sums=np.sum(img_search,axis=0)
        average=np.sum(img_search)/(jss)
        flag=True
        index=0
        if count>9000:
            return -1
        
        for i in range(jss-1):
            #print(sums[i])
            if sums[i]>average and flag :
                image_temp[:,i,:]=255
                #cv2.imshow("grey",image_temp)
                #cv2.waitKey()
                flag=False
                index=i
                return index
    def get_track(self,distance):      # distance为传入的总距离
        # 移动轨迹
        track=[]
        # 当前位移
        current=0
        # 减速阈值
        mid=distance*4/6
        # 计算间隔
        t=1
        # 初速度
        v=0.1
        sum=0
        while current<distance:
            if current<mid:
                # 加速度为2
                a=1
            else:
                # 加速度为-2
                a=-1
            v0=v
            # 当前速度
            v=v0+a*t
            # 移动距离
            move=v0*t+1/2*a*t*t
            # 当前位移
            current+=round(move)
            sum+=round(move)
            # 加入轨迹
            track.append(round(move))
        last=track.pop()
        sum-=last
        track.append(distance-sum)
        print(track)
        return track

            
    def reserve(self):
        time.sleep(1)
        action = webdriver.ActionChains(self.driver)
        button_reserve=self.driver.find_element(By.ID,'reserve')
        button_reserve.click()
        
        self.driver.switch_to.frame('captcha-iframe')
        button_refresh=self.driver.find_element(By.ID,'slider-refresh-btn')
        #self.getpic()
        index=-1
        while 1:
            self.getpic()
            #time.sleep(1)
            index=self.checkpic()
            #time.sleep(1)
            aaa=1
            if index==-1:
                button_refresh.click()
                #time.sleep(1)
                print("a")
            else:
                print(index)
                break
        print("over")
        
        time.sleep(1)
        button_slider=self.driver.find_element(By.CLASS_NAME,'slider-move-btn')
        action.click_and_hold(button_slider).perform()
        distance=int((index-20)*260/590)
        tracks=self.get_track(distance)
        for x in tracks:
            action.move_by_offset(xoffset=x,yoffset=0)
        time.sleep(1)
        action.release().perform()
        time.sleep(1)
        self.driver.switch_to().default_content()
        button_confirm=self.driver.find_element(By.CLASS_NAME,'confirm')
        button_confirm.click()

        


    
if __name__=='__main__':
    con=center()

    con.choose_area()
    if con.flag==1:
        print("b"*10)
        time.sleep(2)
        con.choose_area()
    con.reserve()
    cv2.waitKey(0)
    