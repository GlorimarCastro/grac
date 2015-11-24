import ply.yacc as yacc
import lexer.graclex as graclex
from scipy import stats
import random, csv, os
import numpy
import sys
from audioop import avg
tokens = graclex.tokens

#grac static variable

global k_fold,  hasHeader, classColumn, featuresColumn, variables, trainingDataFilePath, testDataFilePath, statDataFilePath, stat, trainingData, testData, statData
global classifier, cv_fold_result, cv_scoring, classifiers
classifiers = ['svc', 'dtc', 'gnbc']
k_fold = 5
hasHeader = False
classColumn = 0
featuresColumn = [1]
testClassColumn = None
testFeaturesColumn = None
variables = {}
trainingDataFilePath = None
testDataFilePath = None
statDataFilePath = None
trainingData = None
testData = None
statData = None
classifier = None
#result variables
classResult = None      #un array simple con cada resultado de la prediccion
stat = {}               #un diccionario de la siguiente forma {'mean': result, 'avg': result ...}
cv_fold_result = {}     #si el usuario hace un cross validation cada este diccionario sera {fold1: truth': y_test, 'prediction': y_predicted, fold2: ...}
cv_scoring = {}         #si el usuario ejecuta cv sera un diccionario con la siguiente forma: {fold1: {'accuracy': float, ..}, fold2: {'accuracy': float, ..}, ... avg scoring: {}}

#start
def p_programm(p):
    '''program : GRAC_START '{'  statement_list '}' '''  
    print "comenzo programa"
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

#inicializa la variable global classifier con el classificador que el usuario haya escrito
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
#aun hay que cambiar el predict a que trabaje con lo que el usuario haya indicado
def p_classifier_methods(t):
    '''classifier_methods : CLASSIFIER_METHOD
                            | CLASSIFIER_METHOD_WPARAMETER '(' ')' '''
    t[0] = t[1]
    global classifier, classResult, testClassColumn, testFeaturesColumn
    #si es un methodo que requiere parametro se ejecuta en el if
    if len(t) > 2:
        if t[1].lower() == "predict":
            verifyTestData()
            verifyClassifier()
            #execute predict
            if testClassColumn == None:
                testClassColumn = classColumn
            if testFeaturesColumn == None:
                testFeaturesColumn = featuresColumn
            
            featuresVect = testData[: ,testFeaturesColumn]
            classResult =  classifier.predict(featuresVect)
            print "Result:"
            print classResult
    else:
        if t[1].lower() == "getcverrorrate()":
            #execute getErrorRate
            if  len(cv_scoring) > 0:
                print "Avg scoring for the cross-validation:"
                print "Accuracy: ", cv_scoring['avg scorinmg']['accuracy'], " Precision: ", cv_scoring['avg scorinmg']['precision'], " Recall: ", cv_scoring['avg scorinmg']['recall'], "F-score ", cv_scoring['avg scorinmg']['fscore']
            else:
                print "No cross-validation scoring on system"                
        elif t[1].lower() == "execute()":
            verifyClassifier()
            verifyTrainingData()
            global lastmethod
            lastmethod = "execute"
            features = trainingData[:,featuresColumn]
            classVector = trainingData[:,classColumn]
            classifier.fit(features, classVector)
            
        elif t[1].lower() == "executecv()":
            verifyClassifier()
            verifyTrainingData()
            lastmethod = "executecv"
            from sklearn.cross_validation import LabelKFold #no poermite overlaping
            print "============================================"
            print "Doing Cross-Validation: "
            features = trainingData[:,featuresColumn]
            classVector =trainingData[:,classColumn]
            label = numpy.array(range(len(classVector)))
            lkf = LabelKFold(label, k_fold)
            #
            iterationNum = 0
            #scoring avg:
            accuracyAvg = 0
            precisionAvg = 0
            recallAvg = 0
            fbetaScoreAvg = 0
            for train_ind, test_ind in lkf:
                X_train, X_test = features[train_ind], features[test_ind]
                y_train, y_test = classVector[train_ind], classVector[test_ind]
                from sklearn.metrics import confusion_matrix, accuracy_score, precision_recall_fscore_support
                
                classifier.fit(X_train, y_train)
                y_predicted = classifier.predict(X_test)
                
                #scoring 
                accuracy = accuracy_score(y_test, y_predicted)
                scoreResult = precision_recall_fscore_support(y_test, y_predicted, beta = 1.0, average = 'micro')
                precision = scoreResult[0]
                recall = scoreResult[1]
                fbetaScore = scoreResult[2]
                cm = confusion_matrix(y_test, y_predicted)
                
                #adding to avg
                accuracyAvg = accuracyAvg + accuracy
                precisionAvg = precisionAvg + precision
                recallAvg = recallAvg  + recall
                fbetaScoreAvg = fbetaScoreAvg + fbetaScore
            
                #adding result
                cv_fold_result['fold_' + str(iterationNum)] = {'truth': y_test, 'prediction': y_predicted}
                cv_scoring['fold_' + str(iterationNum)] = {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'fscore': fbetaScore, 'confusion matrix': cm}
                print "---------------------------------------"
                print "For fold ", iterationNum
                print "Confusion matrix is:"
                print confusion_matrix(y_test, y_predicted)
                print "Accuracy: ", accuracy, " Precision: ", precision, " Recall: ", recall, 'F-score', fbetaScore
                
                iterationNum = iterationNum + 1
            accuracyAvg = accuracyAvg / k_fold
            precisionAvg = precisionAvg / k_fold
            recallAvg = recallAvg / k_fold
            fbetaScoreAvg = fbetaScoreAvg / k_fold
            cv_scoring['avg scorinmg'] = {'accuracy': accuracyAvg, 'precision': precisionAvg, 'recall': recallAvg, 'fscore': fbetaScoreAvg}
            print "---------------------------------------"
            print "Avg scoring:"
            print "Accuracy: ", accuracyAvg, " Precision: ", precisionAvg, " Recall: ", recallAvg, "F-score ", fbetaScoreAvg

