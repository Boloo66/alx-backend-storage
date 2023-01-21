#!/usr/bin/env python3

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
        #self.msg = self.name + " got " + self.grade

    @property
    def msg(self):
        return self.name + " got " + self.grade

    @msg.setter
    def msg(self, msg2):
        msg1 = msg2.split(" ")
        print(msg1)
        self.name = msg1[0]
        self.grade = msg1[-1]


class Score:
    def __init__(self, score):
        self.__score = score


s = Score(200)
s.__score = 100
print(s.__score)
print(dir(s))
