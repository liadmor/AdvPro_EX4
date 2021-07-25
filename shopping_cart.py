from errors import ItemAlreadyExistsError, ItemNotExistError
from item import Item


class ShoppingCart:
    def __init__(self):
        """ initial the shopping cart to new list and make the sum price of the cart to zero """
        self.shop_cart = []
        self.sum_cart = 0

    def add_item(self, item: Item):
        """if the item not in the list, we will add him and update the sum price cart
        :raise ItemAlreadyExistsError"""
        for item1 in self.shop_cart:
            if item.name == item1.name:
                raise ItemAlreadyExistsError
        self.shop_cart.append(item)
        self.sum_cart += item.price

    def remove_item(self, item_name: str):
        """if the item in the list, we will remove him and update the sum price cart
        :raise ItemNotExistError
        :return after finish updating"""
        for item in self.shop_cart:
            if item_name == item.name:
                self.shop_cart.remove(item)
                self.sum_cart -= item.price
                return
        raise ItemNotExistError

    def get_subtotal(self) -> int:
        """:return the sum price cart"""
        return self.sum_cart
