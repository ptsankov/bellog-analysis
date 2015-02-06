from utils import TRUE, ERROR

class Atom:
    # Empty default constructor
    def __init__(self):
        pass
        
    # String constructor for atoms
    @classmethod
    def fromString(self, string):
        newAtom = Atom()
        if '(' not in string:
            # no arguments
            newAtom.pred = string
            newAtom.args = []
        else: 
            newAtom.pred = string.split('(')[0]            
            newAtom.args = string.split('(')[1].split(')')[0].split(',')
        newAtom.checkRemote()
        return newAtom

    def getCopy(self):
        copyAtom = Atom()
        copyAtom.pred = self.pred
        copyAtom.args = []
        for arg in self.args:
            copyAtom.args.append(arg)
        return copyAtom
        
    def checkRemote(self):
        if '@' in self.pred:            
            self.remote = True
            self.address = self.pred.split('@')[1]
            self.table = self.pred.split('@')[0]
        else:
            self.remote = False
            
    def replaceArg(self, old, new):
        self.args = [x if x != old else new for x in self.args]
        
    def vars(self):
        listVars = [arg if arg.isupper() else 'dummy' for arg in self.args]
        setVars = set(listVars)
        if 'dummy' in setVars:
            setVars.remove('dummy')
        return setVars
        
    def consts(self):
        listConsts = [arg if arg.islower() else 'dummy' for arg in self.args]
        setConsts = set(listConsts)
        if 'dummy' in setConsts:            
            setConsts.remove('dummy')
        return setConsts
    
    def isGround(self):
        return len(self.vars()) == 0
    
    def __str__(self):
        string = self.pred
        if len(self.args) > 0:
            string  = string + '(' + ', '.join(self.args) + ')'
        return string
    
    def getProposition(self):
        return self.pred + '_' + '_'.join(self.args)
    
    def toDatalog(self, v):
        string = self.pred + '_' + v
        if len(self.args) > 0:
            string  = string + '(' + ', '.join(self.args) + ')'
        return string 
        
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (self.pred, self.args) == (other.pred, other.args)