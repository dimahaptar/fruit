import sqlite3

connection = sqlite3.connect('store.db')


class Product:
    table_name = 'products'
    fields = ['id', 'name', 'category', 'price', 'quantity', 'created']

    def __init__(self, name=None, category=None, price=None, quantity=None, id=None, created=None):
        self.id = id
        if self.id is not None:
            self.reload()
        else:
            self.name = name
            self.category = category
            self.price = price
            self.quantity = quantity
            self.created = created

    # Аналог предыдущего инита, только в этом случае все аргунменты надо передовать по значение
    # те Product(name="onion"), а не Product("onion")
    # def __init__(self, **kwargs):
    #     for attr, value in kwargs.items():
    #         setattr(self, attr, value)
    #
    #     for field in self.fields:
    #         if not hasattr(self, field):
    #             setattr(self, field, None)

    def save(self):
        """Сохраняем объект в базу. 
        На самом деле INSERT INTO всегда создает новый объект
        
        Если объект уже есть в базе, то его надо переписать (а не создавать новый с тем же именем)
        Для этого изобрели UPDATE команду:: 
        
            UPDATE products
            SET name = ?, category = ?, ...
            WHERE id = ?;
        
        И хотя мы ещё не разбирали этот случай, советую попробовать его реализовать
        """
        connection = sqlite3.connect('store.db')

        if self.id is None:
            result = connection.execute("INSERT INTO products (name, category, price, quantity)\
                                         VALUES (?, ?, ?, ?);",
                                        (self.name, self.category, self.price, self.quantity))
            connection.commit()   # как выяснилось, без этого не работает
            self.id = result.lastrowid
        else:
            connection.execute("UPDATE products\
                                SET name=?, category=?,price=?,quantity=?\
                                WHERE id=?;", (self.name, self.category, self.price, self.quantity, self.id))
            connection.commit()

        self.reload()
        return self

    def reload(self):
        """ Обновляет информацию об объекте на актуальную (из базы).
        Т.е. на случай, если в базе что-то поменялось (изменилась цена)
        """
        # execute в данном случае вернёт курсор, по которому можно итерироваться
        # но т.к. объект только один, можно взять первый элемен при помощи next
        # случай, когда self.id нет, или не существует объекта с такими id здесь не рассматривается,
        # но в вашем классе можно добавить пару проверок
        connection = sqlite3.connect('store.db')

        if self.id is None:
            raise Exception("Object is not in the db so far.")

        data = next(connection.execute("SELECT * FROM products WHERE id = ?;", (self.id,)))
        # data = list(connection.execute("SELECT * FROM products WHERE id = ?;", (self.id, )))[0]

        # распаковка итераторов
        # a, b = data
        self.id, self.name, self.category, self.price, self.quantity, self.created = data

        # можно распокавать возврат функции
        # self.id, self.name, self.category, self.price, self.quantity, self.created = \
        #     next(connection.execute("SELECT * FROM products WHERE id = ?;", (self.id,)))

        # yet another way:
        # for field, value in zip(self.fields, data):
        #     setattr(self, field, value)

        return self

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ", ".join("{}={}".format(field, repr(getattr(self, field)))
                                         for field in self.fields))

    # classmethod делает метод уровня класса, а не объекта
    # те вместо self будет сам класс cls (в нашем случае Product)
    # это позвалает вызвать этот метод Product.select
    @classmethod
    def select(cls):
        connection = sqlite3.connect('store.db')

        result = []
        for row in connection.execute("SELECT * FROM products;"):
            # row - это картеж (tuple)
            # так как мы любим ООП, нам нужен объект класса Product.
            # в данном случае cls равен Product, но всё-таки лучше указать cls
            # почему? - из-за наследования (эта функция будет *коректно* работать и с наследниками класса Product)
            result.append(cls(name=row[1], id=row[0], created=row[5],
                              category=row[2], price=row[3], quantity=row[4]))
            # pythonic way:
            # result.append(cls(**{attr: name for attr, name in zip(cls.fields, row)}))
            # result.append(cls(**dict(zip(cls.fields, row))))
        return result

        # for brave:
        # for row in connection.execute("SELECT * FROM products;"):
        #     yield cls(**{attr: name for attr, name in zip(cls.fields, row)})


    def delete(self):
        """ Этот метод должен удалить запись об этом объекте из базы.
        
        """
        connection = sqlite3.connect('store.db')
        connection.execute("DELETE FROM products WHERE id = ?;", (self.id, ))
        connection.commit()
        self.id = None
        del self


if __name__ == '__main__':
    # Создаем новый объект
    potato = Product(name="Potato", category="food", price="2.10", quantity=10)
    # его ещё нет в базе - поэтому нет и id
    print(potato.id)

    potato.save() # теперь он в базе и получил свой id
    print(potato.id, potato.created)

    print("Теперь в базе есть следующие объекты:")
    print(list(Product.select()))

    # Было бы здорово менять атрибуты объектов
    potato.category = 'tasty food'
    # и сохранять изменения в базу
    print("До:", list(Product.select()))
    potato.save()  # update
    print("После:", list(Product.select()))

    # Да и удалять объекты - тоже хороший навык
    potato.delete()
    print("Теперь:", list(Product.select()))
    print("Объект {} удалён".format(potato))
    # молодцы, что дочитали до конца