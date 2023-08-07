from datetime import datetime
import colorama as color
import sqlalchemy as sq
from models import *
from sqlalchemy.orm import sessionmaker

def add_brand():
    try:
        brand_name = str(input('Введите название нового бренда: ')).capitalize()
        query = str(input(f'Вы хотите добавить бренд {brand_name}, верно? ')).capitalize()
        if query == "Да" or query == "":
            brand = Brand(brand_name=brand_name)
            session.add(brand)
            session.commit()
    except sq.exc.IntegrityError:
        print(color.Fore.RED + 'Данный бренд уже существует')
        session.rollback()
    except:
        print(color.Fore.RED + 'Возникла непредвиденная ошибка, попробуйте еще раз')


def add_sex():
    try:
        sex_name = str(input('Введите название нового пола: ')).capitalize()
        query = str(input(f'Вы хотите добавить пол {sex_name}, верно? ')).capitalize()
        if query == "Да" or query == "":
            sex = Sex(sex_name=sex_name)
            session.add(sex)
            session.commit()
    except sq.exc.IntegrityError:
        print(color.Fore.RED + 'Данный пол уже существует')
        session.rollback()
    except:
        print(color.Fore.RED + 'Возникла непредвиденная ошибка, попробуйте еще раз')

def add_size():
    try:
        size_name = str(input('Введите название нового размера: ')).upper()
        query = str(input(f'Вы хотите добавить размер {size_name}, верно? ')).capitalize()
        if query == "Да" or query == "":
            size = Size(size_name=size_name)
            session.add(size)
            session.commit()
    except sq.exc.IntegrityError:
        print(color.Fore.RED + 'Данный размер уже существует')
        session.rollback()
    except:
        print(color.Fore.RED + 'Возникла непредвиденная ошибка, попробуйте еще раз')

def add_category():
    try:
        name = str(input('Введите название новой категории: ')).capitalize()
        sex_id_or_name = str(input('Введите айди или пол: ')).capitalize()
        marginality_percent = int(input('Введите процент маржинальности: '))
        if sex_id_or_name.isdigit():
            sex = sex_id_or_name
        else:
            sex = session.query(Sex.sex_id).select_from(Sex).filter(Sex.sex_name == sex_id_or_name).scalar_subquery()
        sex_id = session.query(Sex.sex_name).select_from(Sex).filter(Sex.sex_id == sex).all()
        session.commit()
        query = str(input(f'Вы хотите добавить категорию с:\n названием "{name}"\n полом "{sex_id[0][0]}" \n процентом маржинальности {marginality_percent}% \nВерно? ')).capitalize()
        if query == "Да" or query == "":   
            category = Category(category_name=name, sex_id=sex, marginality_percent=marginality_percent)
            session.add(category)
            session.commit()
    except sq.exc.IntegrityError:
        print(color.Fore.RED + 'Данная категория уже существует')
        session.rollback()
    except:
        print(color.Fore.RED + 'Возникла непредвиденная ошибка, попробуйте еще раз')

def add_item(receive_price):
    try:
        article = int(input('Введите артикул товара: '))
        item_name = str(input('Введите название товара: ')).capitalize()
        if_name_in_db = session.query(Storage.item_id).select_from(Storage).all()
        session.commit()
        if article in if_name_in_db:
            amount = str(input('Введите количество единиц добавляемого товара: '))
            amount_in_db = session.query(Storage.amount_left).select_from(Storage).filter(Storage.item_id == article)
            final_amount = amount + amount_in_db
        else:
            final_amount = str(input('Введите количество единиц добавляемого товара: '))
        brand_id_or_name = str(input('Введите айди или бренд: ')).capitalize()
        if brand_id_or_name.isdigit():
            brand = brand_id_or_name
        else:
            brand = session.query(Brand.brand_id).select_from(Brand).filter(Brand.brand_name == brand_id_or_name).scalar_subquery()
        category_id_or_name = str(input('Введите айди или категорию: ')).capitalize()
        if category_id_or_name.isdigit():
            category = category_id_or_name
        else:
            category = session.query(Category.category_id).select_from(Category).filter(Category.category_name == category_id_or_name).scalar_subquery()
        size_id_or_name = str(input('Введите айди или размер: ')).capitalize()
        if size_id_or_name.isdigit():
            size = size_id_or_name
        else:
            size = session.query(Size.size_id).select_from(Size).filter(Size.size_name == size_id_or_name).scalar_subquery()
        receive_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        marged_price = session.query(Category.marginality_percent).select_from(Category).filter(Category.category_id == category).all()
        session.commit()
        result = 0.01 * marged_price[0][0]
        sale_price = int(receive_price) * int(result) + int(receive_price)
        pottential_revenue = int(sale_price) - int(receive_price)
        fact_marginality_percent = int(sale_price) / int(receive_price) * 100 - 100
        brand_id = session.query(Brand.brand_name).select_from(Brand).filter(Brand.brand_id == brand).all()
        category_id = session.query(Category.category_name).select_from(Category).filter(Category.category_id == category).all()
        size_id = session.query(Size.size_name).select_from(Size).filter(Size.size_id == size).all()
        session.commit()
        query = str(input(f'Вы хотите добавить товар с:\n артикулом {article}\n названием {item_name}\n брендом {brand_id}\n категорией {category_id}\n размером {size_id}\n датой принятия {receive_datetime}\n ценой принятия {receive_price}\n ценой продажи {sale_price}\n потенциальной выгодой {pottential_revenue}\n фактическим процнетом маржинальности {fact_marginality_percent}\n количеством {final_amount}\nВерно?'))
        if query == "Да" or query == "":
            item_for_sell = Sold_items(item_id=article, item_name=item_name, brand_id=brand, category_id=category, size_id=size, receive_datetime=receive_datetime, receive_price=receive_price, sale_price=sale_price, pottential_revenue=pottential_revenue,  fact_marginality_percent=fact_marginality_percent)
            storage = Storage(item_id=article, amount_left=final_amount)
            session.add(storage)
            session.add(item_for_sell)
            session.commit()
    except sq.exc.IntegrityError:
        print(color.Fore.RED + 'Данный артикул уже существует')
        session.rollback()
    except:
        print(color.Fore.RED + 'Возникла непредвиденная ошибка, попробуйте еще раз')

