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


start_message = (
    'Это отзыв ИИ которая проверяет только соответсвие `Требованиями к УП`. '
    'Если у ИИ есть какие-то замечания, то это не значит что так и есть. '
    'Вы должны убедиться что в этом месте у Вас написано верно, это поможет вам сократить время ожидании проверки вашей работы на занятии. '
)


def wait_element(xpath: str):
        while True:
            try:
                return driver.find_element(By.XPATH, xpath)
            except:
                print(f'Элемент не найден {xpath}')


def send_promt(promt:str):
    driver.get("https://giga.chat/")
    textarea = wait_element('//textarea')
    textarea.click()
    pyperclip.copy(promt)
    textarea.send_keys(Keys.CONTROL + 'v')
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
    pyperclip.copy(text)
    comment = driver.find_element(By.XPATH, '//textarea[@placeholder="Leave a comment"]')
    comment.click()
    comment.send_keys(Keys.CONTROL + 'v')

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
           
        links = [pr_link.get_attribute("href") for pr_link in driver.find_elements(By.XPATH, '//a[@data-hovercard-type="pull_request"]')]
        
        for pr_url in links:
            delay //= 2

            try:
                driver.get(pr_url)
                print(pr_url)

                wait_element('//a[@id="prs-files-anchor-tab"]').click()

                repo = driver.find_element(By.XPATH, '(//a[contains(@class, "PullRequestBranchName")])[2]').get_attribute('href').replace('tree', 'refs/heads').replace('github', 'raw.githubusercontent')
                folder = driver.find_element(By.XPATH, '//span[contains(@class, "PRIVATE_TreeView-item-content-text")]/span').text
                
                repo_url_doc_md = f'{repo}/{folder}/doc.md'
                repo_url_models_py = f'{repo}/{folder}/models.py'
                repo_url_service_py = f'{repo}/{folder}/service.py'
                doc_md = None
                models_py = None
                service_py = None
                review = start_message

                # проверка doc.md
                try:
                    driver.find_element(By.XPATH, '//a[.="doc.md"]')
                    driver.get(repo_url_doc_md)
                    print(repo_url_doc_md)
                    doc_md = driver.find_element(By.XPATH,  '//pre').text
                    promt = ''
                    with open(file='promt.txt', mode='r', encoding='utf-8') as f:
                        promt = ''.join(f.readlines())
                    promt += doc_md
                    review += f'\n\n---\n\n# Проверка doc.md\n\n{send_promt(promt)}'
                except Exception as ex:
                    review += "\n\n---\n\nфайл doc.md не найден"
                            

                # проверка models.py
                if doc_md:
                    try:
                        driver.get(pr_url)
                        wait_element('//a[@id="prs-files-anchor-tab"]').click()
                        driver.find_element(By.XPATH, '//a[.="models.py"]')
                        driver.get(repo_url_models_py)
                        print(repo_url_models_py)
                        models_py = driver.find_element(By.XPATH,  '//pre').text
                        promt = f'Проверь соотвесвие реализации models.py по требованиям из doc.md\n\nФайл `doc.md`\n\n{doc_md}\n\nФайл `models.py`\n\n{models_py}\n\nЕсли есть замечания, коротко напиши их, если замечаний нет, напиши "Замечаний нет"'
                        review += f'\n\n---\n\n# Проверка models.py\n\n{send_promt(promt)}'
                    except Exception as ex:
                        review += "\n\n---\n\nфайл models.py не найден"


                # проверка service.py
                if doc_md and models_py:
                    try:
                        driver.find_element(By.XPATH, '//a[.="service.py"]')
                        driver.get(repo_url_service_py)
                        print(repo_url_service_py)
                        service = driver.find_element(By.XPATH,  '//pre').text
                        promt = f'Проверь соотвесвие реализации service.py по требованиям из doc.md с учётом models.py\n\nФайл `doc.md`\n\n{doc_md}\n\nФайл `models.py`\n\n{models_py}\n\nФайл `service.py`\n\n{service}\n\nЕсли есть замечания, коротко опиши их, если замечаний нет, напиши "Замечаний нет"'
                        review += f'\n\n---\n\n# Проверка service.py\n\n{send_promt(promt)}'
                    except Exception as ex:
                        review += "\n\n---\n\nфайл service.py не найден"

                send_review(pr_url, review)


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