#Done
#esto se encarga de inicializar la variable global de data con la data que elk usuario subio.
#    trainingData: si elk usuario llama uploadTrainingData
def p_upload_methods(t):
    '''upload_methods : UPLOAD_COMMAND '(' PATH ')' '''
    t[0] = t[1]
    t[3] = t[3][1:-1] #para quitar las comillas
    if t[1].lower() == "uploadTrainingData".lower():
        global trainingDataFilePath, trainingData
        trainingDataFilePath = t[3]
        trainingData = uploadFile(t[3])
        print "Training data uploaded"
    elif t[1].lower() == "uploadTestData".lower():
        global testDataFilePath, testData
        testDataFilePath = t[3]
        testData = uploadFile(t[3])
        print "Test data uploaded"
    elif t[1].lower() == "uploaddata":
        global statData, statDataFilePath
        statDataFilePath = t[3]
        statData = uploadFile(statDataFilePath)
        print "Data uploaded"
    
#rafa
#aun hay que terminar esto
#falta asegurar que los file sean validos y que es un directorio
def p_csv_methods(p):
    ''' csv_methods : CSV_SAVERESULT '(' PATH ')' '''

    path = p[3][1:-1]

    if p[1].lower() == 'savePredResult'.lower():
        print "Prediction results are going to be saved in ", path
        #verifica que el path existe y el file es csv
        if not os.path.exists(p[3]):
            raise Exception('Cannot locate file.')

        if not p[3].lower().endswith('.csv'):
            raise Exception('Incorrect file extension.')

        if classResult == None:
            sys.exit("Classifier prediction have not being calculated")

        writer = open(path +'.csv', 'w')
        firstline = True
        for value in classResult:
            if firstline:
                firstline = False
                writer.write(str(value))
            writer.write("\n" + str(value))
        writer.close()

    elif p[1].lower() == 'saveStatResult'.lower():
        #verifica que el path existe y el file es csv
        if not os.path.exists(p[3]):
            raise Exception('Cannot locate file.')

        if not p[3].lower().endswith('.csv'):
            raise Exception('Incorrect file extension.')

        writer = csv.writer(open(p[3], 'wb'))

        for key, value in stat.items():
            writer.writerow([key, value])

    elif p[1].lower() == 'savecvresult'.lower():
        #verificar que el usuario te dio un directory path
        if len(cv_fold_result) < 1:
            sys.exit("Cross-validation have not being executed")
        if(not os.path.isdir(path)):
            sys.exit("Directory not found")
        #para cada fold creara el file
        for foldn in cv_fold_result:

            writer = csv.writer(open(path+'/'+str(foldn) + '.csv', 'wb')) #verificar que actually grabe dentro del directorio p[3]+ '\\' +
            writer.writerow(['truth' , 'prediction'])
            for i in range(len(cv_fold_result[foldn]['truth'])):
                writer.writerow([cv_fold_result[foldn]['truth'][i] , cv_fold_result[foldn]['prediction'][i]])

        #crea file para scoring
        f = open(path+'/'+'scoring.csv', 'wb')
        for foldn in cv_scoring:
            f.write(p[3] + foldn + ': ' + str(cv_scoring[foldn]))
            f.write("\n")


        
