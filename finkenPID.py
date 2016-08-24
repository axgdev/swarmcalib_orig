import math
import logging

class PIDController:
    'Common base class for all PID'

    def __init__(self, newP, newI, newD, logger):
        self.p = newP
        self.i = newI
        self.d = newD
        self.e = 0
        self.e_prev = 0
        self.e_sum = 0
        self.pChange = 0
        self.iChange = 0
        self.dChange = 0
        self.changeThreshold = 1
        self.differentialThreshold = 50
        self.logger = logger
        
    def sign(self, x):
        return (x<0 and -1) or 1
        
    def step(self, newE, deltat):
        self.e_prev = self.e
        self.e = newE
        if self.sign(newE) == self.sign(self.e_prev):
            self.e_sum = self.e_sum + newE * deltat
        else:
            self.e_sum = 0
        #print('P:{} I:{} D:{} E:{} E_PREV:{} E_SUM:{}'.format(self.p,self.i,self.d,self.e,self.e_prev,self.e_sum))
        self.pChange = self.p*self.e
        self.iChange = self.i*self.e_sum
        self.dChange = self.d*((self.e-self.e_prev)/deltat)
        totalChange = self.pChange + self.iChange + self.dChange
        exponent = self.e/self.differentialThreshold
        thresholdTerm = self.changeThreshold*(math.pow(1.2,exponent*exponent)-1) #when error equals differential threshold, the full changeThreshold is considered
        self.logger.debug("ExpTerm: %f, ThresholdTerm: %f" % (math.pow(1.2,exponent*exponent)-1,thresholdTerm))
        if (totalChange > thresholdTerm):
            totalChange = thresholdTerm
        elif (totalChange < -thresholdTerm):
            totalChange = -thresholdTerm
        
        return (totalChange)
        
    def reset(self):
        self.e = 0
        self.e_prev = 0
        self.e_sum = 0
    
    def printValues(self):
        simxAddStatusbarMessage("error: " + e)
        simxAddStatusbarMessage("previous error: " + e_prev)
        simxAddStatusbarMessage("accumulated error: " + e_sum)
        simxAddStatusbarMessage("p: " + p)
        simxAddStatusbarMessage("i: " + i)
        simxAddStatusbarMessage("d: " + d)
