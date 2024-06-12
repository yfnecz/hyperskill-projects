import os
import time
from threading import Thread, Lock
from collections import deque


class TrafficLight:
    def __init__(self):
        print("Welcome to the traffic management system!")
        self.max_roads = None
        self.interval = None
        self.start_time = None
        self.l = Lock()
        self.k = 1
        self.state = ''
        self.roads = deque()
        self.open_time = None
        self.offset = 0

    def validate_input(self):
        self.l.acquire()
        error = "Error! Incorrect Input. "
        input_line = "Input the number of roads:"
        while not self.max_roads:
            roads = input(input_line)
            if roads.isdigit() and int(roads) > 0:
                self.max_roads = int(roads)
                break
            print(error, end='')
            input_line = "Try Again:"
        input_line = "Input the interval:"
        while not self.interval:
            interval = input(input_line)
            if interval.isdigit() and int(interval) > 0:
                self.interval = int(interval)
                break
            print(error, end='')
            input_line = "Try Again:"
        self.start_time = time.time()
        self.l.release()

    @staticmethod
    def calc_distance(queue, i, j):


    @staticmethod
    def validate_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Menu:\n1. Add road\n2. Delete road\n3. Open system\n0. Quit")
        menu_choice = input()
        if menu_choice.isdigit():
            menu_choice = int(menu_choice)
            if menu_choice > 3:
                menu_choice = None
        else:
            menu_choice = None
        return menu_choice

    def add_road(self):
        a = input("Input road name:")
        if len(self.roads) < self.max_roads:
            if not len(self.roads):
                self.open_time = int(time.time())
                self.roads.append([a, self.open_time])
            else:
                self.roads.append([a, None])
            print(f"Road {a} added!")
        else:
            print("queue is full")

    def delete_road(self):
        if len(self.roads) > 0:
            if True:
                self.offset += 0 # if road was open, add offset for it to the total
            a = self.roads.popleft()
            print(f"Road {a} deleted!")
            if not len(self.roads):
                self.open_time = None
        else:
            print("queue is empty")

    def run(self):
        self.validate_input()
        while True:
            self.l.acquire()
            self.state = ''
            i = self.validate_menu()
            if i is None:
                print("Incorrect option")
            elif i == 0:
                print("Bye!")
                self.k = 0
                break
            elif i == 1:
                self.add_road()
            elif i == 2:
                self.delete_road()
            else:
                print("System opened!")
                self.state = 'System'
            self.l.release()
            input()

    def print_state(self):
        while self.k:
            if self.state == 'System':
                self.l.acquire()
                os.system('cls' if os.name == 'nt' else 'clear')
                time_passed = int(time.time() - self.start_time)
                print(f"! {time_passed}s. have passed since system startup !")
                print(f"! Number of roads: {self.max_roads} !")
                print(f"! Interval: {self.interval} !\n")
                secs = 0
                num = -1
                if len(self.roads):
                    times = int(time.time() - self.open_time)
                    secs = times % (self.interval * len(self.roads)) # seconds since the beginning of the first road open this cycle
                    num = secs // self.interval # number of road currently open
                for i, road in enumerate(self.roads):
                    open_secs = (num + 1) * self.interval - secs # seconds current open road will be open
                    road_open = 'open' if i == num else 'closed'
                    if i != num:
                        if i > num:
                            open_secs += self.interval * (i - num - 1)
                        if i < num and num - i != len(self.roads):
                            open_secs += self.interval * (len(self.roads) - num - 1)
                            open_secs += self.interval * (num - i - 1)
                    if not open_secs:
                        open_secs = self.interval
                    print(f'road "{road[0]}" will be {road_open} for {open_secs}s.')
                print('\n! Press "Enter" to open menu !')
                self.l.release()
                time.sleep(1)


if __name__ == '__main__':
    t = TrafficLight()
    t1 = Thread(target=TrafficLight.print_state, args=(t,))
    t1.setName("QueueThread")
    t1.start()
    t.run()
    t1.join()
