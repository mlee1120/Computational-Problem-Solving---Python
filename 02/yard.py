'''
yard.py
This module defines the class LumberYard.
'''
__author__ = 'zjb'

class LumberYard:
    __slots__ = 'logs'

    def __init__(self):
        '''
        Creates the LumberYard object.
        '''
        self.logs = []

    def addLog(self,log):
        '''
        Adds a log to the lumber yard.
        :param log: length of log to add.
        '''
        self.logs.append(log)

    def allLogs(self):
        '''
        :return: List of logs in the yard.
        '''
        return self.logs
