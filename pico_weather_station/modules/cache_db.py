class CacheDB:
    def __init__(self):
        self.__db = {}

    def read_all(self):
        return self.__db

    def read(self, key: str):
        return self.__db.get(str(key))

    def write(self, key: str, value):
        self.__db[str(key)] = value

    def delete(self, key: str):
        if self.__db.get(str(key)) is not None:
            del self.__db[str(key)]

    def get_key_by_prefix(self, prefix: str) -> str:
        search_key = None

        for key in self.__db.keys():
            if str(key).startswith(prefix):
                search_key = key
                break

        return search_key
