from syncobj import SyncObjConsumer, replicated


def one_byte_hash(s):
    return hash(s) % 256


class MyReplDict(SyncObjConsumer):
    def __init__(self):
        super(MyReplDict, self).__init__()
        self.__data = {}
        self.__lock = {}

    @replicated
    def set(self, key, value):
        self.__lock[key] = True
        self.__data[key] = value
        self.__lock[key] = False

    def values(self):
        return self.__data.values()

    @replicated
    def lock(self, key):
        while self.__lock.get(key, False):
            pass
        self.__lock[key] = True

    @replicated
    def unlock(self, key):
        self.__lock[key] = False
