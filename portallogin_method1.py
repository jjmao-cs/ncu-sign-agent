import requests
from lxml import html
from bs4 import BeautifulSoup as bs


def sign_start(id,password):

    with requests.session() as session_requests:
        #參數
        cookie=session_requests.get('https://portal.ncu.edu.tw')
        cookie=session_requests.cookies.get_dict()
        User_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        header={
            'Referer': 'https://portal.ncu.edu.tw/login',
            'User-Agent':User_agent,}
        log={
            'j_username':id,
            'j_password':password}
        
        #save=session_requests.post('https://portal.ncu.edu.tw')
        result=session_requests.post(
            'https://portal.ncu.edu.tw/j_spring_security_check',
            data=log,
            headers=header,
            cookies=cookie)


        #human=session_requests.get('https://portal.ncu.edu.tw/system/143')
        human=session_requests.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn')
        soup_human = bs(human.text, "lxml")
        #print(soup_human.find_all('a'))

        check='https://cis.ncu.edu.tw/HumanSys/student/'+soup_human.find_all('a')[-2].get('href') 
        sign=session_requests.get(check) #到簽到網站
        #print(check)
        #print(soup_human.find_all('a')[-2].get('href').split("=")[-1])
        #'''
        soup_sign = bs(sign.text, "lxml")
        sign_token = soup_sign.find_all("input")[0].get('value')
        ParttimeUsuallyId = soup_human.find_all('a')[-2].get('href').split("=")[-1]
        sign_data={
            'functionName' : "doSign",
            'idNo' : '',
            'ParttimeUsuallyId' : ParttimeUsuallyId,
            'AttendWork' : '',
            '_token' : sign_token
        }
        sign_header = header.copy()
        del sign_header['Referer']
        sign_header['Host'] = 'https://cis.ncu.edu.tw'
        #print(sign_header)
        
        sign_out_post=session_requests.post(
            'https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail',
            data=sign_data,
            headers = sign_header
        )
        sign_out_get=session_requests.get(
            'https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId=84668&msg=signout_ok',
            headers = sign_header
        )
        print(bs(sign_out_post.text, "lxml"))
        

if __name__ == "__main__":
    #id,password=input().split()
    sign_start(id,password)
    pass