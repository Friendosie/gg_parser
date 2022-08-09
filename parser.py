# Импорты
import requests, time, os
from bs4 import BeautifulSoup
from datetime import datetime

def scrape(link):
    # Юзер Агент
    session = requests.Session()
    ua = {"User-Agent":"Mozilla/5.0 (Linux; Android 11; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"}
    # Проверка на правильность ссылки
    if link.find('https://ggsel.com/catalog/') != -1:
        dir_name = link.replace('https://ggsel.com/catalog/', '')
        # Создаем директории
        try:
            os.mkdir('data')
        except:
            pass
        try:
            os.mkdir(f'data/{dir_name}')
        except:
            pass
        # Получаем "сырую" информацию
        raw_data = session.get(link, headers=ua)
        # Приводим информацию в нормальный вид
        data = BeautifulSoup(raw_data.text, 'lxml')
        # Ищем все предложения
        find_data = data.find_all('div', class_='product-item')
        # Обрабатываем предложения
        count = 0
        for find in find_data:
            count += 1
            # Создаем директории
            try:
                os.mkdir(f'data/{dir_name}/{count}')
            except:
                pass
            full_info = ""
            # Описание товара
            full_info += "Описание: " + (find.find('a', class_='product-item-descr').text)
            # Цена
            prices = (find.find('div', class_='product-price'))
            full_info += "\nЦена: " + (prices.find('span').text)
            # Если есть скидка на товар, записываем
            try:
                full_info += "\nСтарая цена: " + (prices.find(class_='cost-old').text)
                full_info += ("\nСкидка: " + find.find('div', class_='product-item-badge').text).replace('    ', '')
            except:
                pass
            # Ссылка на товар
            full_info += "\nСсылка: " + (find.find('a', class_='prod-link')['href'])
            # Картинка товара
            image = find.find('a', class_='product-item-img lazy')['data-bg']
            image = session.get(image, headers=ua).content
            with open(f'data/{dir_name}/{count}/{count}.png', 'wb') as f:
                f.write(image)
            with open(f'data/{dir_name}/{count}/{count}.txt', 'w') as f:
                f.write(full_info)
            print(f'{count} готово')

link = input('Введите ссылку: ')
scrape(link)