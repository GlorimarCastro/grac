import ply.lex as lex
from ply.lex import TOKEN
import re

#reserved words:
reservedWords = {
    'CLASSIFIER'  : ['svc\(\)','dtc\(\)', 'nnc\(\)'],
    'CLASSIFIER_METHOD': ['getErrorRate\(\)', 'saveErrorRate\(\)', 'predict', 'execute\(\)'],
    'COMMENT': ['#'],
    'INT':'int',
    'CROSSVALIDATION_VAR':['doCrossValidation', 'k_foldd'],
    'UPLOAD_COMMAND':['uploadTrainingData', 'uploadTestData', 'uploadData'],
    'CSV_VAR':['hasHeader','classColumn','featuresColumns','saveResult'],
    'BOOLEAN':['true', 'false'],
    'ALL': 'all'

}

#list of token names
tokens = [
       'PATH'   
] + list(reservedWords)#+ list(iter.chain.from_iterable(reservedWords.values())) 

literals = ['(',')','{','}', '=']
#------------------------------------------------------
#        REG DECLARATIONS - @TOKEN DECORATORS
#------------------------------------------------------
reg_classifiers = re.compile('|'.join(reservedWords['CLASSIFIER']))
reg_classifiers_methods = re.compile('|'.join(reservedWords['CLASSIFIER_METHOD']))
reg_crossvalidation = re.compile('|'.join(reservedWords['CROSSVALIDATION_VAR']))
reg_uploadcommand = re.compile('|'.join(reservedWords['UPLOAD_COMMAND']))
reg_csvvar = re.compile('|'.join(reservedWords['CSV_VAR']))
reg_boolean = re.compile('|'.join(reservedWords['BOOLEAN']))
#------------------------------------------------------
#        SIMPLE TOKEN DEFINITION
#----------------------------------------------------
t_ignore = ' \t'
t_ALL = r'all'
#------------------------------------------------------
#        TOKEN DEFINITION WITH FUNCTION
#------------------------------------------------------
def t_PATH(t):
    r'\"(.+?)\"'
    return t
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

@TOKEN(reg_csvvar.pattern)
def t_CSV_VAR(t):
    return t

@TOKEN(reg_boolean.pattern)
def t_BOOLEAN(t):
    return t
#rule for upload
@TOKEN(reg_uploadcommand.pattern)
def t_UPLOAD_COMMAND(t):
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

#=========================================================================
#test
#=========================================================================
data2test = """
svc()dtc()DTC()"SvC()" doCrossValidation execute() #hola 
svc()965() all true
uploadData
hasHeader
"""
lexer = lex.lex(reflags=re.UNICODE|re.IGNORECASE)
lexer.input(data2test)
for tok in lexer:
    print tok


print 'llego al final'