import time
import traceback
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Автоматически скачивает и настраивает ChromeDriver
service_py = Service(ChromeDriverManager().install())

options = Options()
# options.page_load_strategy = "eager"
driver = webdriver.Chrome(service=service_py, options=options)
driver.maximize_window()
driver.implicitly_wait(5)
delay = 2

start_message = (
    '# Проверьте требования, они были переписаны так, что бы ваши нейросети их понимали!!!\n\n'
    '## Если вы считаете требования противоречивыми, напишите об этом.\n\n'
    'Это отзыв ИИ которая проверяет только соответсвие `Требованиями к УП`. '
    'Если у ИИ есть какие-то замечания, то это не значит что так и есть. '
    'Вы должны убедиться что в этом месте у Вас написано верно, это поможет вам сократить время ожидании проверки вашей работы на занятии. '
)

requirements_5_md_url = 'https://raw.githubusercontent.com/YuriSilenok/AI/refs/heads/main/requirements_5.md'
requirements_4_md_url = 'https://raw.githubusercontent.com/YuriSilenok/AI/refs/heads/main/requirements_4.md'
requirements_3_md_url = 'https://raw.githubusercontent.com/YuriSilenok/AI/refs/heads/main/requirements_3.md'


def wait_element(xpath: str):
        for _ in range(20):
            try:
                element = driver.find_element(By.XPATH, xpath)
                # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                ActionChains(driver).move_to_element(element).perform()
                return element
            except:
                print(f'Элемент не найден {xpath}')

def get_content(url: str):
    print(url)
    driver.get(url)
    time.sleep(delay)
    content = driver.find_element(By.XPATH,  '//pre').text
    if "404: Not Found" != content:
        return content


def send_promt(promts:tuple[str]):
    # driver.get("https://giga.chat")
    driver.get("https://alice.yandex.ru/")
    time.sleep(delay)
    for promt in promts:
        textarea = wait_element('//textarea')
        textarea.click()
        # print(f"\n\n{promt}\n\n")
        pyperclip.copy(promt)
        textarea.send_keys(Keys.CONTROL + 'v')
        textarea.send_keys(Keys.ENTER)
        print('Промт отправлен')
        time.sleep(delay)
        # wait_element('//button[@id="call-button"]')
        wait_element('//button[@id="oknyx-button" and @aria-label="Алиса, начни слушать"]')
        
    # wait_element('(//button[@data-da_name="MessageCopyButton"])[last()]').click()
    
    wait_element('(//button[@aria-label="Копировать"])[last()]').send_keys(Keys.END)
    wait_element('(//button[@aria-label="Копировать"])[last()]').click()
    time.sleep(delay)
    print('Ответ на промт получен')
    return pyperclip.paste()

def send_review(pr_url: str, text: str):
    driver.get(pr_url)
    time.sleep(delay)
    driver.find_element(By.XPATH, '//a[@id="prs-files-anchor-tab"]').click()
    driver.find_element(By.XPATH, '//button[.//span[contains(., "Submit")]]').click()
    driver.find_element(By.XPATH, '//label[span[.="Request changes"]]').click()
    comment = driver.find_element(By.XPATH, '//textarea[@placeholder="Leave a comment"]')
    comment.click()
    comment.send_keys(Keys.CONTROL + 'a')
    comment.send_keys(Keys.BACKSPACE)
    pyperclip.copy(text)
    comment.send_keys(Keys.CONTROL + 'v')
    time.sleep(delay)
    driver.find_element(By.XPATH, '(//div[button[.//span[.="Cancel"]]]//button)[2]').click()
    wait_element('//button[@data-comment-text="Close with comment"]')
    print('Проверка отправлена')
    time.sleep(delay*2)

