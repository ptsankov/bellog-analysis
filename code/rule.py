#!/usr/bin/python

from literal import Literal
from atom import Atom
from utils import freshPredicate
import re
from django.utils.six import string_types
from pyparsing import nestedExpr

class Rule:
    # Empty default constructor
    def __init__(self):
        self.body = []
    
    #String constructor for riles
    @classmethod    
    def fromString(self, string):
        newRule = Rule()
        string = string.replace(' ','')
        tmp = string.split(':-')
        newRule.head = Atom.fromString(tmp[0])        
        if len(tmp) > 1:
            for literalString in tmp[1].split('^'):
                newRule.body.append(Literal.fromString(literalString))
        return newRule
    
    @classmethod
    def fromCompositeString(self, string):
        newRule = Rule()
        newRule.head = Atom.fromString(string.split(':-')[0])
        body = string.split(':-')[1].replace(' ', '')
        expressions = nestedExpr('[', ']').parseString(body).asList()
        (notused, rules) = Rule.compositeToBasicRules(newRule.head.pred, expressions[0], varOrder = ','.join(newRule.head.args))
        return reversed(rules)
    
    @classmethod
    def compositeToBasicRules(self, pred, body, varOrder = None):
        variables = set()
        rules = []
        rule = Rule()
        passOperator = ''
        for literal in body:
            newLiteral = None        
            if isinstance(literal, string_types):
                for literalString in literal.split('^'):
                    if re.match('[!#]?[a-z]+[_0-9\([a-zA-Z,]+\)]?' , literalString):
                        newLiteral = Literal.fromString(literalString)
                        rule.body.append(newLiteral)
                        variables = variables.union(newLiteral.vars())
                    elif re.match('[!#]', literalString):
                        passOperator = literalString
            else:            
                freshPred = freshPredicate()
                (newLiteralVars, newLiteralRules) = Rule.compositeToBasicRules(freshPred, literal)
                rules += newLiteralRules
                newLiteral = Literal.fromString( passOperator + freshPred + '(' + ','.join(newLiteralVars) + ')')
                rule.body.append(newLiteral)
                variables = variables.union(newLiteral.vars())
                passOperator = ''
        if varOrder is not None:
            rule.head = Atom.fromString(pred + '(' + varOrder + ')')        
        else:
            rule.head = Atom.fromString(pred + '(' + ','.join(map(str, variables)) + ')')
        rules.append(rule)  
        return (variables, rules)
        
    #String constructor for a rule with an empty body
    @classmethod
    def fromAtoms(self, atom, body):
        newRule = Rule()
        newRule.head = atom
        newRule.body = body
        return newRule
    
    def isGround(self):
        for lit in self.body:
            if not lit.isGround():
                return False
        return True
    
    def getCopy(self):
        copyRule = Rule()
        copyRule.head = self.head.getCopy()
        copyRule.body = []
        for lit in self.body:
            copyRule.body.append(lit.getCopy())
        return copyRule
    
    def replaceArg(self, old, new):
        self.head.replaceArg(old, new)
        for literal in self.body:
            literal.replaceArg(old, new)
            
    def vars(self):
        variables = self.head.vars()
        for l in self.body:
            variables = variables.union(l.vars())
        return variables
    
    def consts(self):
        constants = self.head.consts()
        for l in self.body:
            constants = constants.union(l.consts())
        return constants
    
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (self.head, self.body) == (other.head, other.body)      
            
    def __str__(self):
        string = str(self.head) + ' :- '
        if self.body is not None:
            string = string + ' ^ '.join(map(str, self.body))
        return string    
    
    def toDatalog(self, v):
        string = self.head.toDatalog(v) + ' :- '
        if self.body is not None:
            string += ', '.join([literal.toDatalog(v) for literal in self.body])
        return string    
