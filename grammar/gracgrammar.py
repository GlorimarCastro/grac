import ply.yacc as yacc
import lexer.graclex as graclex

tokens = graclex.tokens

#grac static variable
global k_fold, doCrossValidation, hasHeader, classColumn, featuresColumn
k_fold = 5
doCrossValidation = False
hasHeader = False
classColumn = 0
featuresColumn = [1]



#start
def p_programm(p):
    '''program : GRAC_START '{'  statement_list '}' '''
    p[0] = p[3]
def p_statement_list(p):
    '''statement_list : statement
                        | statement ';' statement_list'''
    if len(p) > 2:
        #verificar que hacer cuando tenemos multiples lineas a ejecutarse
        p[0] = (p[1], p[3]) 
    else:
        p[0] = p[1]

def p_statement(p):
    '''statement : method 
                    | assignment'''
    p[0] = p[1]

#=====================================================================================
#            METHODS            METHODS
#=====================================================================================
#hay que terminar esto
def p_method(p):
    '''method : classifier
                | classifier_methods
                | upload_methods
                | csv_methods
                | printResults
                | statistics_methods'''
    p[0] = p[1]
    
def p_classifier(t):
    'classifier : CLASSIFIERS'
    t[0] = t[1]
    if t[1] == "svc()":
        #execute svm
        pass
    elif t[1] == "dtc()":
        #execute dtc
        pass
    elif t[1] == "nnc()":
        #execute nnc
        pass

def p_classifier_methods(t):
    '''classifier_methods : CLASSIFIER_METHOD
                            | CLASSIFIER_METHOD_WPARAMETER '(' PATH ')' '''
    t[0] = t[1]
    #si es un methodo que requiere parametro se ejecuta en el if
    if len(t) > 2:
        if t[1] == "predict":
            #execute predict
            pass
    else:
        if t[1] == "getErrorRate()":
            #execute getErrorRate
            pass
        elif t[1] == "saveErrorRate()":
            #execute saveErrorRate
            pass
        elif t[1] == "execute()":
            #execute execute
            pass
        pass


def p_upload_methods(t):
    '''upload_methods : UPLOAD_COMMAND '(' PATH ')' '''
    t[0] = t[1]
    if t[1] == "uploadTrainingData":
        #execute uploadTrainingData
        pass
    elif t[1] == "uploadTestData":
        #execute uploadTestData
        pass
    elif t[1] == "uploadData":
        #execute uploadData
        pass
    pass
  
def p_csv_methods(p):
    ''' csv_methods : CSV_SAVERESULT '(' PATH ')' '''
    pass
    
def p_printResults(t):
    'printResults : PRINT'
    t[0] = t[1]
    if t[1] == "printBestClassifier()":
        #execute printBestClassifier
        pass
    elif t[1] == "printClassifiersComparitions()":
        #execute printClassifiersComparitions
        pass
    
def p_statistics_methods(p):
    '''statistics_methods : STATISTICS '(' ID ')' 
                            | STATISTICS '(' INT ')' '''
    pass

#=====================================================================================
#            ASSIGNMENT RULES            ASSIGNMENT RULES
#=====================================================================================
def p_assignment(p):
    '''assignment : crossvalidation_assignment
                    | csv_assignment'''
    p[0] = p[1]
    
def p_crossvalidation_assignment(p):
    '''crossvalidation_assignment :  KFOLD '=' INT
                                    | CROSSVALIDATIONACTION '=' BOOLEAN'''
    if isinstance(p[3], int):
        global k_fold
        k_fold = p[3]
    else:
        global doCrossValidation
        doCrossValidation = p[3]

def p_csv_assignment(p):
    '''csv_assignment : CSV_HEADER '=' BOOLEAN
                        | CSV_CLASSCOLUMN '=' INT
                        | CSV_FEATURESCOLUMNS '=' array_list'''
    if isinstance(p[3], int):
        global classColumn
        classColumn = p[3]
    elif isinstance(p[3], bool):
        global hasHeader
        hasHeader = p[3]
    else:
        global featuresColumn
        featuresColumn = p[3]

def p_array_list(p):
    '''array_list : '[' list ']' '''
    p[0] = p[2]

def p_list(p):
    '''list : INT 
                | INT ',' list'''
    if len(p) > 2:
        if isinstance(p[3], list): 
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]] + [p[3]]
    else:
        p[0] = p[1]

#error handler, se debe de incluir una salida al programa
def p_error(p):
    print ("Sintax error in input")



#===============================================================================================================================
#                    TEST                        TEST                        TEST                        TESTs
#===============================================================================================================================
data2test3 = ""
 
data2test = """
grac { features_columns = [3 ,4 ,5,4,5,5,6,6,7]
}
"""

y = yacc.yacc()
result = y.parse(data2test3)
print doCrossValidation
print k_fold
print featuresColumn
print(result)
