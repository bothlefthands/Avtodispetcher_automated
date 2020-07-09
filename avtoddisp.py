from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep



PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)
try:
    # 1st task: Пользователь заходит на сайт Яндекс: www.yandex.ru
    driver.get('https://yandex.ru')

    # 2nd task: Вводит в поисковую строку фразу «расчет расстояний между городами» и запускает поиск
    search_string = 'расчет расстояний между городами'
    search_field = driver.find_element_by_id('text')
    search_field.send_keys(search_string)
    search_field.send_keys(Keys.ENTER)

    # 3rd task: Среди результатов поиска пользователь ищет результат с сайта «avtodispetcher.ru»
    desired_result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'avtodispetcher.ru'))
    )

    # 4th task: Найдя нужный результат с этого сайта – пользователь кликает на данном результате и переходит на сайт
    desired_result.click()
    driver.switch_to.window(driver.window_handles[-1])

    # 5th task: Убедившись, что открылась верная ссылка,
    print(driver.current_url)
    # assert driver.current_url == 'https://www.avtodispetcher.ru/distance/'
    if driver.current_url != 'https://www.avtodispetcher.ru/distance/':
        raise Exception('Check current url!')

    # Пользователь вводит следующие значения в поля:
    def find_and_fill(name, value):
        """
        Функция
        1. Ждет появления формы с именем 'name' на странице
        2. Заполняет форму значением 'value'
        """
        field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, name))
        )
        field.clear()
        field.send_keys(value)

    find_and_fill('from', 'Тула')
    find_and_fill('to', 'Санкт-Петербург')
    find_and_fill('fc', '9')
    find_and_fill('fp', '46')

    # 6th task: Пользователь нажимает кнопку «Рассчитать»
    driver.find_element_by_class_name('submit_button').click()

    # 7th task: Пользователь проверяет что рассчитанное расстояние = 897 км, а стоимость топлива = 3726 руб.
    total_distance = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'totalDistance'))).text)
    total_fuel_price = int(driver.find_element_by_xpath('//*[@id="summaryContainer"]/form/p').text.split(' ')[-2])
    print(total_distance)
    print(total_fuel_price)

    if total_fuel_price != 3726 or total_distance != 897:
        raise Exception('Check fuel price and distance for the first case!')

    # 8th task: Пользователь кликает на «Изменить маршрут»
    driver.find_element_by_id('triggerFormD').click()

    # 9th task: В открывшейся форме в поле «Через города» вводит «Великий Новгород»
    find_and_fill('v', 'Великий Новгород')

    # 10th task: Ждет минуту и снова нажимает «Рассчитать»
    sleep(60)
    submit_button = driver.find_element_by_xpath('//*[@id="CalculatorForm"]/div[2]/input')
    submit_button.location_once_scrolled_into_view
    submit_button.click()

    # 11th task: Пользователь проверяет что расстояние теперь = 966 км, а стоимость топлива = 4002 руб
    total_distance = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'totalDistance'))).text)
    total_fuel_price = int(driver.find_element_by_xpath('//*[@id="summaryContainer"]/form/p').text.split(' ')[-2])
    print(total_distance)
    print(total_fuel_price)

    if total_fuel_price != 4002 or total_distance != 966:
        raise Exception('Check fuel price and distance for the second case!')


except Exception as e:
    print(e)

finally:
    driver.quit()


