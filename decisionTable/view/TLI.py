
class Tli:
    @staticmethod
    def showErrors(title,errors = []): 
        raise ValueError(title+'\n'+('='*30)+'\n'+'\n > '.join(errors))