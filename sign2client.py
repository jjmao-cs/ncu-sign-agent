import requests
from lxml import html
from bs4 import BeautifulSoup as bs
import getpass


#get your personal identity
def get_id():
    acc = input('\n>> 請輸入NCU Portal帳號:')
    while len(acc) != 9:
	    acc = input('\n[Error] 帳號格式錯誤，請輸入ncu portal帳號:')
    password = getpass.getpass('\n>> 請輸入ncu portal密碼:')
    while len(password) < 8 or len(password) > 20:
	    password = getpass.getpass('\n[Error] 密碼格式錯誤，請輸入ncu portal密碼:')
    return id,password


#get the time you want to sign
def get_time():
    maxtime = 8
    needtime = int(input('\n>> 輸入今日要簽的時數，輸入0直接簽退:'))
    while needtime > maxtime or needtime < 0:	
        needtime = int(input('\n[Error] 時數不符，重新輸入時數:'))
    return needtime


#get job description
def get_job_description():
    job_description = input('\n>> 請輸入工作內容(直接Enter使用預設):')
    if job_description == '':
        job_description = '機房值班'
    return job_description


#main sign core
def sign_start(id,password,job_description):

    with requests.session() as session_requests:
        #parameters
        cookie=session_requests.get('https://portal.ncu.edu.tw')
        cookie=session_requests.cookies.get_dict() #cookie for NCU_Portal login
        User_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        header={
            'User-Agent':User_agent,}
        log={
            'j_username':id,
            'j_password':password}
        
        # <<login to NCU_Portal>>
        # we go straight to the login page and send the inform to the server to let session login
        result=session_requests.post(
            'https://portal.ncu.edu.tw/j_spring_security_check',
            data=log,
            headers=header,
            cookies=cookie)

        # <<Enter HR System to get __token, ParttimeUsuallyId, idNo for each sign in/out>>
        human=session_requests.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn') # session_requests.get('https://portal.ncu.edu.tw/system/143')
        soup_human = bs(human.text, "lxml")
        #print(soup_human.find_all('a'))
        check='https://cis.ncu.edu.tw/HumanSys/student/'+soup_human.find_all('a')[-2].get('href') # url for the job's sign page
        sign=session_requests.get(check) # goto job's sign page
        soup_sign = bs(sign.text, "lxml") # through BeautifulSoup inorder to get some information
        sign_token = soup_sign.find_all("input")[0].get('value') # get the token used to protect the server of sign page
        ParttimeUsuallyId = soup_human.find_all('a')[-2].get('href').split("=")[-1] # ParttimeUsuallyId is an ID related to a person and its job
        idNo=soup_sign.find(id='idNo') 
            # idNo will be empty before sign in, 
            # the system will give client a idNo after sign in,
            # will be use when sign out.

        # <<Sign in an Sign out>>
        sign_data={
            'functionName' : "doSign",
            'idNo' : idNo['value'],
            'ParttimeUsuallyId' : ParttimeUsuallyId,
            'AttendWork' : job_description,
            '_token' : sign_token
        }
        sign_header = header.copy()

        # WARNING DO NOT REMOVE OR ADD THE PARA. BELOW. WILL CAUSE ERROR #
        #del sign_header['Referer']
        #sign_header['Host'] = 'https://cis.ncu.edu.tw'
        #print(sign.cookies.get_dict())

        sign_post=session_requests.post(
            'https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail',
            data = sign_data,
            headers = sign_header,
        )
        
        # used to make a GET to server, now seems USELESS
        '''data={'ParttimeUsuallyId' : ParttimeUsuallyId,
                'msg':'signin_ok'}
        sign_out_get=session_requests.get(
            'https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId=84668&msg=signout_ok',
            headers = sign_header,
            cookies = sign.cookies.get_dict()
        )
        #print(sign_out_post)
        #print(bs(sign_out_post.text, "lxml"))
        '''


if __name__ == "__main__":
    id, password = get_id()
    time = get_time()
    job_description = get_job_description()
    sign_start(id,password,job_description)
    print('QQQ')
    pass

#客戶端版_開發日誌
'''
0307 資訊輸入完成，須加入帳號密碼錯誤提示
'''