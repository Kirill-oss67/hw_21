from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, items, company):
        self.items = items
        self.company = company

    @abstractmethod
    def add(self, title, count):
        pass

    @abstractmethod
    def remove(self, title, count):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title, count):
        if title in self._items:
            self._items[title] += count
        else:
            self._items[title] = count
        self._capacity -= count

    def remove(self, title, count):
        res = self._items[title] - count
        if res > 0:
            self._items[title] = res
        else:
            del self._items[title]
        self._capacity += count

    @property
    def get_free_space(self):
        return self._capacity

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items
        self._capacity -= sum(self._items.values())

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())


class Shope(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20


class Request:
    def __init__(self, info):
        self.info = self._split_info(info)
        self.from_ = self.info[4]
        self.to_ = self.info[6]
        self.amount = int(self.info[1])
        self.product = self.info[2]

    @staticmethod
    def _split_info(info):
        return info.split(" ")

    def __repr__(self):
        return f"Доставить {self.amount} {self.product} из {self.from_} в {self.to_}"


def main():
    while (True):
        user_input = input("Введите запрос :")

        if user_input == 'stop':
            break

        request = Request(user_input)

        from_ = store if request.from_ == 'склад' else shop
        to_ = store if request.to_ == 'склад' else shop

        if request.product in from_.items:
            print(f"нужный товар есть в пункте \'{request.from_}\'")
        else:
            print(f'в пункте {request.from_} нет такого товара ')
            continue

        if from_.items[request.product] >= request.amount:
            print(f"нужное колличество есть в пункте'{request.from_}\'")
        else:
            print(f'В пункте \"{request.from_}\" не хватает {request.amount - from_.items[request.product]}')
            continue
        if to_.get_free_space >= request.amount:
            print(f"В пункте \'{request.to_}\' достаточно места ")
        else:
            print(f"В пункте {request.to_} не хватает {request.amount - to_.get_free_space} места ")
            continue
        if request.to_ == 'магазин' and to_.get_unique_items_count == 5 and request.product not in to_.items:
            print("В магазине достаточно уникальных значений")
            continue
        from_.remove(request.product, request.amount)
        print(f"Курьер забрал {request.amount} {request.product} из пункта {request.from_}")
        print(f"Курьер везет {request.amount} {request.product} из пункта {request.from_} в пункт {request.to_}")
        to_.add(request.product, request.amount)
        print(f"Курьер доставил {request.amount} {request.product} в пункт {request.to_}")
        print('='*30)
        print('На складе :')
        for title, count in store.items.items():
            print(f"{title} : {count}")
        print(f'Свободного места {store.get_free_space}')
        print('=' * 30)
        print('В магазине :')
        for title, count in shop.items.items():
            print(f"{title} : {count}")
        print(f'Свободного места {shop.get_free_space}')
        print('=' * 30)


if __name__ == "__main__":
    store = Store()
    shop = Shope()

    store_items = {
        'чипсы': 20,
        "сок": 20,
        'печеньки': 38
    }
    store.items = store_items
    main()

#Доставить 3 печеньки из склад в магазин