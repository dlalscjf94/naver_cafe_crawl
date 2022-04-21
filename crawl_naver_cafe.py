"""
네이버 카페 내 전체 게시글들 크롤링 및 엑셀 작성하는 코드 - mdby.LMC
"""

# 데이터 엑셀 저장 및 dataFrame 운용을 위한 pandas import
import pandas as pd

# 크롤링한 텍스트 정규화를 위한 re import
import re
import requests

# 기본 크롤링을 위한 webdriver import
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# selenium exception
from selenium.common import exceptions
from datetime import datetime

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip


def get_url_lst():

    url_lst = []

    # 네이버 계정으로 로그인 한 상태에서 진행
    # 전체글 보기 상태 url 지정
    # 최초에 로그인페이지로 진입 시도
    # 로그인 우회 필요

    # url = 'https://cafe.naver.com/hubhaksa'
    url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https://cafe.naver.com/hubhaksa'

    driver = webdriver.Chrome()

    driver.get(url)

    # 로그인 진행필요
    # id xpath 및 pw xpath 확인

    time.sleep(5)

    """
    # id 창 find_element_by_name
    inputid = driver.find_element_by_name("id")

    # id 전송
    inputid.send_keys('nmecrew')

    # pw 창
    inputpw = driver.find_element_by_name("pw")

    # pw 전송
    inputpw.send_keys('NMECREW!!')

    # 로그인 버튼 클릭
    login_btn = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/form/fieldset/input')

    login_btn.click()
    """

    # 로그인 우회 성공 pyperclip 이용
    id = '본인ID입력'
    pw = '본인PW입력'
    pyperclip.copy(id)

    driver.find_element_by_name("id").click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(4)

    pyperclip.copy(pw)

    driver.find_element_by_name("pw").click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(4)

    # 로그인 버튼 클릭
    login_btn = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/form/fieldset/input')

    login_btn.click()

    time.sleep(4)

    """
    # 전체글보기 클릭

    see_ent = driver.find_element_by_xpath('/html/body/div[4]/div/div[7]/div[1]/div[2]/div[2]/ul[2]/li[1]/a')

    see_ent.click()

    time.sleep(3)

    # iframe 적용 필요
    driver.switch_to.frame("cafe_main")

    # tbody
    tbody = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/table/tbody')

    a_tags = tbody.find_elements_by_tag_name('a')

    for a_tag in a_tags:

        link = a_tag.get_attribute('href')

        # url 에 articleid가 존재하는 경우만 print, append
        if 'articleid' in link:

            print(link)
            url_lst.append(link)

        else:

            pass

    # print(url_lst)

    time.sleep(3)
    
    """

    # https://cafe.naver.com/hubhaksa?iframe_url=/ArticleList.nhn%3Fsearch.clubid=17745091%26search.boardtype=L%
    # 26search.totalCount=151%26search.page=1
    # 페이지 컨트롤 가능
    """
    page_cnt = 1

    while True:

            # 페이지 베이스 url
            base_url = 'https://cafe.naver.com/hubhaksa?iframe_url=/ArticleList.nhn%3Fsearch.clubid=17745091%26' \
                       'search.boardtype=L%26search.totalCount=151%26search.page={}'

            url = base_url.format(page_cnt)

            driver.get(url)

            time.sleep(3)

            # iframe 적용 필요
            driver.switch_to.frame("cafe_main")

            # tbody
            tbody = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/table/tbody')

            a_tags = tbody.find_elements_by_tag_name('a')

            # 만약 링크를 가지고 있는 결과물이 하나도 없다면 return
            if len(a_tags) == 0:

            #  - test 용
            # if page_cnt == 2:

                print(url_lst)

                # 드라이버를 같이 return 해주어야 함
                return url_lst, driver

            else:

                for a_tag in a_tags:

                    link = a_tag.get_attribute('href')

                    # url 에 articleid가 존재하는 경우만 print, append
                    if 'articleid' in link:

                        print(link)
                        url_lst.append(link)

                    else:

                        pass

                page_cnt = page_cnt + 1
    """

    # url_lst 파일을 생성했을 경우 이 코드를 통해 시간 단축 가능
    url_lst = read_xlsx()

    return url_lst, driver