def sell_item():
    try:
        item_id_or_name = str(input('Введите айди или название товара: ')).capitalize()
        if item_id_or_name.isdigit():
            item = item_id_or_name
        else:
            item = session.query(Sold_items.item_id).select_from(Sold_items).filter(Sold_items.item_name == item_id_or_name).scalar_subquery()
        selling_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        amount_sold = int(input('Введите количество продаваемых товаров: '))
        amount_in_db = session.query(Storage.amount_left).select_from(Storage).filter(Storage.item_id == item).all()
        session.commit()
        amount_in_db = amount_in_db[0][0]
        final_amount = amount_in_db - amount_sold
        item_name = session.query(Sold_items.item_name).select_from(Sold_items).filter(Sold_items.item_id == item).all()
        session.commit()
        query = str(input(f"Вы хотите продать:\n товар {item_name}\n в {selling_datetime}\n в количестве {amount_sold} штук \nВерно?"))
        if final_amount == 0:
            session.query(Storage).filter(Storage.item_id == item).delete()
            sell = Sells(item_id=item, selling_datetime=selling_datetime, amount_sold=amount_sold)
            session.add(sell)
            session.commit()
        elif final_amount < 0:
            print('Товаров на скалде меньше, чем количество в продаже')
        else:
            session.query(Storage).filter(Storage.item_id == item).update({'amount_left' : final_amount})
            sell = Sells(item_id=item, selling_datetime=selling_datetime, amount_sold=amount_sold)
            session.add(sell)
            session.commit()
    except IndexError:
        print(color.Fore.RED + 'Данного товара не существует')
        session.rollback()
    except:
        print(color.Fore.RED + 'Возникла непредвиденная ошибка, попробуйте еще раз')

def choose_option():
    while True:
        comment = str(input('Выберите необходимую функцию: 1 - для добавления бренда, 2 - для добавления пола, 3 - для добавления размера, 4 - для добавления категории, 5 - для добавления вещи на склад, 6 - для регитсрации продажи, 7 - для выхода из программы: '))
        if comment == '1':
            while True:
                add_brand()
                add_more = str(input('Добавить еще один бренд? Напечатайте "No" или "Нет" для выхода из функции: '))
                if add_more.capitalize() == 'No' or add_more.capitalize() == 'Нет':
                    break
        if comment == '2':
            while True:
                add_sex()
                add_more = str(input('Добавить еще один пол? Напечатайте "No" или "Нет" для выхода из функции: '))
                if add_more.capitalize() == 'No' or add_more.capitalize() == 'Нет':
                    break
        if comment == '3':
            while True:
                add_size()
                add_more = str(input('Добавить еще один размер? Напечатайте "No" или "Нет" для выхода из функции: '))
                if add_more.capitalize() == 'No' or add_more.capitalize() == 'Нет':
                    break
        if comment == '4':
            while True:
                add_category()
                add_more = str(input('Добавить еще одну категорию? Напечатайте "No" или "Нет" для выхода из функции: '))
                if add_more.capitalize() == 'No' or add_more.capitalize() == 'Нет':
                    break
        if comment == '5':
            receive_price = str(input('Введите закупочную цену: '))
            while True:
                add_item(receive_price)
                add_more = str(input('Добавить еще один предмет? Напечатайте "No" или "Нет" для выхода из функции: '))
                if add_more.capitalize() == 'No' or add_more.capitalize() == 'Нет':
                    break
        if comment == '6':
            while True:
                sell_item()
                add_more = str(input('Продать еще один предмет? Напечатайте "No" или "Нет" для выхода из функции: '))
                if add_more.capitalize() == 'No' or add_more.capitalize() == 'Нет':
                    break
        if comment == '7':
            break

if __name__ == '__main__':
    DNS = 'postgresql://ADMIN:12345678@localhost:5432/database_name'
    DNS = 'postgresql://postgres:12345678@localhost:5432/database_name'
    engine = sq.create_engine(DNS, pool_size=20)
    Session = sessionmaker(bind=engine)
    session = Session()
    color.init(autoreset=True)
    choose_option()
    session.close()
