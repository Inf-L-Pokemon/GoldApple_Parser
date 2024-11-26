from save_to_csv import SaveCSV


def main():
    pages = input('Введите количество страниц для поиска данных в категории парфюмерия\n')
    get_data = SaveCSV(pages)
    get_data.save_csv()


if __name__ == '__main__':
    main()
