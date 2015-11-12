import ply.yacc as yacc
import lexer.graclex as graclex
from scipy import stats
import random, csv
import numpy
import sys
from sklearn.base import ClassifierMixin
tokens = graclex.tokens

#grac static variable
global k_fold, doCrossValidation, hasHeader, classColumn, featuresColumn, variables, trainingDataFilePath, testDataFilePath, statDataFilePath, stat, trainingData, testData, statData
global classifier, statLast
k_fold = 5
doCrossValidation = False
hasHeader = False
classColumn = 0
featuresColumn = [1]
variables = {}
trainingDataFilePath = None
testDataFilePath = None
statDataFilePath = None
trainingData = None
testData = None
statData = None
classifier = None
stat = {}
classResult = None
statLast = None

#start
def p_programm(p):
    '''program : GRAC_START '{'  statement_list '}' '''
    p[0] = p[3]
def p_statement_list(p):
    '''statement_list : statement
                        | statement ';' statement_list'''
    if len(p) > 2:
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
def p_method(p):
    '''method : classifier
                | classifier_methods
                | upload_methods
                | csv_methods
                | printResults
                | statistics_methods'''
    p[0] = p[1]

#GLORIMAR
def p_classifier(t):
    'classifier : CLASSIFIERS'
    t[0] = t[1]
    global classifier, statLast
    statLast = False
    if t[1] == "svc()":
        #execute svm
        verifyTrainingData()
        from sklearn import svm
        classifier = svm.SVC()
    elif t[1] == "dtc()":
        #execute dtc
        verifyTrainingData()
        from sklearn import tree
        classifier = tree.DecisionTreeClassifier()
        
    elif t[1] == "gnbc()":
        #execute gnvc
        verifyTrainingData()
        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
        
#GLORIMAR
def p_classifier_methods(t):
    '''classifier_methods : CLASSIFIER_METHOD
                            | CLASSIFIER_METHOD_WPARAMETER '(' ')' '''
    t[0] = t[1]
    global classifier, classResult
    #si es un methodo que requiere parametro se ejecuta en el if
    if len(t) > 2:
        if t[1] == "predict":
            #execute predict
            verifyTestData()
            verifyClassifier()
            featuresVect = testData[: ,featuresColumn]
            classResult =  classifier.predict(featuresVect)
            print "Result:"
            print classResult
    else:
        if t[1] == "getErrorRate()":
            #execute getErrorRate
            pass
        elif t[1] == "saveErrorRate()":
            #execute saveErrorRate
            pass
        elif t[1] == "execute()":
            verifyClassifier()
            verifyTrainingData()
            
            features = trainingData[:,featuresColumn]
            classVector = trainingData[:,classColumn]
            classifier.fit(features, classVector)
            



def p_upload_methods(t):
    '''upload_methods : UPLOAD_COMMAND '(' PATH ')' '''
    t[0] = t[1]
    t[3] = t[3][1:-1] #para quitar las comillas
    if t[1].lower() == "uploadTrainingData".lower():
        global trainingDataFilePath, trainingData
        trainingDataFilePath = t[3]
        trainingData = uploadFile(t[3])
    
    elif t[1].lower() == "uploadTestData".lower():
        global testDataFilePath, testData
        testDataFilePath = t[3]
        testData = uploadFile(t[3])
        print "entro"
    elif t[1].lower() == "uploaddata":
        global statData, statDataFilePath
        statDataFilePath = t[3]
        statData = uploadFile(statDataFilePath)
        
    
#********************************************************************************************************************************************************************************************************************************************************
#rafa
#guardar variables de resultado en file en formato csv
#carlos - {methodo: result }
#glorimar - matriz
#path csv y existe
def p_csv_methods(t):
    ''' csv_methods : CSV_SAVERESULT '(' PATH ')' '''
    
    writer = csv.writer(open(t[3]+'.csv', 'wb'))
#writes statistics results
    for key, value in stat.items():
        writer.writerow([key, value])
        
#**********************************************************************************************************************************************************************************************************************************************************
#glorimar
def p_printResults(t):
    'printResults : PRINT'
    t[0] = t[1]
    if t[1] == "printBestClassifier()":
        #execute printBestClassifier
        pass
    elif t[1] == "printClassifiersComparitions()":
        #execute printClassifiersComparitions
        pass
