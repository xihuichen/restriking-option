from datetime import date

class tradeslist:

    # A student ID counter
    tradeidCounter = 0

    def __init__(self, ls, id, nnotional,inputterminationdate,p0=100,inputdealdate=date.today()):
        self.longshort = ls
        self.assetid = id
        self.dealdate = inputdealdate
        self.terminationdate = inputterminationdate
        self.notional = nnotional
        self.p0 = p0
        self.record = {}
        # Each time I create a new student, the idCounter increment
        tradeslist.tradeidCounter += 1
        self.name = 'Trades {0}'.format(tradeslist.tradeidCounter)
        # newTrades = tradeslist()
        # classRoster.append(newTrades)
        # print(newTrades.name)

    def getassetid(self):
        return self.assetid

    def getls(self):
        return self.longshort

    def getp0(self):
        return self.p0

    def getnotional(self):
        return self.notional    
    
    def getterminationdate(self):
        return self.terminationdate

    def setassetid(self, newassetid):
        self.assetid = newassetid

    def setlongshort(self, ls):
        self.longshort = ls

    def setnotional(self, newnotional):
        self.notional = newnotional
    
    def setterminationdate(self, termination):
        self.terminationdate = termination

    def setTradeprice(self, newnotional):
        self.p0 = newnotional

    def setdealdate(self, date):
        self.dealdate = date


class EOption(tradeslist):
    """
    Here we defined the european option
    """

    def __init__(self, ls, id, callput, strike, nnotional,inputterminationdate,p0=100,inputdealdate=date.today()):
        tradeslist.__init__(self, ls, id, nnotional,inputterminationdate,p0=100,inputdealdate=date.today())
        self.cp = callput
        self.strike = strike
        
    def getcp(self):
        return self.cp

    def getstrike(self):
        return self.strike

    def setcp(self, cp):
        self.cp = cp

    def setstrike(self, strike):
        self.strike = strike
        
class RSoption(tradeslist):
   """ here we define the restriking option"""

   def __init__(self, ls, id, callput,inputterminationdate, strike,nnotional,threshold,observation,method,limit,p0=100,inputdealdate=date.today()):
        tradeslist.__init__(self, ls, id, nnotional,inputterminationdate,p0=100,inputdealdate=date.today())
        self.cp = callput
        self.strike = strike
        self.threshold = threshold
        self.p0=p0
        self.observation = observation
        self.ls = ls
        self.method = method
        self.limit = limit
   def getls(self):
       return self.ls
   
   def getp0(self):
        return self.p0
   def getcp(self):
        return self.cp

   def getstrike(self):
        return self.strike

   def setcp(self, cp):
        self.cp = cp

   def setstrike(self, strike):
        self.strike = strike           
#==============================================================================
#     def setthreshold(self,threshold):
#         self.threshold= threshold
#==============================================================================
    
   def getthreshold(self):
       return self.threshold
   def getobs(self):
       return self.observation
   def setthreshold(self, threshold):
       self.threshold = threshold
   def setobservation(self, observation):
       self.observation = observation
   def setmethod(self, method):
       self.method = method
   def getmethod(self):
       return self.method
   def setlimit(self, limit):
       self.limit = limit
   def getlimit(self):
       return self.limit
  
class DDoption(tradeslist):
    """
    Here we defined the (dual)digital option
    """

    def __init__(self, ls, id, settlement, callput, strike, nnotional,inputterminationdate,p0=100,inputdealdate=date.today()):
        tradeslist.__init__(self, ls, id, nnotional,inputterminationdate,p0=100,inputdealdate=date.today())
        self.cp = callput
        self.strike = strike
        self.settlement = settlement
        
    def getcp(self):
        return self.cp

    def getstrike(self):
        return self.strike

    def setcp(self, cp):
        self.cp = cp

    def setstrike(self, strike):
        self.strike = strike
        
    def getsettlement(self):
        return self.settlement

    def setsettlement(self, settlement):
        self.settlement = settlement

        
class Autocall(tradeslist):
    """
    Here we defined the european option
    """

    def __init__(self, ls, id, settlement, couponbarrier, strike, knockout, knockin, nnotional,inputterminationdate,coupon,p0=100,inputdealdate=date.today()):
        tradeslist.__init__(self, ls, id, nnotional,inputterminationdate,p0=100,inputdealdate=date.today())
        self.settlement = settlement
        self.couponbarrier = couponbarrier
        self.knockout = knockout
        self.knockin = knockin
        self.strike = strike
        self.coupon = coupon
    
    def getsettlement(self):
        return self.settlement

    def setsettlement(self, settlement):
        self.settlement = settlement
    
    def getcp(self):
        return self.cp
    
    def setcp(self, cp):
        self.cp = cp
        
    def getcoupon(self):
        return self.coupon

    def setcoupon(self, coupon):
        self.coupon = coupon    

    def getstrike(self):
        return self.strike

    def setstrike(self, strike):
        self.strike = strike
        
    def getcouponbarrier(self):
        return self.couponbarrier
    
    def setcouponbarrier(self, cp):
        self.couponbarrier = cp
        
    def getknockout(self):
        return self.knockout
    
    def setknockout(self, cp):
        self.knockout = cp
        
    def getknockin(self):
        return self.knockin
    
    def setknockin(self, cp):
        self.knockin = cp
        
class ContingentOption(tradeslist):
    """
    Here we defined the Contingent Option
    """
    def __init__(self, ls, id, callput, strike, nnotional,inputterminationdate,p0=100,\
                 inputdealdate=date.today(), ContingentAssetId=[], ContingentAssetStrike=[], ContingentDirection=[]):
        tradeslist.__init__(self, ls, id, nnotional,inputterminationdate,p0=100,inputdealdate=date.today())
        self.ContingentAssetId = ContingentAssetId
        self.ContingentDirection = ContingentDirection
        self.strike = strike
        
    def getcp(self):
        return self.cp

    def getstrike(self):
        return self.strike

    def setcp(self, cp):
        self.cp = cp

    def setstrike(self, strike):
        self.strike = strike
        
    def getsettlement(self):
        return self.settlement

    def setsettlement(self, settlement):
        self.settlement = settlement  
    
    def getContingentAssetId(self):
        return self.ContingentAssetId

    def setContingentAssetId(self, ContingentAssetId):
        self.ContingentAssetId = ContingentAssetId
        
    def getContingentAssetStrike(self):
        return self.ContingentAssetStrike

    def setContingentAssetStrike(self, ContingentAssetStrike):
        self.ContingentAssetStrike = ContingentAssetStrike
        
    def getContingentDirection(self):
        return self.ContingentDirection

    def setContingentDirection(self, ContingentDirection):
        self.ContingentDirection = ContingentDirection
        