#glorimar
#done
def p_printResults(t):
    'printResults : PRINT'
    t[0] = t[1]
    if t[1].lower() == "printbestclassifier()":
        verifyTrainingData()
        from sklearn.cross_validation import LabelKFold #no poermite overlaping
        print "============================================"
        print "Calculating best Classifier: "
        features = trainingData[:,featuresColumn]
        classVector =trainingData[:,classColumn]
        label = numpy.array(range(len(classVector)))
        lkf = LabelKFold(label, k_fold)
        #
        iterationNum = 0
        #scoring avg:
        avgScoring = {'svc': {'accuracy': 0, 'precision': 0, 'recall': 0, 'fscore': 0, 'name': 'Support Vector Classifier'}, 'dtc': {'accuracy': 0, 'precision': 0, 'recall': 0, 'fscore': 0, 'name': 'Decision Tree Classifier'}, 'gnbc': {'accuracy': 0, 'precision': 0, 'recall': 0, 'fscore': 0, 'name': 'GaussianNB'}}

        for train_ind, test_ind in lkf:
            X_train, X_test = features[train_ind], features[test_ind]
            y_train, y_test = classVector[train_ind], classVector[test_ind]
            from sklearn.metrics import confusion_matrix, accuracy_score, precision_recall_fscore_support
            from sklearn import svm, tree
            from sklearn.naive_bayes import GaussianNB
            
            svc_prediction = svm.SVC().fit(X_train, y_train).predict(X_test) 
            dtc_prediction = tree.DecisionTreeClassifier().fit(X_train, y_train).predict(X_test) 
            gnbc_prediction = GaussianNB().fit(X_train, y_train).predict(X_test) 
            
            #scoring 
            scoreResult = precision_recall_fscore_support(y_test, svc_prediction, beta = 1.0, average = 'micro')
            avgScoring['svc']['accuracy'] = avgScoring['svc']['accuracy'] + accuracy_score(y_test, svc_prediction)
            avgScoring['svc']['precision'] = avgScoring['svc']['precision'] + scoreResult[0]
            avgScoring['svc']['recall'] = avgScoring['svc']['recall'] + scoreResult[1]
            avgScoring['svc']['fscore'] = avgScoring['svc']['fscore'] + scoreResult[2]
            
            scoreResult = precision_recall_fscore_support(y_test, dtc_prediction, beta = 1.0, average = 'micro')
            avgScoring['dtc']['accuracy'] = avgScoring['svc']['accuracy'] + accuracy_score(y_test, dtc_prediction)
            avgScoring['dtc']['precision'] = avgScoring['svc']['precision'] + scoreResult[0]
            avgScoring['dtc']['recall'] = avgScoring['svc']['recall'] + scoreResult[1]
            avgScoring['dtc']['fscore'] = avgScoring['svc']['fscore'] + scoreResult[2]
            
            scoreResult = precision_recall_fscore_support(y_test, gnbc_prediction, beta = 1.0, average = 'micro')
            avgScoring['gnbc']['accuracy'] = avgScoring['svc']['accuracy'] + accuracy_score(y_test, gnbc_prediction)
            avgScoring['gnbc']['precision'] = avgScoring['svc']['precision'] + scoreResult[0]
            avgScoring['gnbc']['recall'] = avgScoring['svc']['recall'] + scoreResult[1]
            avgScoring['gnbc']['fscore'] = avgScoring['svc']['fscore'] + scoreResult[2]
 
            iterationNum = iterationNum + 1
            
        scoreResult = precision_recall_fscore_support(y_test, svc_prediction, beta = 1.0, average = 'micro')
        avgScoring['svc']['accuracy'] = avgScoring['svc']['accuracy'] / k_fold
        avgScoring['svc']['precision'] = avgScoring['svc']['precision'] / k_fold
        avgScoring['svc']['recall'] = avgScoring['svc']['recall'] / k_fold
        avgScoring['svc']['fscore'] = avgScoring['svc']['fscore'] / k_fold
            
        scoreResult = precision_recall_fscore_support(y_test, dtc_prediction, beta = 1.0, average = 'micro')
        avgScoring['dtc']['accuracy'] = avgScoring['svc']['accuracy']/ k_fold
        avgScoring['dtc']['precision'] = avgScoring['svc']['precision'] / k_fold
        avgScoring['dtc']['recall'] = avgScoring['svc']['recall'] / k_fold
        avgScoring['dtc']['fscore'] = avgScoring['svc']['fscore'] / k_fold
            
        scoreResult = precision_recall_fscore_support(y_test, gnbc_prediction, beta = 1.0, average = 'micro')
        avgScoring['gnbc']['accuracy'] = avgScoring['svc']['accuracy'] / k_fold
        avgScoring['gnbc']['precision'] = avgScoring['svc']['precision']/ k_fold
        avgScoring['gnbc']['recall'] = avgScoring['svc']['recall'] / k_fold
        avgScoring['gnbc']['fscore'] = avgScoring['svc']['fscore'] / k_fold

        #calculate best one
        bestclassifier = {'accuracy': 0, 'name': []}
        """
        if avgScoring['svc']['accuracy'] < avgScoring['dtc']['accuracy']:
            bestclassifier[0] = 'Decision Tree'
        else:
            bestclassifier.append('Decision Tree')
            """
        for key in avgScoring:
            if avgScoring[key]['accuracy'] > bestclassifier['accuracy']:
                bestclassifier['accuracy'] = avgScoring[key]['accuracy']
                bestclassifier['name'] = [avgScoring[key]['name']]
            elif avgScoring[key]['accuracy'] ==  bestclassifier['accuracy']:
                bestclassifier['accuracy'] = avgScoring[key]['accuracy']
                bestclassifier['name'].append(avgScoring[key]['name'])
        
        print "Best Classifier(s): ", ','.join(bestclassifier['name']), ". With an accuracy of: ", (bestclassifier['accuracy'] * 100), "%"
            
        

