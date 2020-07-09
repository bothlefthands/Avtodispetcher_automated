import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class AvtoDisp(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')
        self.driver.get('https://yandex.ru')

        # 2nd task: Вводит в поисковую строку фразу «расчет расстояний между городами» и запускает поиск
        search_string = 'расчет расстояний между городами'
        search_field = self.driver.find_element_by_id('text')
        search_field.send_keys(search_string)
        search_field.send_keys(Keys.ENTER)

        # 3rd task: Среди результатов поиска пользователь ищет результат с сайта «avtodispetcher.ru»
        desired_result = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'avtodispetcher.ru'))
        )

        # 4th task: Найдя нужный результат с этого сайта – пользователь кликает на данном результате и переходит на сайт
        desired_result.click()

        # Переключаем активную вкладку
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def test_page_url(self):
        """Проверяем, открылась ли нужная ссылка"""
        assert self.driver.current_url == 'https://www.avtodispetcher.ru/distance/'

    def test_first_case_numbers(self):
        """Проверяем дистанцию и стоимость бензина для первого случая"""

        # 5th task: Пользователь вводит следующие значения в поля:
        def find_and_fill(name, value):
            """
            Функция
            1. Ждет появления формы с именем 'name' на странице
            2. Очищает форму, если там уже было значение
            3. Заполняет форму значением 'value'
            """
            # 1
            field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, name))
            )
            # 2
            field.clear()
            # 3
            field.send_keys(value)

        find_and_fill('from', 'Тула')
        find_and_fill('to', 'Санкт-Петербург')
        find_and_fill('fc', '9')
        find_and_fill('fp', '46')

        # 6th task: Пользователь нажимает кнопку «Рассчитать»
        self.driver.find_element_by_class_name('submit_button').click()

        # 7th task: Пользователь проверяет что рассчитанное расстояние = 897 км, а стоимость топлива = 3726 руб.
        total_distance = int(
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'totalDistance'))).text
        )
        total_fuel_price = int(
            self.driver.find_element_by_xpath('//*[@id="summaryContainer"]/form/p').text.split(' ')[-2]
        )
        assert total_fuel_price == 3726 or total_distance == 897

    def test_second_case_numbers(self):
        """Проверяем дистанцию и стоимость бензина для второго случая"""

        # 5th task: Пользователь вводит следующие значения в поля:
        def find_and_fill(name, value):
            """
            Функция
            1. Ждет появления формы с именем 'name' на странице
            2. Очищает форму, если там уже было значение
            3. Заполняет форму значением 'value'
            """
            # 1
            field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, name))
            )
            # 2
            field.clear()
            # 3
            field.send_keys(value)

        find_and_fill('from', 'Тула')
        find_and_fill('to', 'Санкт-Петербург')
        find_and_fill('fc', '9')
        find_and_fill('fp', '46')

        # 6th task: Пользователь нажимает кнопку «Рассчитать»
        self.driver.find_element_by_class_name('submit_button').click()

        # 7th task: Пользователь проверяет что рассчитанное расстояние = 897 км, а стоимость топлива = 3726 руб.
        total_distance = int(
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'totalDistance'))).text
        )
        total_fuel_price = int(
            self.driver.find_element_by_xpath('//*[@id="summaryContainer"]/form/p').text.split(' ')[-2]
        )


        # 8th task: Пользователь кликает на «Изменить маршрут»
        self.driver.find_element_by_id('triggerFormD').click()

        # 9th task: В открывшейся форме в поле «Через города» вводит «Великий Новгород»
        find_and_fill('v', 'Великий Новгород')

        # 10th task: Ждет минуту и снова нажимает «Рассчитать»
        sleep(60)
        submit_button = self.driver.find_element_by_xpath('//*[@id="CalculatorForm"]/div[2]/input')
        submit_button.location_once_scrolled_into_view
        submit_button.click()

        # 11th task: Пользователь проверяет что расстояние теперь = 966 км, а стоимость топлива = 4002 руб
        total_distance = int(
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'totalDistance'))).text
        )
        total_fuel_price = int(
            self.driver.find_element_by_xpath('//*[@id="summaryContainer"]/form/p').text.split(' ')[-2]
        )
        assert total_fuel_price == 4002 or total_distance == 966

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