#carlos
#resultado guardarlos en un dic global
#si el usuario no ha subido file error
#int = columna del file
#ID sacar de dict
# verificar que to-do exista
def p_statistics_methods(p):
    '''statistics_methods : STATISTICS '(' ID ')' 
                            | STATISTICS '(' INT ')' 
                            | STATISTICS '(' array_list ')' '''
    global stat, statLast
    statLast = True
    if isinstance(p[3], int):
        #WTF LOL
        pass
    elif isinstance(p[3], list):

        if p[1] == 'count':
            temp = 0
            for e in p[3]:
                temp += 1
            stat['count'] = temp

        if p[1] == 'min':

            stat['min'] = min(p[3])

        if p[1] == 'max':

            stat['max'] = max(p[3])

        if p[1] == 'rndm':

            stat['rndm'] = random.choice(p[3])

        if p[1] == 'least':
            # Tally occurrences of numbers in a list
            cnt = {}
            result = []
            #initialize dictionary with counts=0
            for n in [p[3]]:
                cnt[n] = 0
            #link keys with their counts
            for w in [p[3]]:
                cnt[w] += 1
            #get min
            min = len(cnt)
            #print min
            for c in cnt:
                if cnt[c] < min:
                    min = cnt[c]

            #prints keys with the lowest counts
            for e in cnt:
                if cnt[e] == min:
                    result.append(e)
            stat['least'] = result

        if p[1] == 'mode':
            stat['mode'] = stats.mode(p[3])
            ""
        if p[1] == 'stdev':
            stat['stdev'] = numpy.std(p[3])
        if p[1] == 'avg':
            stat['avg'] = numpy.mean(p[3])
        if p[1] == 'mean':
            stat['mean'] = numpy.mean(p[3])

    else:
        global variables
        if p[3] in variables:
            if p[1] == 'count':
                temp = 0
                for e in variables[p[3]]:
                    temp += 1
                stat['count'] = temp

            if p[1] == 'min':

                stat['min'] = min(variables[p[3]])

            if p[1] == 'max':

                stat['max'] = max(variables[p[3]])

            if p[1] == 'rndm':

                stat['rndm'] = random.choice(variables[p[3]])

            if p[1] == 'least':
                # Tally occurrences of numbers in a list
                cnt = {}
                result = []
                #initialize dictionary with counts=0
                for n in [variables[p[3]]]:
                    cnt[n] = 0
                #link keys with their counts
                for w in [variables[p[3]]]:
                    cnt[w] += 1
                #get min
                min = len(cnt)
                #print min
                for c in cnt:
                    if cnt[c] < min:
                        min = cnt[c]

                #prints keys with the lowest counts
                for e in cnt:
                    if cnt[e] == min:
                        result.append(e)
                stat['least'] = result

            if p[1] == 'mode':
                stat['mode'] = stats.mode(variables[p[3]])
            if p[1] == 'stdev':
                stat['stdev'] = numpy.std(variables[p[3]])
            if p[1] == 'avg':
                stat['avg'] = numpy.mean(variables[p[3]])
            if p[1] == 'mean':
                stat['mean'] = numpy.mean(variables[p[3]])

        else:
            print "Variable not defined"


#=====================================================================================
#            ASSIGNMENT RULES            ASSIGNMENT RULES
#=====================================================================================
def p_assignment(p):
    '''assignment : crossvalidation_assignment
                    | csv_assignment
                    | ID '=' array_list'''
    p[0] = p[1]
    if len(p) > 2:
        global variables
        variables[p[1]] = p[3]
    
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
    elif isinstance(p[3], list):
        global featuresColumn
        featuresColumn = p[3]
    else:
        global hasHeader
        hasHeader = p[3]

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
#                                                   Intermediate Code
#===============================================================================================================================

def uploadFile(csvfilepath):
    print csvfilepath
    if not csvfilepath.lower().endswith('.csv'):
        raise Exception('Incorrect file extension.')

    else:
        try:
            if hasHeader == "true":
                return numpy.loadtxt(open(csvfilepath,"rb"),delimiter=",",skiprows=1)
            else:
                return numpy.loadtxt(open(csvfilepath,"rb"),delimiter=",")
        except:
            raise Exception('Invalid path or file is corrupt.')
    return None

def verifyTrainingData():
    global trainingData
    if trainingData == None  :
            sys.exit("Trainind data have not being uploaded.")


def verifyTestData():
    global testData
    if testData == None  :
            sys.exit("Test data have not being uploaded.")

def verifyClassifier():
    if classifier == None:
        sys.exit("Classifier have not being initialized")
        
#===============================================================================================================================
#                    TEST                        TEST                        TEST                        TESTs
#===============================================================================================================================
data2test3 = ""
 
data2test = """
grac {
features_columns = [1,2,3,4];
hasHeader = false;
class_column = 0;
uploadTrainingData("dumyData.csv");
gnbc();
execute();
uploadTestData("testdata.csv\");
predict();
uploaddata("statdumy.csv")
}
"""

y = yacc.yacc()
result = y.parse(data2test)
print statData
 


#print random.choice([1,2,3,4,5,6,7,8,9,10])
#print stats

'''
###TESTING LEAST FREQUENT ALGORITHM
# Tally occurrences of numbers in a list
cnt = {}
result = []
#initialize dictionary with counts=0
for n in ['green','green','blue','blue','red','red','red','red']:
    cnt[n] = 0
#link keys with their counts
for w in ['green','green','blue','blue','red','red','red','red']:
    cnt[w] += 1
#get min
min = len(cnt)
#print min
for c in cnt:
    if cnt[c] < min:
        min = cnt[c]

#prints keys with the lowest counts
for e in cnt:
    if cnt[e] == min:
        result.append(e)

print result

'''

