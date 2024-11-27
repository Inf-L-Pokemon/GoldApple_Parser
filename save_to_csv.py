import csv

from tqdm import trange

from parser import Parser


class SaveCSV:
    """
    Сохраняет данные по каждому товару в файл расширения csv.
    """

    def __init__(self, pages):
        self.pages = int(pages)
        self.parser = Parser()
        self.headers_csv = ['url', 'name', 'price', 'rating', 'description', 'instruction', 'country']

    def save_csv(self):
        """
        Записывает данные по товару в файл goldapple.csv, находящийся в корневой папке проекта.
        """

        with open("goldapple.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers_csv, delimiter='|')
            writer.writeheader()
            for page in trange(1, self.pages + 1):
                links = self.parser.get_perfumes_links(page=page)
                if not links:
                    break
                for link in links:
                    data_perfume = self.parser.get_perfumes_data(url=link)
                    writer.writerow(data_perfume)
