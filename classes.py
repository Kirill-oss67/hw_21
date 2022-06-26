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
        # user_input = input("Введите запрос :")
        user_input = "Доставить 31 презики из склад в магазин"
        if user_input == 'stop':
            break
        store = Store()
        shop = Shope()
        request = Request(user_input)

        store_items = {
                        'чипсы' : 20,
                       "презики" : 20 ,
                       'печеньки' : 30
                         }
        store.items = store_items
        from_ = store if request.from_ == 'склад' else shop
        to_ = store if request == 'склад' else shop
        print(request.product)
        print(from_.items)
        if request.product in from_.items:
            print(f"нужный товар есть в пункте \'{request.from_}\'")
        else:
            print('пошел на')

        if from_.items[request.product] >= request.amount:
            print('все ок')
        else:
            print(f'пошел на, в пункте \"{request.from_}\" не хватает {request.amount - from_.items[request.product]}')
        break


if __name__ == "__main__":
    main()
