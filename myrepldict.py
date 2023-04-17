from syncobj import SyncObjConsumer, replicated


def one_byte_hash(s):
    return hash(s) % 256


class MyReplDict(SyncObjConsumer):
    def __init__(self):
        super(MyReplDict, self).__init__()
        self.__data = {}

    @replicated
    def set(self, value):
        key = one_byte_hash(value.encode('utf-8'))
        self.__data[key] = value

    def values(self):
        return self.__data.values()
