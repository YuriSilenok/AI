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


def check_models_py(pr_url: str):
    driver.get(pr_url)
    wait_element('//a[@id="prs-files-anchor-tab"]').click()
    try:
        driver.find_element(By.XPATH, '//a[.="models.py"]')
    except Exception as ex:
        send_review(pr_url, 'файл models.py не найден')
        return False
    repo = driver.find_element(By.XPATH, '(//a[contains(@class, "PullRequestBranchName")])[2]').get_attribute('href').replace('tree', 'refs/heads').replace('github', 'raw.githubusercontent')
    folder = driver.find_element(By.XPATH, '//span[contains(@class, "PRIVATE_TreeView-item-content-text")]/span').text
    
    repo_url_doc_md = f'{repo}/{folder}/doc.md'
    driver.get(repo_url_doc_md)
    doc_md = driver.find_element(By.XPATH,  '//pre').text
    
    repo_url_models_py = f'{repo}/{folder}/models.py'
    driver.get(repo_url_models_py)
    models_py = driver.find_element(By.XPATH,  '//pre').text
                
    promt = f'Проверь соотвесвие реализации models.py по требованиям из doc.md\n\n`doc.md`\n\n{doc_md}\n\n`models.py`\n\n{models_py}.\n\nЕсли всё соответсвует требованиям, тебе запрещается использовать слово "есть".'

    review = send_promt(promt)
    if 'есть' in review:
        send_review(pr_url, review)
        return False
    return True


def check_doc_md(pr_url: str):
    driver.get(pr_url)
    wait_element('//a[@id="prs-files-anchor-tab"]').click()
    try:
        driver.find_element(By.XPATH, '//a[.="doc.md"]')
    except Exception as ex:
        send_review(pr_url, 'файл doc.md не найден')
        return False
    repo = driver.find_element(By.XPATH, '(//a[contains(@class, "PullRequestBranchName")])[2]').get_attribute('href').replace('tree', 'refs/heads').replace('github', 'raw.githubusercontent')
    folder = driver.find_element(By.XPATH, '//span[contains(@class, "PRIVATE_TreeView-item-content-text")]/span').text
    repo_url = f'{repo}/{folder}/doc.md'
    driver.get(repo_url)
    
                
    promt = ''
    with open(file='promt.txt', mode='r', encoding='utf-8') as f:
        promt = ''.join(f.readlines())
    promt += driver.find_element(By.XPATH,  '//pre').text
    review = send_promt(promt)
    if 'есть' in review:
        send_review(pr_url, review)
        return False
    return True


def wait_element(xpath: str):
        while True:
            try:
                return driver.find_element(By.XPATH, xpath)
            except:
                print(f'Элемент не найден {xpath}')


def send_promt(promt:str):
    driver.get("https://giga.chat/")
    textarea = wait_element('//textarea')

   
    for line in promt.split('\n'):
        line = line.replace('\r', '')
        textarea.send_keys(line + (Keys.SHIFT + Keys.ENTER))

    textarea.send_keys(Keys.ENTER)
    print('Промт отправлен')
    wait_element('//button[contains(@class, "ActionMessageButton")]')
    driver.find_element(By.XPATH, '(//button[@data-da_name="MessageCopyButton"])[last()]').click()
    time.sleep(1)
    print('Ответ на промт получен')
    return pyperclip.paste()

def send_review(pr_url: str, text: str):
    driver.get(pr_url)
    time.sleep(15)
    driver.find_element(By.XPATH, '//a[@id="prs-files-anchor-tab"]').click()
    driver.find_element(By.XPATH, '//button[.//span[contains(., "Submit")]]').click()
    driver.find_element(By.XPATH, '//textarea[@placeholder="Leave a comment"]').send_keys(text)
    driver.find_element(By.XPATH, '(//div[button[.//span[.="Cancel"]]]//button)[2]').click()
    wait_element('//button[@data-comment-text="Close with comment"]')
    print('Проверка отправлена')

try:
    driver.maximize_window()
    driver.implicitly_wait(30)
    
    driver.get("https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fpulls%2Freview-requested")
    driver.find_element(By.XPATH, '//input[@id="login_field"]').send_keys('YuriSilenok')
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys('a1501274296')
    driver.find_element(By.XPATH, '//input[@value="Sign in"]').click()
    driver.find_element(By.XPATH, '//button[@data-disable-with="More options…"]').click()
    driver.find_element(By.XPATH, '//span/span/span[.="GitHub Mobile"]').click()
    
    wait_element('//a[@title="Pull requests requesting your review"]')

    delay = 30
    while True:
        try:
                
            links = [pr_link.get_attribute("href") for pr_link in driver.find_elements(By.XPATH, '//a[@data-hovercard-type="pull_request"]')]
            
            # if not links:
            #     break
            
            for pr_url in links:
                delay //= 2
                print(pr_url)


                if not check_doc_md(pr_url):
                    continue
                
                if not check_models_py(pr_url):
                    continue


                send_review(pr_url, 'Бот не нашел к чему придраться, но он не всё проверяет.')

        except Exception as ex:
            print(pr_url, '\n', traceback.format_exc())

        delay += 1
        time.sleep(delay)
        driver.get("https://github.com/pulls/review-requested")
        wait_element('//a[@title="Pull requests requesting your review"]').click()
    
finally:
    driver.quit()
    time.sleep(3)
    print("Браузер закрыт.")