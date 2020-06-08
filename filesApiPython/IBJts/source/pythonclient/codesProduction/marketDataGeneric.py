#!/usr/bin/env python3
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum 
import datetime
import time
import sys

global myList
global app
global var1
global var2
global finalList

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        global myDict
        #myDict = {}
        #myDict ={'68':'0.0','72':'0.0','73':'0.0','75':'0.0','74':'0.0'}
        myDict ={'68':0,'72':0,'73':0,'75':0,'74':0} #Tener Diccionario con 0 por si un dato No viene.
        global contador
        contador = 3

    def processTickLine(self):
        global contador
        print("GENERANDO FICHERO")
        x = datetime.datetime.now()
        print(x.strftime("%x"))
        myDict ['d'] = x.strftime("%x")
        with open(('./DATOS/%s/%s.txt' % (var1,var2)), 'a+') as f:
            f.write("%s,%2.2f,%2.2f,%2.2f,%2.2f,%i" % ((myDict['d']),
                                                    (myDict['68']),
                                                    (myDict['72']),
                                                    (myDict['73']),
                                                    (myDict['75']),
                                                    (myDict['74'])) + '\n')
        print("Pasando Por Contador")
        contador -= 1
        print(contador)
        if contador == 0:
            print("Termine con un contrato de la lista")
            #self.otroContrato()
            self.disconnect()# Manda al codigo a la linea despues de app.run()
        else:
            print("Faltan lineas para terminar")   

    def error(self, reqId, errorCode, errorString):
        print("Error: ",reqId,"  ",errorCode," ",errorString)
        
    def tickPrice(self, reqId ,tickType, price,attrib):
        if tickType == 68:
            myDict['68'] = price
            print(TickTypeEnum.to_str(tickType),"Price:", price)
            if len(myDict) > 4:
                self.processTickLine()
                                         
        if tickType == 72:#Este tickType solo viene cuando cerro el mercado
            myDict['72'] = price
            print(TickTypeEnum.to_str(tickType),"Price:", price)
        
        if tickType == 73:#Este tickType solo viene cuando cerro el mercado
            myDict['73'] = price
            print(TickTypeEnum.to_str(tickType),"Price:", price)
        
        if tickType == 75:#Este tickType solo viene una vez
            myDict['75'] = price
            print(TickTypeEnum.to_str(tickType),"Price:", price)
            if len(myDict) > 4:
                self.processTickLine()
        
    def tickSize(self, reqId, tickType, size):
        if tickType == 74:
            myDict['74'] = size
            print(TickTypeEnum.to_str(tickType), "Size:", size)
            if len(myDict) > 4:
               self.processTickLine() 
           
def main():
    time.sleep(3)
    global finalList
    global myList
    global app
    global var1
    global var2
    app = TestApp()
    app.connect("127.0.0.1", 7497, 0)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    
    time.sleep(3)
    contract = Contract()
    contract.symbol = var2                #variable 2
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = var1     #variable 1 

        #Esto son metodos de la clase EClient
    app.reqMarketDataType(4) # Este 4 es para delayed-frozen data
                
                #(tickrId, contract, genericTickList(GenericTickTypes), snapshot, regulatorySnaphsot,mkdDataOptions)
    app.reqMktData(0,contract,"",False,False,[])
    app.run()
    print("Existen mas contratos ???")
    newContrato()#Importante Evalua si existen mas contratos
    
def contratos():
    global myList
    global finalList
    global var1
    global var2
    finalList = [] # Lista Vacia
    myList = []
    print("Todos los contratos")
    with open('descargas.txt','r') as file: 
        # reading each line	 
        for line in file: 
            for word in line.split():
                print(word)
                myList.append(word)
            print("Termine de leer una linea del fichero")
			#print("Lista Previa donde se elimina el EOL:")
        print("Lista donde se elimina el EndOfLine del fichero descargas.txt:")
        print(myList)
        print("Uniendo los elementos en la lista")
        print(','.join(myList))
        s = (','.join(myList))#Juntando todo los elementos en una variable
        print("Valor de S:")
        print(s)
        for elemento in s.split(','):
            print(elemento)
            finalList.append(elemento)
        print("Lista Final para Contratos")
        print(finalList)
        print("Asigno Posicion")	
        var1 = finalList[0]
        var2 = finalList[1]
        print(finalList)
        print("Termine el bucle de for y lectura del archivo.txt / Tengo un array de contratos")
            

def newContrato():
    global app
    global var1
    global var2 
    global myList
    global finalList
    print("Elimine conexion del objeto anterior de la clase TestApp")
    finalList.remove(finalList[0])
    finalList.remove(finalList[0])
    
    if len(finalList) == 0:
        print("Termine todos los contratos")
        sys.exit()
    else:
        print("Faltan contratos")
        print("Asigno posiciones")
    var1 = finalList[0]
    var2 = finalList[1]
    print(finalList)
    main()
   
contratos()
main()
    