def crawl_url(url_lst, driver):

    global t_text
    global n_text
    global cnt_text

    # 글제목 lst
    title_lst = []

    # 작성자 lst
    nickname_lst = []

    # 조회수
    cnt_lst = []

    # 첨부파일 리스트
    att_lst = []

    # URL_LST
    f_url_lst = []

    driver = driver

    for i in range(0, len(url_lst), 1):

        driver.get(url_lst[i])

        time.sleep(3)

        driver.switch_to.frame('cafe_main')

        print("===============================================")

        try:

            title = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[1]/div[1]/div/h3')

            print("제목 : ", title.text)

            t_text = title.text

            # title_lst.append(title.text)

        except:

            # title_lst.append('NULL')
            t_text = 'NULL'

        try:

            nickname = driver.find_element_by_class_name('nick_box')

            print("작성자 : ", nickname.text)

            n_text = nickname.text

            # nickname_lst.append(nickname.text)

        except:

            # nickname_lst.append('NULL')
            n_text = 'NULL'

        try:

            cnt = driver.find_element_by_class_name('count')

            count_text = cnt.text.replace("조회 ", "")

            print("조회 수 : ", count_text)

            cnt_text = count_text

            # cnt_lst.append(count_text)

        except:

            # cnt_lst.append('NULL')

            cnt_text = 'NULL'

        try:
            """
            # a태그 자체를 가져와서
            att_file = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/div/div/a')
            # 링크만 뜯어내기
            att_file_link = att_file.get_attribute('href')

            print("첨부파일 링크 : ", att_file_link)
            att_lst.append(att_file_link)
            """

            # att_files = driver.find_element_by_class_name('file_download')

            # 클래스 변경

            att_files = driver.find_element_by_class_name('layer_attach')

            a_tags = att_files.find_elements_by_tag_name('a')

            # tot_link = ''

            for a_tag in a_tags:

                print(a_tag.get_attribute('href'))

                link = a_tag.get_attribute('href')

                # 2개 이상인경우 링크 이어 붙이기
                if 'downapi.cafe.naver.com' in link:

                    print("첨부파일 링크 : ", link)

                    title_lst.append(t_text)
                    nickname_lst.append(n_text)
                    cnt_lst.append(cnt_text)
                    att_lst.append(link)
                    f_url_lst.append(url_lst[i])

                    # tot_link = tot_link + ',' + link

                # 옛날게시글 첨부파일 링크 형태 링크 추가 (20201114)
                elif 'cafeattach.naver.net' in link:

                    print("첨부파일 링크 : ", link)

                    title_lst.append(t_text)
                    nickname_lst.append(n_text)
                    cnt_lst.append(cnt_text)
                    att_lst.append(link)
                    f_url_lst.append(url_lst[i])

                    # tot_link = tot_link + ',' + link

                # 옛날게시글 첨부파일 링크 형태 링크 추가 (20201115)
                elif 'bolgattach.naver.net' in link:

                    print("첨부파일 링크 : ", link)

                    title_lst.append(t_text)
                    nickname_lst.append(n_text)
                    cnt_lst.append(cnt_text)
                    att_lst.append(link)
                    f_url_lst.append(url_lst[i])

                else:

                    pass

        except:

            print("첨부파일이 없습니다.")

            title_lst.append(t_text)
            nickname_lst.append(n_text)
            cnt_lst.append(cnt_text)
            att_lst.append('NULL')
            f_url_lst.append(url_lst[i])

        # /html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div/ul

        print("===============================================")

    dict = {"글제목": title_lst, "작성자": nickname_lst, "조회 수": cnt_lst, "첨부파일": att_lst, "URL": f_url_lst}

    df = pd.DataFrame(dict)

    df.to_excel("최종파일"+".xlsx", sheet_name='sheet1')


def make_xlsx(url_lst):

    dict = {"URL": url_lst}

    df = pd.DataFrame(dict)

    df.to_excel('URL_LST'+'.xlsx', sheet_name='sheet1')


# 저장해둔 url_lst 꺼내쓰기
def read_xlsx():

    df = pd.read_excel('URL_LST.xlsx')

    url_lst = df['URL'].tolist()

    return url_lst


# 메인, 모듈 관리
def main():

    url_lst, driver = get_url_lst()

    # make_xlsx(url_lst)

    crawl_url(url_lst, driver)


if __name__ == '__main__':

     main()
