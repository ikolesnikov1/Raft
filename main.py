import random
import sys
import time
from syncobj import SyncObj
from myrepldict import MyReplDict

sys.path.append("../")

if __name__ == '__main__':
    nodes = [
        '127.0.0.1:4321',
        '127.0.0.1:4322',
        '127.0.0.1:4323',
    ]

    dict1 = MyReplDict()

    syncObjs = [
        SyncObj(node, nodes, consumers=[dict1])
        for node in nodes
    ]

    while True:
        time.sleep(2)
        for syncObj in syncObjs:
            print(f"{syncObj.selfNode.id}: ", dict1.values())
            print("Other nodes: ")
            for n in syncObj.otherNodes:
                print(f"{n.id}")
            print()

        dict1.lock("mutex_key", sync=True)
        dict1.set(f'testValue_{random.randint(1, 100)}')
        dict1.unlock("mutex_key", sync=True)
