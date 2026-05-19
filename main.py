import time
import traceback
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Автоматически скачивает и настраивает ChromeDriver
service = Service(ChromeDriverManager().install())

options = Options()
# options.page_load_strategy = "eager"
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.maximize_window()
    driver.implicitly_wait(30)
    
    driver.get("https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fpulls%2Freview-requested")
    driver.find_element(By.XPATH, '//input[@id="login_field"]').send_keys('YuriSilenok')
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys('a1501274296')
    driver.find_element(By.XPATH, '//input[@value="Sign in"]').click()
    driver.find_element(By.XPATH, '//button[@data-disable-with="More options…"]').click()
    driver.find_element(By.XPATH, '//span/span/span[.="GitHub Mobile"]').click()

    while True:
        try:
            driver.find_element(By.XPATH, '//a[@title="Pull requests requesting your review"]').click()
            break
        except:
            print('Страница с PR не загружена')


    while True:
        try:
            driver.get("https://github.com/pulls/review-requested")
            links = [pr_link.get_attribute("href") for pr_link in driver.find_elements(By.XPATH, '//a[@data-hovercard-type="pull_request"]')]
            for pr_url in links:
            
                driver.get(pr_url)
                print(pr_url)
                driver.find_element(By.XPATH, '//a[@id="prs-files-anchor-tab"]').click()
                # time.sleep(3)
                try:
                    doc_md = driver.find_element(By.XPATH, '//a[.="doc.md"]')
                except Exception as ex:
                    print(pr_url, 'файл doc.md не найден')
                    continue
                repo = driver.find_element(By.XPATH, '(//a[contains(@class, "PullRequestBranchName")])[2]').get_attribute('href').replace('tree', 'refs/heads').replace('github', 'raw.githubusercontent')
                folder = driver.find_element(By.XPATH, '//span[contains(@class, "PRIVATE_TreeView-item-content-text")]/span').text
                repo_url = f'{repo}/{folder}/doc.md'
                driver.get(repo_url)
                doc_md_text = driver.find_element(By.XPATH,  '//pre').text
                
                driver.get("https://giga.chat/")
                
                textarea = driver.find_element(By.XPATH, '//textarea')

                promt = ''

                with open(file='promt.txt', mode='r', encoding='utf-8') as f:
                    promt = ''.join(f.readlines())
                
                promt += doc_md_text
                
                for line in promt.split('\n'):
                    line = line.replace('\r', '')
                    textarea.send_keys(line + (Keys.SHIFT + Keys.ENTER))

                textarea.send_keys(Keys.ENTER)
                time.sleep(60)
                driver.find_element(By.XPATH, '(//button[@data-da_name="MessageCopyButton"])[last()]').click()
                time.sleep(3)
                driver.get(pr_url)
                driver.find_element(By.XPATH, '//a[@id="prs-files-anchor-tab"]').click()
                driver.find_element(By.XPATH, '//button[.//span[contains(., "Submit")]]').click()
                driver.find_element(By.XPATH, '//textarea[@placeholder="Leave a comment"]').send_keys(pyperclip.paste())
                driver.find_element(By.XPATH, '(//div[button[.//span[.="Cancel"]]]//button)[2]').click()
                time.sleep(30)


        except Exception as ex:
            print(pr_url, '\n', traceback.format_exc())
        # break
        time.sleep(60)
    
finally:
    driver.quit()
    print("Браузер закрыт.")