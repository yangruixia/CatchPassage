from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import re
import pandas as pd

from bs4 import BeautifulSoup
# import requests

def extract_info(driver):
    with open('result.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # csv_writer = csv.writer(csvfile)
        # csv_writer.writerow(['Number', 'Scores', 'Passage'])
        data = [] 
        for i in range(157):
            try:
                time.sleep(2)  # 等待页面加载
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                pattern = r"get_zw_bzb\('([^']+)'\)"
                matches = re.findall(pattern,page_source )
                current_span = soup.find('span', class_='current')
                print(current_span.text[1:-1])

                if(int(current_span.text[1:-1])<155):
                    next_element = driver.find_element(By.LINK_TEXT, "下一页")
                    next_element.click()
                    continue

                    
                for txt_id in matches:
                    if txt_id=='200510302523200142':   #458 
                        # undifed 和 无标准文本的 数据 筛掉
                        continue
                    js_code = "get_zw_bzb('"+ txt_id +"')"
                    driver.execute_script(js_code)
                    time.sleep(1)  # 等待页面加载
                    
                    # title_element = driver.find_element(By.CLASS_NAME, "layui-layer-title")
                    # title_text = title_element.text
                    yl_txt_element = driver.find_element(By.ID, "yl_txt")
                    page_nav_element = yl_txt_element.find_element(By.ID, "PageNav")
                    page_text_element=driver.find_element(By.ID,"text_body")
                    page_nav_text = page_nav_element.text
                    page_text=page_text_element.text
                    if page_text=="undefined":
                        x_element = driver.find_element(By.CLASS_NAME, "layui-layer-ico.layui-layer-close.layui-layer-close1")
                        page_text=x_element.text
                        x_element.click()
                        continue
                    page_score=[txt_id]
                    text_score=page_nav_text.split('【')
                    t=text_score[1:]
                    for i in t:
                        start = i.find("：")  # 找到第一个冒号的位置
                        end = i.find("】", start)  # 找到冒号后面的第一个右方括号的位置
                        content = i[start + 1:end]  # 利用切片获取冒号后的内容
                        page_score.append(content)
                    if(txt_id=='200210529529251002'):
                        page_text=page_text[1:]
                    page_score.append(page_text)


                    data.append(page_score)
                    df = pd.DataFrame(data, columns=['作文编码', '作文标题', '国籍', '字数', '词数', '证书级别', '考试日期', '性别', '作文分数', '口试分数','听力理解分数','阅读理解分数','综合表达分数','考试总分','标注版文本'])
                    # 将 DataFrame 存储到 Excel 文件中
                    df.to_excel('output3.xlsx', index=False)
                    # csv_writer.writerow([txt_id+'/t',page_nav_text,page_text])
                    # print("PageNav 元素的文本内容:", page_nav_text,page_text)
                    time.sleep(1)
                    x_element = driver.find_element(By.CLASS_NAME, "layui-layer-ico.layui-layer-close.layui-layer-close1")
                    page_text=x_element.text
                    x_element.click()
                    time.sleep(2)  # 等待页面加载


                
                next_element = driver.find_element(By.LINK_TEXT, "下一页")

                # 模拟点击元素
                next_element.click()

            except Exception as e:
                print(f"An error occurred: {str(e)}")
        # print(Match)
        # try:
        #     num=0
        #     for i in Match:
        #         num+=1
        #         for j in range(len(i)):
        #             js_code = "get_zw_bzb('"+i[j]+"')"
        #             driver.execute_script(js_code)
                    
        #             page_source = driver.page_source
        #             # print(page_source)
        #             if(j==len(i)-1):
        #                 pattern0 = r'<div class="layui-layer-title".*?>.*?\[(\d+)\]</div>'
        #                 bianhao = re.findall(pattern, page_source)
        #                 pattern1 = r'<div id="PageNav">(.*?)</div>'
        #                 page_nav_text = re.findall(pattern1, page_source)
        #                 #print(page_source)
        #                 pattern2 = r'<pre id="text_body">(.*?)</pre>'
        #                 text_body_text= re.findall(pattern2, page_source,re.DOTALL)
        #                 #print(bianhao,page_nav_text,text_body_text)
        #                 for n in range(len(i)):
        #                     csv_writer.writerow([str(i[n])+'/t', page_nav_text[15*(num-1)+n], text_body_text[15*(num-1)+n]])
        # except Exception as e:
        #     print(f"An error occurred during login: {str(e)}")        
        # print('爬取完成')


if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path=r'D:\files-new\chromedriver\chromedriver-win64\chromedriver.exe')
    driver.get('http://hsk.blcu.edu.cn/')

# 用户输入账户和密码
    username = 'fangyouying'
    password = '1234'
    yanzhengma = input("yanzhengma: ")
    username_field = driver.find_element(By.ID, 'input_admin_name')  # 使用 By.ID 定位用户名输入框
    password_field = driver.find_element(By.ID, 'input_admin_pwd')  # 使用 By.ID 定位密码输入框
    yanzhengma_field = driver.find_element(By.ID, 'input_admin_verify')  # 使用 By.ID 定位验证码输入框

    username_field.send_keys(username)
    password_field.send_keys(password)
    yanzhengma_field.send_keys(yanzhengma)
    button = driver.find_element(By.XPATH, '//a[@id="exec_submit"]')  # 使用 By.XPATH 定位按钮
    button.click()

    try:
        # 等待登录完成
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.visibility_of_element_located((By.ID, 'nav_qpjs')))
        button.click()
        form_control_element = driver.find_element(By.CLASS_NAME, "btn-primary")
        form_control_element.click()

        extract_info(driver)
        print('已经查询完成')

        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@id="nav_qpjs"]')))
        # extract_info(driver)
        # print("Data has been saved to result.csv")

    except Exception as e:
        print(f"An error occurred during login: {str(e)}")

    # finally:
        # driver.quit()


        #200205271525100098、
