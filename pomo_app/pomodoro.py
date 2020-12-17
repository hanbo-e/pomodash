st#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:59:10 2020

@author: hanbo
"""

import os
import datetime
import time
import sys

SLEEP_TIME = 1

class TimeCycle:
    'Base class for break and work timers'
    
    def __init__(self, timespan: int):
        self.timespan = timespan
    
    def __repr__(self):
        return f'<Timespan: {self.timespan}>'
        
class PomodoroCycle(TimeCycle):
    'Class for timing a 25 minute cycle and writing start end and topic to a file'
    def __init__(self, timespan = 25):
        self.timespan = timespan
        #self.topic = 'Not Specified'
    
    def run_pomodoro(self, topic: str):
        self.topic = topic
        '''
        1. Looks for a file poms.txt or creates one with first line 
        "date, tstart, tend, count" if not found.
        2. Writes current date and current time (comma separated) to poms
        3. Waits 25 minutes
        4. Writes current time and '1' followed by '\n'.
        5. Sounds a gong
        6. Closes file
        Type contract: one parameter 'topic' of type string.
        

        Returns
        -------
        Return value is prompt to continue or quit.

        '''
        if os.path.isfile("./poms.txt"):
            f = open("poms.txt", "a")
        else:
            f = open("poms.txt", "w")
            f.write("topic,date,tstart,tend,count\n")
        date = datetime.date.today()
        date = str(date)
        tstart = datetime.datetime.time(datetime.datetime.now())
        tstart = str(tstart)
        f.write(self.topic + "," + date + "," + tstart)
            
        for x in range (self.timespan, 0, -1):
            timeformat = '{:02d}'.format(x)
            print(timeformat, end="\r")
            time.sleep(SLEEP_TIME)
        
        tend = datetime.datetime.time(datetime.datetime.now()) #get time
        tend = str(tend) #write tend and count
        f.write("," + tend + ",1\n")
        f.close()
        os.system('afplay ./tone.wav')
        prompt = input("Great job! Take 5 or call it a day? 5/quit: ")
        return prompt

class BreakCycle(TimeCycle):
    'times the length of your break and then prompts you for the next pomodoro'
    def run_break(self):
        '''
        1. pauses program for five minutes
        2. Plays bell Sound
        3. Asks if you want to do another pomodoro

        Returns
        -------
        cont : String
            User input on whether to continue or not.

        '''
        for x in range (self.timespan, 0, -1):
            timeformat = '{:02d}'.format(x)
            print(timeformat, end="\r")
            time.sleep(SLEEP_TIME)
        os.system('afplay ./bell.wav')
        cont = input("Do another pomodoro? Y/N: ")
        return cont

if __name__ == "__main__":
    start = input("Hi there! When you are ready to start doing a pomodoro please type 'start' and hit enter:\n")
    while start == 'start':
        my_topic = input("Please enter the topic you are working on now: ")
        my_pom = PomodoroCycle(25)
        my_prompt = my_pom.run_pomodoro(my_topic)
        if my_prompt == '5':
            my_break = BreakCycle(5)
            again = my_break.run_break()
            if again != 'Y':
                start = 'stop'                
        else:
            print('See you later!')
            sys.exit()
    else:
        print('Bye for now')
        sys.exit()