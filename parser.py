import requests

from bs4 import BeautifulSoup


class Parser:
    """
    Класс для обработки страницы сайта "Золотое Яблоко" и сбора необходимых данных со страницы.
    """

    def __init__(self):
        self.start_url = 'https://goldapple.ru/parfjumerija'

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        """
        Принимает в качестве аргумента адрес страницы, возвращает объект BeautifulSoup.

        :param url: Адрес страницы
        :return: Объект BeautifulSoup
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        return soup

    def get_perfumes_links(self, page: int) -> list:
        """
        Ищет ссылки на каждый товар со страницы сайта с категорией "Парфюмерия".

        :param page: Номер страницы.
        :return: Список ссылок по каждому товару.
        """

        links = []
        page_url = self.start_url + f'?p={page}'

        def find_data_scroll_id(tag):
            return tag.name == 'div' and tag.has_attr('data-scroll-id')

        soup = self.get_soup(page_url)
        perfumes_data_scroll_id = soup.find_all(find_data_scroll_id)

        for perfume_link in perfumes_data_scroll_id:
            tag_a = perfume_link.find('a')
            if tag_a is not None:
                link = 'https://goldapple.ru/' + tag_a.get('href')
                links.append(link)

        return links

    def get_perfumes_data(self, url: str) -> dict:
        """
        Принимает на вход ссылку на товар, возвращает данные о товаре.

        :param url: Ссылка на товар.
        :return: Данные о товаре
        """

        soup = self.get_soup(url)

        name = soup.find('meta', itemprop='brand')
        name = name.get('content') + ' ' + name.find_next().text.strip()

        price = soup.css.select('meta[itemprop="price"]')
        price = price[0].get('content')

        try:
            rating = soup.css.select('meta[itemprop="ratingValue"]')
            rating = rating[0].get('content')
        except Exception:
            rating = 0

        try:
            description = soup.css.select('div[itemprop="description"]')
            description = description[0].text.strip().replace('\n', ' ')
        except Exception:
            description = 'Описание отсутствует'

        try:
            instruction = soup.css.select('div[text="применение"]')
            instruction = instruction[0].text.strip().replace('\n', ' ')
        except Exception:
            instruction = 'Инструкция отсутствует'

        try:
            country = soup.css.select('div[text="о бренде"]')
            country = country[0].contents[2].text.strip().replace('\n', ' ')
        except Exception:
            country = 'Страна не указана'

        data = {
            'url': url,
            'name': name.replace(chr(160), ' '),
            'price': price,
            'rating': rating,
            'description': description.replace(chr(160), ' '),
            'instruction': instruction.replace(chr(160), ' '),
            'country': country
        }

        return data