#carlos
#imprimir resultados al terminal

def p_statistics_methods(p):
    '''statistics_methods : STATISTICS '(' ID ')' 
                            | STATISTICS '(' INT ')' 
                            | STATISTICS '(' array_list ')' '''
    global stat

    #PARA INT
    if isinstance(p[3], int):

        if p[1] == 'count':
            temp = 0
            for e in statData[:,p[3]]:
                temp += 1
            stat['count'] = temp
            print("count = "+str(stat['count']))

        if p[1] == 'min':

            stat['min'] = min(statData[:,p[3]])
            print("min = "+str(stat['min']))

        if p[1] == 'max':

            stat['max'] = max(statData[:,p[3]])
            print("max = "+str(stat['max']))
        if p[1] == 'rndm':

            stat['rndm'] = random.choice(statData[:,p[3]])
            print("random number = "+str(stat['rndm']))
        if p[1] == 'least':
            # Tally occurrences of numbers in a list
            cnt = {}
            result = []
            #initialize dictionary with counts=0
            x = statData[:,p[3]]
            for n in x:
                cnt[n] = 0
            #link keys with their counts
            for w in [statData[:,p[3]]]:
                cnt[w] += 1
            #get min
            mini = len(cnt)
            #print min
            for c in cnt:
                if cnt[c] < mini:
                    mini = cnt[c]

            #prints keys with the lowest counts
            for e in cnt:
                if cnt[e] == mini:
                    result.append(e)
            stat['least'] = result
            print("least repeated number = "+str(stat['least']))

        if p[1] == 'mode':

            if statData.ndim == 1:
                x,y = stats.mode(statData[:])
                stat['mode'] = "Valor mas repetido: " + str( x[0]) +  ". Se repitio: " +  str(y[0]) 
                print("mode = ", stat['mode'])
            else:
                x,y = stats.mode(statData[:,p[3]])
                stat['mode'] = "Valor mas repetido: " + str( x[0]) +  ". Se repitio: " +  str(y[0]) 
                print("mode = ", stat['mode'])

        if p[1] == 'stdev':
            if statData.ndim == 1:
                stat['stdev'] = numpy.std(statData[:])
                print("standard deviation = "+stat['stdev'])
            else: 
                stat['stdev'] = numpy.std(statData[:,p[3]])
                print("standard deviation = "+stat['stdev'])

        if p[1] == 'avg':
            stat['avg'] = numpy.mean(statData[:,p[3]])
            print("average = "+str(stat['avg']))

        if p[1] == 'mean':
            stat['mean'] = numpy.mean(statData[:,p[3]])
            print("mean = ", stat['mean'])


    #PARA list
    elif isinstance(p[3], list):

        if p[1] == 'count':
            temp = 0
            for e in p[3]:
                temp += 1
            stat['count'] = temp
            print("count = "+str(stat['count']))

        if p[1] == 'min':

            stat['min'] = min(p[3])
            print("min = "+str(stat['min']))

        if p[1] == 'max':

            stat['max'] = max(p[3])
            print("max = "+str(stat['max']))

        if p[1] == 'rndm':

            stat['rndm'] = random.choice(p[3])
            print("random number = "+str(stat['rndm']))
        if p[1] == 'least':
            # Tally occurrences of numbers in a list
            cnt = {}
            result = []
            #initialize dictionary with counts=0
            x = p[3]
            for n in x:
                cnt[n] = 0
            #link keys with their counts
            for w in [p[3]]:
                cnt[w] += 1
            #get min
            mini = len(cnt)
            #print min
            for c in cnt:
                if cnt[c] < mini:
                    mini = cnt[c]

            #prints keys with the lowest counts
            for e in cnt:
                if cnt[e] == mini:
                    result.append(e)
            stat['least'] = result
            print("least repeated number = "+str(stat['least']))

        if p[1] == 'mode':
            stat['mode'] = stats.mode(p[3])
            print("mode = "+str(stat['mode']))

        if p[1] == 'stdev':
            stat['stdev'] = numpy.std(p[3])
            print("standard deviation = "+str(stat['stdev']))

        if p[1] == 'avg':
            stat['avg'] = numpy.mean(p[3])
            print("average = "+str(stat['avg']))

        if p[1] == 'mean':
            stat['mean'] = numpy.mean(p[3])

            print("mean = "+ str(stat['mean']))

    else:
        global variables
        if p[3] in variables:
            if p[1] == 'count':
                temp = 0
                for e in variables[p[3]]:
                    temp += 1
                stat['count'] = temp
                print("count = "+str(stat['count']))

            if p[1] == 'min':

                stat['min'] = min(variables[p[3]])
                print("min = "+str(stat['min']))

            if p[1] == 'max':

                stat['max'] = max(variables[p[3]])
                print("max = "+str(stat['max']))

            if p[1] == 'rndm':

                stat['rndm'] = random.choice(variables[p[3]])
                print("random number = "+str(stat['rndm']))

            if p[1] == 'least':
                ###TESTING LEAST FREQUENT ALGORITHM
                # Tally occurrences of numbers in a list
                cnt = {}
                result = []
                x = variables[p[3]]
                #initialize dictionary with counts=0
                for n in x:
                    cnt[n] = 0
                #link keys with their counts
                for w in x:
                    cnt[w] += 1
                #get min
                mini = len(cnt)
                #print min
                for c in cnt:
                    if cnt[c] < mini:
                        mini = cnt[c]

                #prints keys with the lowest counts
                for e in cnt:
                    if cnt[e] == mini:
                        result.append(e)
                stat['least'] = result
                print("least repeated number = "+str(stat['least']))

            if p[1] == 'mode':
                stat['mode'] = stats.mode(variables[p[3]])
                print("mode = "+str(stat['mode']))

            if p[1] == 'stdev':
                stat['stdev'] = numpy.std(variables[p[3]])
                print("standard deviation = "+str(stat['stdev']))

            if p[1] == 'avg':
                stat['avg'] = numpy.mean(variables[p[3]])
                print("average = "+str(stat['avg']))

            if p[1] == 'mean':
                stat['mean'] = numpy.mean(variables[p[3]])
                print("mean = " + str(stat['mean']))


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
        print "esta entrando aqui"
        variables[p[1]] = p[3]
    
