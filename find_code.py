from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,os,re
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook

def extract_info(driver):
    try:
        data=[]
        data = pd.DataFrame(columns=['编码', '性别'])
        for i in range(772):
            time.sleep(2)
            page_source = driver.page_source
            pattern = r"get_zw_bzb\('([^']+)'\)"
            matches = re.findall(pattern, page_source)
            soup = BeautifulSoup(page_source, 'html.parser')

            current_span = soup.find('span', class_='current')
            print(current_span.text[1:-1])
            # if(int(current_span.text[1:-1])<704):
            #     next_element = driver.find_element(By.LINK_TEXT, "下一页")
            #     next_element.click()
            #     continue

            trs = soup.find_all('tr')[1:]
            data_list = []

            for i, tr in zip(matches, trs):
                first_active_td = tr.find('td', class_='active')
                data = data.append({'编码': i, '性别': first_active_td.text.strip()}, ignore_index=True)

            data.to_excel('Code.xlsx', index=False)
            next_element = driver.find_element(By.XPATH, '//a[@class="next"]')
            next_element.click()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print('爬取完成')



if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path=r'D:\files-new\chromedriver\chromedriver-win64\chromedriver.exe')
    driver.get('http://hsk.blcu.edu.cn/')

    username = 'fangyouying'
    password = '1234'
    yanzhengma = input("yanzhengma: ")
    username_field = driver.find_element(By.ID, 'input_admin_name')
    password_field = driver.find_element(By.ID, 'input_admin_pwd')
    yanzhengma_field = driver.find_element(By.ID, 'input_admin_verify')

    username_field.send_keys(username)
    password_field.send_keys(password)
    yanzhengma_field.send_keys(yanzhengma)
    button = driver.find_element(By.XPATH, '//a[@id="exec_submit"]')
    button.click()

    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.visibility_of_element_located((By.ID, 'nav_qpjs')))
        button.click()
        form_control_element = driver.find_element(By.CLASS_NAME, "btn-primary")
        form_control_element.click()
        print('已经查询完成')

        extract_info(driver)

    except Exception as e:
        print(f"An error occurred during login: {str(e)}")
