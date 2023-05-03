from syncobj import SyncObjConsumer, replicated
import threading
import time


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
        self.__data[one_byte_hash(value)] = value
        self.__lock[key] = False

    def values(self):
        return self.__data.values()

    @replicated
    def lock(self, key):
        if self.__lock.get(key, False):
            return False

        self.__lock[key] = True

        timeout_thread = threading.Thread(target=self.__timeout_handler, args=(key,))
        timeout_thread.start()

        return True

    def unlock(self, key):
        self.__lock[key] = False

    def __timeout_handler(self, key):
        time.sleep(300)

        if self.__lock.get(key, False):
            self.__lock[key] = False
