import time
from datetime import datetime

class Env():
    def __init__(self, name):
        self.name = name
        self.is_free = True
        self.order = None
        self.queue = None

    def start(self, order):
        self.order = order
        self.is_free = False

    def stop(self):
        self.order = None
        self.is_free = True

    def kick(self):
        self.stop()

class Queue():
    """ Queue object that keeps orders in right sequence
    """
    def __init__(self):
        self.items = []

    def enque(self, item):
        """Add order to the end of queue
        """
        self.items.append(item)

    def deque(self, env):
        """Remove the first order that matches requested [env] from the queue
        """
        if self.items:
            i = 0
            count = len(self.items)
            while i < count:
                
                if env.name in self.items[i].envs:
                    print('I was removed from queue: {0} by {1}'.format(env.name, self.items[i].user))
                    return self.items.pop(i)
                i += 1
            return None
    
    def status(self):
        """Just temporary method, will be removed in future
        """
        print('Queue status:')
        for item in self.items:
            print("Order for {} by {}".format(item.envs, item.user))

class Order():
    """Order object. Contains information about list of requested environments and requester.
    In future, user property will represent Dgango auth user object
    """
    def __init__(self, envs, user, ordered_duration):
        self.envs = envs
        self.user = user
        self.ordered_duration = ordered_duration
        self.start_time = None
        self.registration_time = datetime.now()

    def start(self, env):
        """Start work with environment
        """
        self.start_time = datetime.now()

    def count_fact_duration(self):
        fact_duration = datetime.now() - self.start_time
        return fact_duration.seconds

    def coun_time_left(self):
        time_left = self.ordered_duration - self.count_fact_duration()
        return time_left

    def is_finished(self):
        if self.coun_time_left() <= 0:
            return True
        else:
            return False

class QueueProcessor():
    """Implements queue processing logic
    """
    def __init__(self, queue, envs):
        self.queue = queue
        self.envs = envs

    def tick(self):
        """This method should be triggered my internal core process each n seconds
        """
        self.push_orders_from_queue_to_env()
        self.remove_orders_from_env()

    def push_orders_from_queue_to_env(self):
        """Removes order from Queue and adds to Env
        """
        for env in self.get_free_envs():
            order = self.queue.deque(env)
            if order:
                order.start(env)
                env.start(order)

    def remove_orders_from_env(self):
        for env in self.get_busy_envs():
            if env.order.is_finished():
                env.stop()
    
    def get_free_envs(self):
        return [env for env in self.envs if env.is_free]

    def get_busy_envs(self):
        return [env for env in self.envs if not env.is_free]


if __name__ == "__main__":
    
    #Test data

    #Create environments
    dev1 = Env('dev1')
    dev2 = Env('dev2')
    envs = [dev1, dev2]
    #Create users
    user1 = 'user1'
    user2 = 'user2'
    user3 = 'user3'
    user4 = 'user4'
    user5 = 'user5'
    user6 = 'user6'
    user7 = 'user7'
    user8 = 'user8'
    user9 = 'user9'

    #Create Queue
    queue = Queue()
    #Add Order to the Queue: User1 wants to order DEV1 for 1 second
    queue.enque(Order(['dev1'],user1, 1))
    queue.enque(Order(['dev1'],user2, 1))
    queue.enque(Order(['dev1'],user3, 1))
    queue.enque(Order(['dev1', 'dev2'],user4, 1))
    queue.enque(Order(['dev1'],user5, 1))
    queue.enque(Order(['dev1'],user6, 1))
    queue.enque(Order(['dev2'],user7, 1))
    queue.enque(Order(['dev2', 'dev1'],user8, 1))
    queue.enque(Order(['dev1'],user9, 1))

    q_proc = QueueProcessor(queue, envs)
    

    #Simulation:
    i = 1
    while i < 1000:
        i+=1
        q_proc.tick()
        queue.status()
        time.sleep(5)
        
