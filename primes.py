#!/usr/bin/env python3
#class that define the primes problem to be used in a distribted system
#author: Eduardo Pinhata

class primes:
    def __init__(self, begin, end, gap):
        self.begin = begin
        self.end = end
        self.processing =[]
        self.processed = []
        self.gap = gap
        self.unitProc = 1 
        self.answer = []

    #define the intervall that the device will process.
    def getProcessUnit(self):
        init_int = self.begin + (self.unitProc-1)*self.gap
        end_int = init_int + self.gap -1
        print('The interval will be ' + str(init_int) + '-' + str(end_int)) 
        interval = str(self.unitProc) + ':' + str(init_int) + ':' + str(end_int)
        self.processing.append(self.unitProc)
        self.unitProc += 1
        print("UnitProc after update: " + str(self.unitProc))
        print(self.processing)
        #insert into processing list

        return interval

    #
    def update(self, unitProc, result):
        #remove from processing and insert into processeda
        print('UnitProc: ' + str(unitProc))
        #self.processing.remove(unitProc)
        self.processing = [x for x in self.processing if x!= unitProc]
        self.processed.append(unitProc)
        #append result in the result set
        for i in result:
            self.answer.append(i)

    def isFinished(self):
        if((self.begin+self.gap*self.unitProc)>=self.end):
            return True
        return False


