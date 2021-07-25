import yaml

from errors import ItemNotExistError, TooManyMatchesError
from item import Item
from shopping_cart import ShoppingCart


class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    @staticmethod
    def num_tags_in_list(item: Item, list_tag: list):
        """"check how mach item tags are similar to the tags in the list
         :return count of the similar tags"""
        count = 0
        for tags in list_tag:
            if tags in item.hashtags:
                count -= 1
        return count

    def search_in_shop_cart(self, item_name: str):
        """search item in the shop cart
        :return list of all the item that fitting"""
        list_items = []
        for item in self._shopping_cart.shop_cart:
            if item_name in item.name:
                list_items.append(item)
        return list_items

    def search_in_store(self, item_name: str):
        """search item in the store items.
        :return list of all the item that fitting"""
        list_items = []
        for item in self.get_items():
            if item_name in item.name:
                list_items.append(item)
        return list_items


    def search_by_name(self, item_name: str) -> list:
        """save all the items that not in the current sopping cart and have the same name to new item list.
        make a list of all the tags in the current shopping cart
        sort the new list by largest fit tags and after that by name (for the case we have the same num of tags
         :return ans = sorted list as needed"""
        fit_items = []
        for item in self.get_items():
            sub = item_name in item.name
            in_cart = item not in self._shopping_cart.shop_cart
            if sub and in_cart:
                fit_items.append(item)
        tags_curr_shop_cart = []
        for item in self._shopping_cart.shop_cart:
            tags_curr_shop_cart.extend(item.hashtags)
        if len(fit_items) == 0:
            return []
        else:
            return sorted(fit_items, key=lambda item1: (self.num_tags_in_list(item1, tags_curr_shop_cart), item1.name))

    def search_by_hashtag(self, hashtag: str) -> list:
        """save all the items that not in the current sopping cart and have the same hashtags to a new item list.
        make a list of all the tags in the current shopping cart
        sort the new list by largest fit tags and after that by name (for the case we have the samenum of tags
         :return ans = sorted list as needed"""
        fit_items = []
        for item in self.get_items():
            sub = hashtag in item.hashtags
            in_cart = item not in self._shopping_cart.shop_cart
            if sub and in_cart:
                fit_items.append(item)
        tags_curr_shop_cart = []
        for item in self._shopping_cart.shop_cart:
            tags_curr_shop_cart.append(item.hashtags)
        if len(fit_items) == 0:
            return []
        else:
            return sorted(fit_items, key=lambda item1: (self.num_tags_in_list(item1, tags_curr_shop_cart), item1.name))

    def add_item(self, item_name: str):
        """search by name the item in the store
        if the length list is 0 then the item not exist.
        if the length list is 1 then the item in the store and we will add it to the shopping cart (unless he in the
         shipping cart).
        if the length list is more than one item contain the name."""
        item_in_store = self.search_in_store(item_name)
        if len(item_in_store) == 0:
            raise ItemNotExistError
        elif len(item_in_store) == 1:
            self._shopping_cart.add_item(item_in_store[0])
        else:
            raise TooManyMatchesError

    def remove_item(self, item_name: str):
        """search by name the item in the shopping cart
        if the length list is 0 then the item not exist.
        if the length list is 1 then the item in the store and we will remove it from the shopping cart (unless he
        didnt appear in the shipping cart).
        if the length list is more than one item contain the name."""
        item_in_shopping_cart = self.search_in_shop_cart(item_name)
        if len(item_in_shopping_cart) == 0:
            raise ItemNotExistError
        elif len(item_in_shopping_cart) == 1:
            self._shopping_cart.remove_item(item_in_shopping_cart[0].name)
        else:
            raise TooManyMatchesError

    def checkout(self) -> int:
        """sum up all the total payment for the shopping cart"""
        return self._shopping_cart.get_subtotal()
