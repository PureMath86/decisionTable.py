# -*- coding: utf-8 -*-
from __future__ import absolute_import

from . import view

class DecisionTable:
    def __init__(self,data,wildcardSymbol='*',parentSymbol='.'):
        
        self.header = [] 
        self.decisions = []
        
        self.__setWildcardSymbol(wildcardSymbol)
        self.__setParentSymbol(parentSymbol)
        
        self.__parseStringData(data)
        self.__replaceSpecialValues()
    
    def __setWildcardSymbol(self,value):
        errors = []
        if not value is str and not value.split():
            errors.append('wildcardSymbol_ERROR : Symbol : must be char or string!')
        else:
            self.__wildcardSymbol = value
        
        if errors:
            view.Tli.showErrors('SymbolError', errors)
            
    def __setParentSymbol(self,value):
        errors = []
        if not value is str and not value.split():
            errors.append('parentSymbol_ERROR : Symbol : must be char or string!')
        else:
            self.__parentSymbol = value
        
        if errors:
            view.Tli.showErrors('SymbolError', errors)
            
    def __parseStringData(self,data):
        error = [] 

        if not data.split():
            error.append('Data variable is empty!')
        
        data = data.split('\n')
        newData = []
        for element in data:
            if element.strip():
                newData.append(element)
        
        for element in newData[0].split():
            if not element in self.header:
                self.header.append(element)
            else:
                error.append('Header element: '+element+' is not unique!')

        for i, data in enumerate(newData[2:]):
            split = data.split()
            if len(split) == len(self.header):
                self.decisions.append(split)
            else:
                error.append('Row: {}==> missing: {} data'.format(
                    str(i).ljust(4),
                    str(len(self.header)-len(split)).ljust(2))
                )
        
        if error:
            view.Tli.showErrors(error)
            
    
    def __replaceSpecialValues(self):
        error = []
        for row, line in enumerate(self.decisions):
            if '.' in line:
                for i, element in enumerate(line):
                    if row == 0:
                        error.append("Row: {}colume: {}==> don't have parent value".format(str(row).ljust(4),str(i).ljust(4)))
                    if element==self.__parentSymbol:
                        if self.decisions[row-1][i] == '.':
                            error.append("Row: {}Colume: {}==> don't have parent value".format(str(row).ljust(4),str(i).ljust(4)))
                        
                        self.decisions[row][i]=self.decisions[row-1][i]
        
        if error:
            view.Tli.showErrors(error)

    def __toString(self,values):
        for key in values:
            if not values[key] is str:
                values[key] = str(values[key])
        return values
    
    def __valueKeyWithHeaderIndex(self,values):
        machingIndexes = {}
        for index, name in enumerate(self.header):
            if name in values:
                machingIndexes[values[name]] = index
        return machingIndexes
    
    def __checkDecisionParameters(self,result,multiple=False,**values):
        error = []
        
        if not result:
            error.append('Function parameter (result array) should contain one or more header string!')
        
        if not values:
            error.append('Function parameter (values variables) should contain one or more variable')
        
        for header in result:
            if not header in self.header:
                error.append('String ('+header+') in result is not in header!')
        
        for header in values:
            if not header in self.header:
                error.append('Variable ('+header+') in values is not in header!')
            elif not values[header].split():
                error.append('Variable ('+header+') in values is empty string')
        
        if error:
            view.Tli.showErrors(error)
                
    def __getDecision(self,result,multiple=False,**values):
        
        values = self.__toString(values)
        __valueKeyWithHeaderIndex = self.__valueKeyWithHeaderIndex(values)
        
        self.__checkDecisionParameters(result,multiple,**values)

        machingData = {}
        for line in self.decisions:

            match = True 

            for valueKey in __valueKeyWithHeaderIndex:
                if line[__valueKeyWithHeaderIndex[valueKey]] != valueKey:
                    if line[__valueKeyWithHeaderIndex[valueKey]] != self.__wildcardSymbol:
                        match = False
                        break
            
            if match:
                if multiple:
                    for header in result:
                        if not header in machingData:
                            machingData[header] = [line[self.header.index(header)]]
                        else:
                            machingData[header].append(line[self.header.index(header)])
                else:
                    for header in result:
                        machingData[header] = line[self.header.index(header)]
                    return machingData
        
        if multiple:
            if machingData:
                return machingData

        #Return none if not found (not string so
        #not found value can be recognized
        return {key:None for key in result}

    def decisionCall(self,callback,result,**values):
        callback(**self.__getDecision(result,**values))
    
    def decision(self,result,**values):
        data = self.__getDecision(result,**values)
        data = [ data[value] for value in result]
        if len(data) == 1:
            return data[0]
        else:
            return data
    
    def allDecisions(self,result,**values):
        data = self.__getDecision(result,multiple=True,**values)
        data = [ data[value] for value in result]
        if len(data) == 1:
            return data[0]
        else:
            return data