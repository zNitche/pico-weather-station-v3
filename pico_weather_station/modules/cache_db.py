class CacheDB:
    def __init__(self):
        self.__db = {}

    def read_all(self):
        return self.__db

    def read(self, key: str):
        return self.__db.get(key)

    def write(self, key: str, value):
        self.__db[key] = value

    def delete(self, key: str):
        if self.__db.get(key) is not None:
            del self.__db[key]

    def get_key_by_prefix(self, prefix: str) -> str:
        search_key = None

        for key in self.__db.keys():
            if key.startswith(prefix):
                search_key = key
                break

        return search_key

    def update(self, key: str, value_key: str, value):
        """can be applied only to dict type db entries"""
        current_data = self.__db.get(key)

        if current_data is None:
            current_data = {value_key: value}
        else:
            current_data[value_key] = value

        self.write(key, current_data)
