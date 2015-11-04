'''
Created on Nov 3, 2015

@author: galarwen
'''
import ply.lex as lex
from ply.lex import TOKEN
import re
import itertools as iter

#reserved words:
reservedWords = {
    'CLASSIFIER': ['svc\(\)','dtc\(\)', 'nnc\(\)'],
    'CLASSIFIER_METHOD': ['getErrorRate\(\)', 'saveErrorRate\(\)', 'predict', 'execute\(\)'],
    'COMMENT': ['#'],
    'INT':'int',
    'CROSSVALIDATION_VAR':['doCrossValidation', 'k_foldd']
}

#list of token names
tokens = [
          
] + list(reservedWords)#+ list(iter.chain.from_iterable(reservedWords.values())) 

literals = ['(',')','{','}']
#------------------------------------------------------
#        REG DECLARATIONS - @TOKEN DECORATORS
#------------------------------------------------------
reg_classifiers = re.compile('|'.join(reservedWords['CLASSIFIER']))
reg_classifiers_methods = re.compile('|'.join(reservedWords['CLASSIFIER_METHOD']))
reg_crossvalidation = re.compile('|'.join(reservedWords['CROSSVALIDATION_VAR']))


#------------------------------------------------------
#        SIMPLE TOKEN DEFINITION
#----------------------------------------------------
t_ignore = ' \t'
#------------------------------------------------------
#        TOKEN DEFINITION WITH FUNCTION
#------------------------------------------------------
#Rule for classifiers:
@TOKEN(reg_classifiers.pattern)
def t_CLASSIFIER(t):
    return(t)

#RULE for classifier methods:
@TOKEN(reg_classifiers_methods.pattern)
def t_CLASSIFIER_METHOD(t):
    return(t)

#RULE FOR CROSSVALIDATION VARIABLES:
@TOKEN(reg_crossvalidation.pattern)
def t_CROSSVALIDATION_VAR(t):
    return t
# Define a rule so we can track line numbers 
def t_newline(t):     
    r'\n+'     
    t.lexer.lineno += len(t.value)

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t
#Comment
def t_COMMENT(t):
    r'\#.*'
    pass #como no devuelve nada ignora
    #return(t)

#error handling, encuentra el error y sigue como si nada
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
 #------------------------------------------------------
#        EXTRA FUNCTIONS
#------------------------------------------------------   
# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


#test
data2test = """
svc()dtc()DTC()SvC() doCrossValidation execute() #hola 
svc()965
"""
lexer = lex.lex(reflags=re.UNICODE|re.IGNORECASE)
lexer.input(data2test)
for tok in lexer:
    print tok


print 'llego al final'