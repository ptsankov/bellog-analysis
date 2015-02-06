#!/usr/bin/python

from atom import Atom
from utils import TRUE, ERROR
import sys

class Literal:
    # Empty default constructor
    def __init__(self):
        pass
    
    #String constructor for literals
    @classmethod
    def fromString(self, string):
        newLiteral = Literal()
        if string[0] == '!':
            newLiteral.op = '!'
            newLiteral.atom = Atom.fromString(string[1:]) 
        elif string[0] == '#':
            newLiteral.op = '#'
            newLiteral.atom = Atom.fromString(string[1:])
        else:
            newLiteral.op = None
            newLiteral.atom = Atom.fromString(string)
        return newLiteral
    
    #String constructor for literals
    @classmethod
    def fromAtom(self, atom):
        newLiteral = Literal()
        newLiteral.op = None
        newLiteral.atom = atom
        return newLiteral 
    
    def vars(self):
        return self.atom.vars()    
    
    def consts(self):
        return self.atom.consts()
    
    def isGround(self):
        return self.atom.isGround()
    
    def replaceArg(self, old, new):
        self.atom.replaceArg(old, new)
    
    def __str__(self):
        if self.op is not None:
            string = self.op
        else:
            string = ''
        return string + str(self.atom)
    
    def getCopy(self):
        copyLiteral = Literal()
        copyLiteral.op = self.op
        copyLiteral.atom = self.atom.getCopy()
        return copyLiteral
    
    def toDatalog(self, v):
        if v not in [TRUE, ERROR]:
            print 'Invalid argument'
            sys.exit(-1)
        if self.op is None:
            return self.atom.toDatalog(v)
        elif self.op == '!':
            if v == TRUE:
                return 'tnot(' + self.atom.toDatalog(ERROR) + ')'
            else:
                return 'tnot(' + self.atom.toDatalog(TRUE) + ')'
        elif self.op == '#':
            return self.atom.toDatalog(TRUE)
         
        
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (self.op, self.atom) == (other.op, other.atom)    
