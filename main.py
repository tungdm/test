import json
import math
import threading
import time
import random
import uuid
import psutil
import os
from app.rabbit_worker import Rabbit
# from rabbit_worker import Rabbit
from app.singleton import Singleton
# from singleton import Singleton


MESSAGES_PER_WORKER = 5
MAX_CPU_USAGE_PERCENT = 80


class Worker(Singleton):
    """ Worker class. """

    def __init__(self):
        print('====> Worker is starting...')
        # self.__binding_to_user_queue()
        # self.__init_subscribers()

    def my_implement():
        for i in range(10):
            print('Hello: ', i)

    def binding_to_user_queue(self):
        """ Binding to user queue when start worker. """
        print('Binding to user queue when startup')
        rabbit = Rabbit()
        rabbit.subscribe(self.__callback)
        print('===> Unsubscribe done.')

    def __callback(self, channel, method, properties, body):
        """ Callback function used to init subscriber. """
        print('method: ', method)
        print('properties: ', properties)
        data = json.loads(body.decode('utf-8'))
        user = data.get('user')
        total_messages = data.get('total_messages')
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print('===> user: %s, total: %s' % (user, total_messages))

        if user:
            fusion_queue = "%s_fusion_queue" % user
            print('fusion_queue: ', fusion_queue)
            num_subs = math.ceil(total_messages/MESSAGES_PER_WORKER)
            print('num_subs: ', num_subs)
            # TODO: save numbers of workers to redis
            for i in range(num_subs):
                sub_name = str(uuid.uuid4())
                threading.Thread(target=self.__create_suscriber,
                                 args=(fusion_queue,),
                                 name=sub_name).start()

    def __create_suscriber(self, queue):
        """ Create subscriber and subscribe to corresponding queue. """
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        print('cpu_usage:', cpu_usage)

        if min(cpu_usage) < MAX_CPU_USAGE_PERCENT:
            thread_name = threading.current_thread().getName()
            print('\tStart ', thread_name)
            rabbit = Rabbit()
            # TODO: substract redis count_worker by 1

            rabbit.subscribe(callback=self.__process_data,
                             queue=queue, auto_delete=True)
            print('===> %s - Unsubscribe done.' % thread_name)
        else:
            print('\tOverload... Scaling')

    def __process_data(self, channel, method, properties, body):
        thread_name = threading.current_thread().getName()
        data = json.loads(body.decode('utf-8'))
        transmit_time = time.time()*1000 - data.get('time')*1000

        print('Process %s - Thread name %s recieved message: %s, time: % 4dms, method: %s, properties: %s' %
              (os.getpid(), thread_name, data, transmit_time, method, properties))
        r = random.randint(0, 1)
        if r:
            if data.get('flag') == 'cancel':
                channel.basic_cancel(consumer_tag=method.consumer_tag)
                print('\t\t====> Quit consumer.')
            else:
                print('\t\t====> Processing data....')
                time.sleep(1)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print('\t\t====> Reject message.')
            channel.basic_reject(
                delivery_tag=method.delivery_tag, requeue=True)

    def __init_subscribers(self):
        """ Initiation subscribers when start worker. """
        pass
