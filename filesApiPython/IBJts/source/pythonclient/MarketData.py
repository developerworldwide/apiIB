from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
import time 

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ",reqId,"  ",errorCode," ",errorString)

    def tickPrice(self, reqId , tickType, price,attrib):
        print("Tick Price. Ticket Id:",reqId,"tickType:",TickTypeEnum.to_str(tickType),"Price:",price, end='')

    def tickSize(self, reqId, tickType, size):
        print("Tick Size.Ticker Id:",reqId,"tickType:",TickTypeEnum.to_str(tickType),"Size:", size)

def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 0)
    time.sleep(3)
    
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    Contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"

    #Esto son metodos de la clase EClient
    app.reqMarketDataType(4) # Este 4 es para delayed-frozen data

                #(tickrId, contract, genericTickList(GenericTickTypes), snapshot, regulatorySnaphsot,mkdDataOptions)
    app.reqMktData(0,contract,"",False,False,[])
    app.run()
    self.disconnect() #No Funciona, No para el codigo
    app.disconnect() #No Funciona,No para el codigo

if __name__ == "__main__":
    main()