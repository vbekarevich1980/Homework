# Task 9.1
#
# Implement the dining philosophers problem

from threading import Thread, Lock
from time import sleep


class Philosophers(Thread):
    def __init__(self, name, left_hand, right_hand):
        Thread.__init__(self)
        self.name = name
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.times = 0

    def consider(self):
        print(f"{self.name} is considering\n")
        sleep(3)

    def bite(self):
        print(f"{self.name} has started eating\n")
        sleep(10)
        self.times += 1
        print(f"{self.name} has bit {self.times} times\n")

    def decision(self):
        while True:
            self.consider()
            if not self.left_hand.locked():
                with self.left_hand:
                    print(f"{self.name} has used left fork\n")
                    self.consider()
                    if not self.right_hand.locked():
                        with self.right_hand:
                            print(f"{self.name} has used right fork\n")
                            self.bite()

    def run(self):
        self.decision()


if __name__ == "__main__":
    philosophers_list = ["One", "Two", "Three", "Four", "Five"]
    forks = [Lock() for i in range(5)]
    philosophers = [
        Philosophers(f"{philosophers_list[i]}", forks[i], forks[(i + 1) % 5])
        for i in range(5)
    ]
    for philosopher in philosophers:
        philosopher.start()
