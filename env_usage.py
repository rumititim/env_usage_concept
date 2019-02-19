
import time
from datetime import datetime



class Env():
    def __init__(self, name):
        self.name = name
        self.is_free = True
        self.order = None
        self.queue = None

    def tick(self):
        if self.is_free:
            self.get_order_from_queue()
        else:
            self.process_order()

    def get_order_from_queue(self):
        if self.is_free:
            self.order = self.queue.deque(self.name)
            if self.order:
                self.is_free = False
                self.order.start()
                

    def process_order(self):
        if not self.is_free:
            self.order.count_fact_duration()
            print('{0}: time left: {1}'.format(self.name, self.order.coun_time_left()))
            if self.order.if_order_finished():
                self.order = None
                self.is_free = True
                print("{0}: I removed order, I'm free".format(self.name))

    def register_queue(self, queue):
        self.queue = queue

class Queue():
    def __init__(self):
        self.items = []

    def enque(self, item):
        self.items.append(item)

    def deque(self, env):
        if self.items:
            i = 0
            count = len(self.items)
            while i < count:
                
                if env in self.items[i].envs:
                    print('I was removed from queue: {0} by {1}'.format(env, self.items[i].user))
                    return self.items.pop(i)
                i += 1
            return None
        

    def status(self):
        print('Queue status:')
        for item in self.items:
            print("Order for {} by {}".format(item.envs, item.user))

class Order():
    def __init__(self, envs, user, ordered_duration):
        self.envs = envs
        self.user = user
        self.ordered_duration = ordered_duration
        self.fact_duration = None
        self.start_time = None
        self.registration_time = datetime.now()

    def start(self):
        self.start_time = datetime.now()

    def count_fact_duration(self):
        self.fact_duration = datetime.now() - self.start_time

    def coun_time_left(self):
        return self.ordered_duration - self.fact_duration.seconds

    def if_order_finished(self):
        if self.fact_duration.seconds > self.ordered_duration:
            return True
        else:
            return False

if __name__ == "__main__":
    
    #Test data
    dev1 = Env('dev1')
    dev2 = Env('dev2')
    devs = [dev1, dev2]
    
    user1 = 'user1'
    user2 = 'user2'
    user3 = 'user3'
    user4 = 'user4'
    user5 = 'user5'
    user6 = 'user6'
    user7 = 'user7'
    user8 = 'user8'
    user9 = 'user9'

    queue = Queue()
    queue.enque(Order(['dev1'],user1, 1))
    queue.enque(Order(['dev1'],user2, 1))
    queue.enque(Order(['dev1'],user3, 1))
    queue.enque(Order(['dev1', 'dev2'],user4, 1))
    queue.enque(Order(['dev1'],user5, 1))
    queue.enque(Order(['dev1'],user6, 1))
    queue.enque(Order(['dev2'],user7, 1))
    queue.enque(Order(['dev2', 'dev1'],user8, 1))
    queue.enque(Order(['dev1'],user9, 1))

    dev1.register_queue(queue)
    dev2.register_queue(queue)
    #End test data

    #Simulation:
    i = 1
    while i < 1000:
        i+=1
        dev1.tick()
        dev2.tick()
        queue.status()
        time.sleep(5)
        