try:
    
    driver.get("https://github.com/pulls?q=is%3Aopen+is%3Apr+review-requested%3AYuriSilenok+archived%3Afalse+sort%3Aupdated-asc")
    time.sleep(delay)
    driver.find_element(By.XPATH, '//input[@id="login_field"]').send_keys('YuriSilenok')
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys('a1501274296')
    driver.find_element(By.XPATH, '//input[@value="Sign in"]').click()
    driver.find_element(By.XPATH, '//button[@data-disable-with="More options…"]').click()
    driver.find_element(By.XPATH, '//span/span/span[.="GitHub Mobile"]').click()
    time.sleep(delay)
    
    wait_element('//a[@title="Pull requests requesting your review"]')

    # driver.get("https://chat.deepseek.com/sign_in")
    # driver.find_element(By.XPATH, '//input[@placeholder="Номер телефона / адрес электронной почты"]').send_keys('yuri.silenok@gmail.com')
    # driver.find_element(By.XPATH, '//input[@placeholder="Пароль"]').send_keys('a2195966')
    # driver.find_element(By.XPATH, '//div[span[.="Войти"]]').click()
    # time.sleep(delay)


    wait = 30
    while True:
        requirements_3_md = get_content(requirements_3_md_url)
        requirements_4_md = get_content(requirements_4_md_url)
        requirements_5_md = get_content(requirements_5_md_url)
            
        driver.get("https://github.com/pulls?q=is%3Aopen+is%3Apr+review-requested%3AYuriSilenok+archived%3Afalse+sort%3Aupdated-asc")
        time.sleep(delay)


        links = [pr_link.get_attribute("href") for pr_link in driver.find_elements(By.XPATH, '//a[@data-hovercard-type="pull_request"]')]
        for pr_url in links:
            wait //= 2

            try:
                print(pr_url)
                driver.get(pr_url)
                time.sleep(delay)

                wait_element('//a[@id="prs-files-anchor-tab"]').click()

                repo = driver.find_element(
                    By.XPATH, '(//a[contains(@class, "PullRequestBranchName")])[2]').get_attribute(
                        'href').replace('tree', 'refs/heads').replace('github', 'raw.githubusercontent')
                folder = driver.find_element(By.XPATH, '//span[contains(@class, "PRIVATE_TreeView-item-content-text")]/span').text
                
                repo_url_doc_md = f'{repo}/{folder}/doc.md'
                repo_url_models_py = f'{repo}/{folder}/models.py'
                repo_url_service_py = f'{repo}/{folder}/service.py'
                repo_url_client_py = f'{repo}/{folder}/client.py'
                doc_md = get_content(repo_url_doc_md)
                models_py = get_content(repo_url_models_py)
                service_py = get_content(repo_url_service_py)
                client_py = get_content(repo_url_client_py)
                review = start_message

                # проверка doc.md
                if doc_md:
                    try:
                        promt = (
                            f'Прочитай требования на оценку 3\n\n{requirements_3_md}'
                            '\n\nНиже представлен текст файла `doc.md`, проверь его на соответсвия требованиям. '
                            '\nЕсли есть замечания, коротко напиши их без рекомендаций, если замечаний нет, напиши "Замечаний нет"'
                            f'\n\n{doc_md}'
                        ),
                        review += f'\n\n---\n\n# Проверка doc.md\n\n{send_promt(promt)}'
                    except Exception as ex:
                        review += f"\n\n---\n\nОшибка при проверке `doc.md`\n\n{traceback.format_exc()}"
                else:
                    review += f"\n\n---\n\nФайл `doc.md` не найден"
                        

                # проверка models.py
                if doc_md and models_py:
                    try:
                        promt = (
                            f'Прочитай требования на оценку 3\n\n{requirements_3_md}\n\n и документацию в файле `doc.md`\n\n{doc_md}'
                            '\n\nНиже представлен текст файла `models.py`, проверь его на соответсвия требованиям  и `doc.md`. '
                            '\nЕсли есть замечания, коротко напиши их без рекомендаций, если замечаний нет, напиши "Замечаний нет"'
                            f'\n\nФайл `models.py`\n\n```\n{models_py}\n```'
                        ),
                        review += f'\n\n---\n\n# Проверка models.py\n\n{send_promt(promt)}'
                    except Exception as ex:
                        review += f"\n\n---\n\nОшибка при проверке `models.py`\n\n{traceback.format_exc()}"
                else:
                    review += f"\n\n---\n\nФайл `models.py` не найден"


                # проверка service.py
                if doc_md and models_py and service_py:
                    try:
                        promt = (
                            f'Прочитай требования на оценку 4\n\n{requirements_4_md}\n\n'
                            f'и документацию в файле `doc.md`\n\n{doc_md}\n\nи файл `models.py`\n\n```\n{models_py}\n```'
                            '\n\nНиже представлен текст файла `service.py`, проверь его на соответсвия требованиям, `doc.md`,  `models.py`.'
                            '\nЕсли есть замечания, коротко напиши их без рекомендаций, если замечаний нет, напиши "Замечаний нет"'
                            f'\n\nФайл `service.py`\n\n```\n{service_py}\n```'
                        ),
                        review += f'\n\n---\n\n# Проверка service.py\n\n{send_promt(promt)}'
                    except Exception as ex:
                        review += f"\n\n---\n\nОшибка при проверке `service.py`\n\n{traceback.format_exc()}"
                else:
                    review += f"\n\n---\n\nФайл `service.py` не найден"
            

                # проверка client.py
                if doc_md and models_py and service_py and client_py:
                    try:
                        promt = (
                            f'Прочитай требования на оценку 5\n\n{requirements_5_md}\n\n'
                            f'и документацию в файле `doc.md`\n\n{doc_md}\n\nи файл `service.py`\n\n```\n{service_py}\n```'
                            '\n\nНиже представлен текст файла `client.py`, проверь его на соответсвия требованиям, `doc.md`,  `service.py`.'
                            '\nЕсли есть замечания, коротко напиши их без рекомендаций, если замечаний нет, напиши "Замечаний нет"'
                            f'\n\nФайл `client.py`\n\n```\n{client_py}\n```'
                        ),
                        review += f'\n\n---\n\n# Проверка client.py\n\n{send_promt(promt)}'
                    except Exception as ex:
                        review += f"\n\n---\n\nОшибка при проверке `client.py`\n\n{traceback.format_exc()}"
                else:
                    review += f"\n\n---\n\nФайл `client.py` не найден"




                print(review)
                send_review(pr_url, review)


            except Exception as ex:
                print(pr_url, '\n', traceback.format_exc())

        wait += 1
        print('wait', wait)
        time.sleep(wait)
    
finally:
    driver.quit()
    time.sleep(3)
    print("Браузер закрыт.")
