#for public version 
from splinter import Browser
from selenium.webdriver.chrome.options import Options
import time
import datetime
import getpass
import os

# General Fixed Data
# windows clear command
clear = 'cls'
# linux clear command
# clear = 'clear'
# maximum time set
maxtime = 8

def enter():
	acc = input('>> 請輸入ncu portal帳號:')
	while len(acc) != 9:
		acc = input('[Error] 帳號格式錯誤，請輸入ncu portal帳號:')
	pwd = getpass.getpass('>> 請輸入ncu portal密碼:')
	while len(pwd) < 8 or len(pwd) > 20:
		pwd = getpass.getpass('[Error] 密碼格式錯誤，請輸入ncu portal密碼:')
	return acc,pwd

def today_sign_time():
	needtime = int(input('\n>> 輸入今日要簽的時數，輸入0直接簽退:'))
	while needtime > maxtime or needtime < 0:	
		needtime = int(input('\n[Error] 時數不符，重新輸入時數:'))
	return needtime

#flag is 0 when its the acc,pwd are not checked
def open_web(acc,pwd):	
	chrome_options = Options()
	chrome_options.add_argument('disable-infobars')
	b = Browser("chrome",options=chrome_options)
	b.visit("https://cis.ncu.edu.tw/HumanSys/login")
	b.fill("j_username",acc)
	b.fill("j_password",pwd)
	b.find_by_xpath('//button[@type="submit"]').click()
	
	#check the acc pwd are match or not
	#flag is 0 when its the acc,pwd are not checked
	
	while b.url == 'https://portal.ncu.edu.tw/login?login_error=t' or b.url == 'https://tarot.cc.ncu.edu.tw/UnixAccount/enableaccount.php':
		b.quit()
		os.system(clear)
		print('[Error] 帳號或密碼輸入錯誤！\n \n>> 請重新輸入\n')
		acc,pwd = enter()
		b = open_web(acc,pwd)
	return b
	
def enter_HumanSys(b):
	b.visit("https://cis.ncu.edu.tw/HumanSys/student/stdSignIn")
	btn = b.find_by_xpath('//a[@href]')[8]
	btn.click()
	return b

def sign_in(b) :
	b.find_by_id('signin').click()

def sign_out(b) :
	b.fill('AttendWork','機房值班')
	b.find_by_id('signout').click()

def timer(intime):
	start_time = datetime.datetime.now()
	end_time = start_time + datetime.timedelta(hours = intime)
	one_hour_later_flag = start_time + datetime.timedelta(hours = 1)
	while end_time >= datetime.datetime.now()  :
		if datetime.datetime.now().timetuple()[3:5] == one_hour_later_flag.timetuple()[3:5]:
			print('>> 已經值班了'+str(datetime.datetime.now().timetuple()[3] - start_time.timetuple()[3])+'小時')
			one_hour_later_flag = datetime.datetime.now() + datetime.timedelta(hours = 1)
		time.sleep(600) #sleep 10 minutes
	
#main
acc,pwd = enter()
needtime = today_sign_time()
if needtime != 0:
	b = open_web(acc,pwd)
	enter_HumanSys(b)
	try:
		sign_in(b)
	except:
		print("\n[Error] 無法順利完成簽到 >>請確認網頁資訊或重新嘗試")
		lefttime = int(input('\n>> 請輸入需要剩餘時數(退出此程式請輸入0): '))
		while int(lefttime) > maxtime:
			os.system(clear)
			print('\n[Error] 輸入超過每日上線！')
			lefttime = int(input('>> 請再次輸入需要剩餘時數(退出請輸入0): '))
		if lefttime <= 0:
			b.quit()
			input('請按任意鍵繼續......')
			quit()
		timer(lefttime)
	finally:
		b.quit()
		os.system(clear)
		print('\n>> 完成簽到')
		print('\n>> 等待簽退')
		timer(needtime)
#定時簽退
b = open_web(acc,pwd)
enter_HumanSys(b)
sign_out(b)
print('\n>> 完成簽退')
b.quit()
input('\n請按任意鍵繼續......')