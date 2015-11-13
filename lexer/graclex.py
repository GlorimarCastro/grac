import ply.lex as lex
from ply.lex import TOKEN
import re

#reserved words:
#crear CSV_Method = saveresult() y borrarlo de CSV_VAR
reservedWords = {
    'CLASSIFIERS'  : ['svc\(\)','dtc\(\)', 'gnbc\(\)'],
    'CLASSIFIER_METHOD': ['getErrorRate\(\)', 'saveErrorRate\(\)',  'execute\(\)','calcBestClassifier\(\)'],
    'COMMENT': ['#'],
    'INT': 'int',
    'UPLOAD_COMMAND':['uploadTrainingData', 'uploadTestData', 'uploadData'],
    'BOOLEAN':['true', 'false'],
    'ALL': ['all'],
    'PRINT': ['printBestClassifier\(\)','printClassifiersComparitions\(\)'],
    'STATISTICS': ['mean','avg','min','max','mode','least','rndm','count','stdev'],
    'GRAC_START': ['grac'],
    'KFOLD': ['k_fold'],
    'CROSSVALIDATIONACTION': ['doCrossValidation'],
    'CSV_HEADER': ['hasheader'],
    'CSV_CLASSCOLUMN': ['class_column'],
    'CSV_TESTCLASSCOLUMN': ['test_class_column'],
    'CSV_FEATURESCOLUMNS': ["features_columns"],
    'CSV_TESTFEATURESCOLUMNS': ['test_features_column'],
    'CSV_SAVERESULT': ['saveResult'],
    'CLASSIFIER_METHOD_WPARAMETER': ['predict']

}

#list of token names
tokens = [
        'PATH',
        'ID',
] + list(reservedWords)#+ list(iter.chain.from_iterable(reservedWords.values())) 

literals = ['(',')','{','}', '=', ',', ';', '[', ']']
#------------------------------------------------------
#        REG DECLARATIONS - @TOKEN DECORATORS
#------------------------------------------------------
reg_classifiers = re.compile('|'.join(reservedWords['CLASSIFIERS']))
reg_classifiers_methods = re.compile('|'.join(reservedWords['CLASSIFIER_METHOD']))
reg_uploadcommand = re.compile('|'.join(reservedWords['UPLOAD_COMMAND']))
reg_boolean = re.compile('|'.join(reservedWords['BOOLEAN']))
reg_print = re.compile('|'.join(reservedWords['PRINT']))
reg_statistics = re.compile('|'.join(reservedWords['STATISTICS']))
reg_featurescolumn = re.compile(reservedWords.get('CSV_FEATURESCOLUMNS')[0])
reg_classcolumn = re.compile(reservedWords.get('CSV_CLASSCOLUMN')[0])
reg_testfeaturescolumn = re.compile(reservedWords.get('CSV_TESTFEATURESCOLUMNS')[0])
reg_testclasscolumn = re.compile(reservedWords.get('CSV_TESTCLASSCOLUMN')[0])
#------------------------------------------------------
#        SIMPLE TOKEN DEFINITION
#----------------------------------------------------
t_ignore                        = ' \t'
t_ALL                           = reservedWords.get('ALL')[0]
t_GRAC_START                    = reservedWords.get('GRAC_START')[0]
t_KFOLD                         = reservedWords.get('KFOLD')[0]
t_CROSSVALIDATIONACTION         = reservedWords.get('CROSSVALIDATIONACTION')[0]
t_CSV_HEADER                    = reservedWords.get('CSV_HEADER')[0]
t_CSV_SAVERESULT                = reservedWords.get('CSV_SAVERESULT')[0]
t_CLASSIFIER_METHOD_WPARAMETER  = reservedWords.get('CLASSIFIER_METHOD_WPARAMETER')[0]
#------------------------------------------------------
#        TOKEN DEFINITION WITH FUNCTION
#------------------------------------------------------
@TOKEN(reg_featurescolumn.pattern)
def t_CSV_FEATURESCOLUMNS(t):   
    return t

@TOKEN(reg_classcolumn.pattern)
def t_CSV_CLASSCOLUMN(t):
    return t
@TOKEN(reg_testfeaturescolumn.pattern)
def t_CSV_TESTFEATURESCOLUMNS(t):
    return t

@TOKEN(reg_testclasscolumn.pattern)
def t_CSV_TESTCLASSCOLUMN(t):
    return t

def t_PATH(t):
    r'\"(.+?)\"'
    return t

#Rule for classifiers:
@TOKEN(reg_classifiers.pattern)
def t_CLASSIFIERS(t):
    return(t)

#RULE for classifier methods:
@TOKEN(reg_classifiers_methods.pattern)
def t_CLASSIFIER_METHOD(t):
    return(t)


@TOKEN(reg_boolean.pattern)
def t_BOOLEAN(t):
    return t
#rule for upload
@TOKEN(reg_uploadcommand.pattern)
def t_UPLOAD_COMMAND(t):
    return t
@TOKEN(reg_print.pattern)
def t_PRINT(t):
    return t
@TOKEN(reg_statistics.pattern)
def t_STATISTICS(t):
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



#DEFINIR EL "ID" AL FINAL
def t_ID(t):
    r'[a-zA-Z]+'
    for key in reservedWords:
        for value in reservedWords.get(key):
            if t.value.lower() == value.lower():
                t.type = key
    return t
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
printClassifiersComparitions()
printBestClassifier()
calcBestClassifier()
mean
avg
dimelou

"""


lexer = lex.lex(reflags=re.UNICODE|re.IGNORECASE)
"""
lexer.input(data2test)
for tok in lexer:
    print tok


print 'llego al final'
"""
