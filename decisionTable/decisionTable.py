# -*- coding: utf-8 -*-
class DecisionTable:
    def __init__(self,data,wildcardSymbol='*',parentSymbol='.'):
        
        self.header = [] 
        self.decisions = []
        
        self.__wildcardSymbol = wildcardSymbol
        self.__parentSymbol = parentSymbol
        
        self.__parseStringData(data)
        self.__replaceSpecialValues()
        
    def __parseStringData(self,data):
        data = data.split('\n')
        newData = []
        for element in data:
            if element.strip():
                newData.append(element)
        
        self.header = newData[0].split()
        
        error = [] 
        for i, data in enumerate(newData[2:]):
            split = data.split()
            if len(split) == len(self.header):
                self.decisions.append(split)
            else:
                error.append('Row: {}==> missing: {} data'.format(str(i).ljust(4),str(len(self.header)-len(split)).ljust(2)))
        
        if error:
            raise ValueError('\n'+('='*30)+'\n'+'\n'.join(error))
    
    def __replaceSpecialValues(self):
        error = []
        for row, line in enumerate(self.decisions):
            if '.' in line:
                for i, element in enumerate(line):
                    if element==self.__parentSymbol:
                        if self.decisions[row-1][i] == '.':
                            error.append("Row: {}Colume: {}==> don't have parent value".format(str(row).ljust(4),str(i).ljust(4)))
                        
                        self.decisions[row][i]=self.decisions[row-1][i]
        
        if error:
            raise ValueError('\n'+('='*57)+'\n'+'\n'.join(error))

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
    
    def __getDecision(self,result,multiple=False,**values):
        
        values = self.__toString(values)
        __valueKeyWithHeaderIndex = self.__valueKeyWithHeaderIndex(values)
        
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

        raise ValueError('Decision in table is not found')

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