def p_crossvalidation_assignment(p):
    '''crossvalidation_assignment :  KFOLD '=' INT'''
    if isinstance(p[3], int):
        global k_fold
        if p[3] < 2:
            sys.exit("kFold should not be less than 2")
        k_fold = p[3]

def p_csv_assignment(p):
    '''csv_assignment : CSV_HEADER '=' BOOLEAN
                        | CSV_CLASSCOLUMN '=' INT
                        | CSV_FEATURESCOLUMNS '=' array_list
                        | CSV_TESTCLASSCOLUMN '=' INT
                        | CSV_TESTFEATURESCOLUMNS '=' array_list'''
    if isinstance(p[3], int):
        if p[1].lower() == 'class_column':               
            global classColumn
            print "Clas column set to ", p[3]
            classColumn = p[3]
        else:
            global testClassColumn
            print "Test class column set to ", p[3]
            testClassColumn = p[3]
    elif isinstance(p[3], list):
        if p[1].lower() == 'features_columns':
            global featuresColumn
            print "features columns now are: ", p[3]
            featuresColumn = p[3]
        else:
            global testFeaturesColumn
            print "testFeaturesColumn now are: ", p[3]
            testFeaturesColumn = p[3] 
    elif p[1].lower() == 'hasheader':
        global hasHeader
        print "Has header set to ", p[3]
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
    sys.exit("Sintax error in input")


#===============================================================================================================================
#                                                   Intermediate Code
#===============================================================================================================================

def uploadFile(csvfilepath):
    if not csvfilepath.lower().endswith('.csv'):
        raise Exception('Incorrect file extension.')
    else:
        try:
            if hasHeader == "true":
                print "entro a con header"
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
    
 
    def precision(predictedVector, truthVector):
        pass
    
    def recall(predictedVector, truthVector):
        pass
    
    def hharmonicMean(predictedVector, truthVector):
        pass
        
def getParser():
    return yacc.yacc()

#===============================================================================================================================
#                    TEST                        TEST                        TEST                        TESTs
#===============================================================================================================================

 
data2test = """
grac{
hasHeader = false;
features_columns = [1,2,3,4,5];
uploadTrainingData("../example/dumytry.csv");
uploadTestData("../example/gracDumyData.csv");
dtc();
execute();#this calculare matrix values for svc 
predict();
savePredResult("dtcResult")
}
"""

#y = yacc.yacc()
#result = y.parse(data2test)
#print "termino"
 


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

