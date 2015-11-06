import ply.yacc as yacc
import graclex

tokens = graclex.tokens

def p_method(t):
    'method : CLASSIFIER'
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


def p_clasification(t):
    'clasification : CLASSIFIER_METHOD'
    t[0] = t[1]
    if t[1] == "getErrorRate()":
        #execute getErrorRate
        pass
    elif t[1] == "saveErrorRate()":
        #execute saveErrorRate
        pass
    elif t[1] == "predict":
        #execute predict
        pass
    elif t[1] == "execute()":
        #execute execute
        pass

def p_crossValidation(t):
    '''crossValidation : CROSSVALIDATION_VAR '=' bool
                       | CROSSVALIDATION_VAR '=' kfold'''


def p_kfold(t):
    "kfold : '(' num ',' num ')'"
    t[0] = t[1]

def p_uploadFile(t):
    "uploadFile : UPLOAD_COMMAND '(' upload ')'"
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

def p_upload(t):
    'upload : PATH'
    t[0] = t[1]

def p_csv(t):
    '''csv : CSV_VAR '=' bool
          | CSV_VAR '=' '(' num ',' num ')'
          | CSV_VAR '=' '(' num ')'
          | CSV_VAR '(' upload ')' '''

def p_num(t):
    'num : INT'
    t[0] = t[1]

def p_bool(t):
    'bool : BOOLEAN'
    t[0] = t[1]

def p_printResults(t):
    'printResults : PRINT'
    t[0] = t[1]
    if t[1] == "printBestClassifier()":
        #execute printBestClassifier
        pass
    elif t[1] == "printClassifiersComparitions()":
        #execute printClassifiersComparitions
        pass



data2test = """
9
"""

y = yacc.yacc()
result = y.parse(data2test)
print(result)
