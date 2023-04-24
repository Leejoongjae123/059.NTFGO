import openpyxl
import pandas as pd
from pyautogui import size
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import datetime
import pyautogui
import pyperclip
import csv
import sys
import os
import math
import requests
import re
import random
import chromedriver_autoinstaller
from PyQt5.QtWidgets import QWidget, QApplication, QTreeView, QFileSystemModel, QVBoxLayout, QPushButton, QInputDialog, \
    QLineEdit, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QCoreApplication
from selenium.webdriver import ActionChains
from datetime import datetime, date, timedelta
import numpy
import datetime
# from window import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
import requests
import pprint


def get_collection(end_limit):
    count=0
    contracts_description_list = []
    for i in range(0,9999):
        if end_limit==i:
            print("끝")
            break
        url = "https://data-api.nftgo.io/eth/v1/market/rank/collection/1h?by=market_cap&with_rarity=false&asc=false&offset={}&limit=50".format(i*50)
        headers = {
            "accept": "application/json",
            "X-API-KEY": "bbf39436-0723-41fc-b95d-7dfe87bab701"
        }

        response = requests.get(url, headers=headers)

        # print(response.text)

        results=json.loads(response.text)['collections']


        for index,result in enumerate(results):
            name=result['name']
            contracts=result['contracts'][0]
            print(count+1,"번째 ","name:",name,"contracts:",contracts)
            description=result['description']
            data=[contracts,description,name]
            contracts_description_list.append(data)
            count=count+1
        print("총갯수:",len(contracts_description_list))
    return contracts_description_list



def get_nft(contracts_description_list):

    url = "https://data-api.nftgo.io/eth/v1/collection/{}/filtered_nfts?sort_by=listing_price_high_to_low&is_listing=true&offset=0&limit=10".format(contracts_description_list[0])

    headers = {
        "accept": "application/json",
        "X-API-KEY": "bbf39436-0723-41fc-b95d-7dfe87bab701"
    }

    response = requests.get(url, headers=headers)

    # print(response.text)

    results=json.loads(response.text)['nfts']

    count=0
    nft_infos=[]
    for index,result in enumerate(results):
        if count>=3:
            break
        #pprint.pprint(result)
        #이름 가져오기
        name="{}_{}".format(contracts_description_list[2],result['name'].replace("#",""))
        print('name:',name)
        #이미지 가져오기
        image=result['image']
        if image.find("sandbox")>=0:
            print("샌드박스건너뜀")
            continue
        print('image:',image)

        file_type=""
        type_list=['svg','jpg','png','gif','jpeg']
        for type_elem in type_list:
            if image.find(type_elem)>=0:
                file_type=type_elem
        if file_type=="":
            file_type="jpg"




        file_path = "001"
        createFolder(file_path)  # 그림파일 저장폴더 생성
        user_agent={"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        while True:
            try:
                image_res= requests.get(image,headers=user_agent)
                image_res.raise_for_status()
                break
            except:
                print("다운로드에러로 잠시 대기")
                time.sleep(3)

        save_path="{}/{}.{}".format(file_path, name.replace('"','').replace(":","").replace("/","").replace("?","").replace("'",""),file_type)
        with open (save_path, "wb") as f:
            f.write(image_res.content)
            print("이미지다운로드완료")


        units=result['listing_price']['crypto_unit']
        if units=="ETH":
            price=result['listing_price']['value']
            print('price:',price)
            count = count + 1
        token_id=result['token_id']
        print('description:',contracts_description_list[1])
        print('token_id:',token_id)
        print('contracts:',contracts_description_list[0])
        print("=================================")
        data=[name,contracts_description_list[1],price,save_path]
        nft_infos.append(data)

    return nft_infos


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


filename='csv_new.csv'
f=open(filename,'w',encoding="utf-8-sig",newline="")
writer=csv.writer(f)
column_name=['상품코드','자체 상품코드','진열상태','판매상태','상품분류 번호','상품분류 신상품영역','상품분류 추천상품영역','상품명','영문 상품명','상품명(관리용)','공급사 상품명','모델명',
             '상품 요약설명','상품 간략설명','상품 상세설명','모바일 상품 상세설명 설정','모바일 상품 상세설명','검색어설정','과세구분','소비자가','공급가','상품가','판매가',
             '판매가 대체문구 사용','판매가 대체문구','주문수량 제한 기준','최소 주문수량(이상)','최대 주문수량(이하)','적립금','적립금 구분','공통이벤트 정보','성인인증',
             '옵션사용','품목 구성방식','옵션 표시방식','옵션세트명','옵션입력','옵션 스타일','버튼이미지 설정','색상 설정','필수여부','품절표시 문구','추가입력옵션',
             '추가입력옵션 명칭','추가입력옵션 선택/필수여부','입력글자수(자)','이미지등록(상세)','이미지등록(목록)','이미지등록(작은목록)','이미지등록(축소)','이미지등록(추가)',
             '제조사','공급사','브랜드','트렌드','자체분류 코드','제조일자','출시일자','유효기간 사용여부','유효기간','원산지','상품부피(cm)','상품결제안내','상품배송안내','교환/반품안내',
             '서비스문의/안내','배송정보','배송방법','국내/해외배송','배송지역','배송비 선결제 설정','배송기간','배송비 구분','배송비입력','스토어픽업 설정','상품 전체중량(kg)',
             "HS코드",'상품 구분(해외통관)','상품소재','영문 상품소재(해외통관)','옷감(해외통관)','검색엔진최적화(SEO) 검색엔진 노출 설정','검색엔진최적화(SEO) Title',
             '검색엔진최적화(SEO) Author','검색엔진최적화(SEO) Description','검색엔진최적화(SEO) Keywords','검색엔진최적화(SEO) 상품 이미지 Alt 텍스트','개별결제수단설정',
             '상품배송유형 코드','메모']
writer.writerow(column_name)

end_limit=6
contracts_description_list=get_collection(end_limit)
for contracts_description_elem in contracts_description_list:
    nft_infos=get_nft(contracts_description_elem)

    for nft_info in nft_infos:
        data_row=["","","Y","Y","23","N","N",nft_info[0],nft_info[0],"","","NoBrand",nft_info[0],nft_info[0],nft_info[1],"","","","B",nft_info[2],nft_info[2],nft_info[2],nft_info[2],
                  "N","","O",1,"",0,"P","N","N","N","","","","","","","","","","","","","",nft_info[3],nft_info[3],nft_info[3],nft_info[3],
                  "","","","","","","","","","","","","","","","","T","I",'B','전국','B',1,'T',
                  "","","","","","","","","","","","","","","",'C']
        writer.writerow(data_row)
f.close()
