# <a id="introduccion"> Introduction </a>

### <a id="description"> Description </a>
GRAC is a python based [special-purpose programming language] for [supervised machine learning] and [statistics]. It allows the user to upload CSV files and run classification methods, predictions and statistics on it.

### <a id="motivation"> Motivation </a>
Python and R are the most used languages for machine learning and data mining. Tools as Weka and Scikit-Learn have been created to facilitate machine learning, data mining, and big data analysis. Weka, however, is for Java programming and just work with attribute-relation file format (ARFF). Scikit-Learn is for Python but doesn't allow you to pre-process text data files. Also, Scikit-Learn requires a lot of dependencies (e.g. NumPy, SciPy, PyDot, etc.).  R is mainly for statistical computing and graphics, making machine learning algorithms hard to code. For these reasons, a new programming tool that converges all the benefits of Weka, Scikit-Learn, and R, but at the same time allow you to program in Python, is desired. Here we propose the creation of a new Python based programming language: GRAC.  GRAC is a programming language for machine learning, data mining and big data analysis that converges some of the benefits of Weka, Scikit-Learn, and R. At the same time GRAC allows you to pre-process text files and it let you use comma-separated values (CSV) files.

Machine learning, data mining and big data have been used for the advance in artificial intelligence, gene therapy, cybersecurity, bioinformatics, medical diagnosis, computer vision, and so on. Also, they have been used to improve financial trading, business processing, sport, law enforcement, telecommunication, search engines, terrorism detection, etc. A lot of different applications for machine learning, data mining and big data can be mentioned. For that reason, good tools for doing machine learning, data mining, and big data analysis are needed. As we presented before, different tools have been created already for these. We propose to add together all the benefits of these different tools in just one; being the main motivation to allow the users to work with CSV files (one of the most used format in the mentioned fields).  The main purpose of GRAC is to allow the users to just indicate the name of the CSV file and a list of actions, so the research can be accomplished faster.


### <a id="statSect"> Statistic Section </a>
The available methods for statitics are:
  - Mean 
  - Average
  - Maximun
  - Minimun
  - Mode
  - Least
  - Random
  - Count
  - Standard Deviation
 
### <a id="Mach"> Machine Learning Section </a>
For now, the machine learning classifiers available are supervised classifiers:
  - [Decision Tree]
  - [Support Vector Machine]
  - [Gaussian Naive Bayes]
  
Also, GRAC allows you to calculate the best classifier for your data (based on accuracy), and to execute [cross-validation]

## Version
1.0


---
# <a id="instal"> Installation </a>
## <a id="depende"> Dependecies </a>
GRAC uses a series of python packages, all listed in the requirement.txt file. To install this packages you can run the next command line in:
### Ubuntu:
```sh
$ python -m pip install -r requirements.txt
```
Make sure that you have the newest version of pip in your system, since Ubuntu has an outdated version of pip. Inside the dependecies folder you can find the python file get-pip.py, this file is for installing the newest version of pip. 
### Windows:
For windows, if you have Anaconda or Conda yo can run the next command line:
```sh
$ conda create -n new environment --file requirements.txt
```

If you don't have Anaconda or Conda, you can install all the dependencies using the next command lines:
```sh
$ python -m pip install numpy
$ python -m pip install scipy
$ python -m pip install ply
$ python -m pip pydot
$ python -m pip scikit-learn
```
If you get an error installing scikit-learn you should download the source file. Users with Python 2.7 can find an installer for scikit-learn in the dependecies folder.

## GRAC

To use GRAC you can clone this repository or you can download the zip file from the latest release. 

---

# <a id="example" >Example Section </a>
Examples of how to use GRAC can be found in the [examples] folder

---
# <a id="grammar"> Grac Grammar </a>
![alt tag](https://github.com/GlorimarCastro/grac/blob/master/imgs/gracgrammar.png?raw=tru)
----
----
# <a id="tutorial"> Language Tutorial </a>
The next video contain a tutorial and a description of GRAC:
- [https://www.youtube.com/watch?v=SGs17I4_cI8&feature=youtu.be]

Also, the user can go to the Reference Manual secction for detailed instruction in how to use the diferent methods of GRAC. 

----
# <a id="referencemanual"> Reference Manual </a>
## <a id="basicsyn"> Basic Syntax </a>
* Main Program: each GRAC program have to start with the GRAC special header
```sh
grac{
}
```
* Statement Separator:
    Each statement need to end with a semicolon ‘;’, except the last statement. 
```sh
grac{
hasheader = true;
t = 9
}
```
## <a id="types"> Types </a>
#### <a id="bool"> Booleans </a>
* Valid values: true | false
* Descriptions: Expresses a truth value. It can be either True or False. GRAC uses reserved boolean 
    variables to specify if CSV file contains header and/or to execute cross validation.
#### <a id="path"> Path </a>
* Valid Values: r'\"(.+?)\"' 
* Description:  a series of characters.  Path variables ares used in uploads methods to 
    specify paths for training and testing data files. Also, path variables are used to provide 
    a path to save GRAC results.
#### <a id="ints"> Integers </a>
* Valid Values: r'\d+'
* Description: integers are numbers that can be written without a fractional component. Integers are 
    used as array component in the following cross validation reserved variables to specify 
    the number of folds and number of columns to train/test: k_fold, class_column, 
    test_class_column, feature_columns and test_feature_column.

#### <a id="arra">Arrays</a>
* Description: an array is a container object that hold a fixed number of values of a single type. Arrays 
    are used to execute  statistics functions and to define cross validation reserved variables. 
    Only arrays of integers are allowed.

## <a id="varia">Variables</a>
#### <a id="kfold">kfold:</a>
* kfold - set the number of folds the k-fold cross-validation method will use. 
* Default Value: 5
* Accepted values/types: Integer
* example:
```sh
$ grac{
$    uploadTrainingData(“C:\path\to\file”);
$    kfold = 10;
$    gnbc();
$    executeCV();
$    saveCVResult(“path\to\output\file”)
$}
```

#### <a id="hasheader">hasheader:</a>
* hasheader - tells whether the first row should be ignored (is a header) or not.
* Default Value: False
* Accepted values/types: Boolean
* Example
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    features_columns = [1,2,52];
$    uploadTrainingData(“C:\path\to\file”);
$    gnbc();
$    execute()
$}
```

#### <a id="classcol">class_column</a>
* class_column - Identify and separates the column that holds the class from the features in the 
    training file. 
* Default Value: 0
* Accepted values/types: Integer
* Example
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    features_columns = [1,2,52];
$    uploadTrainingData(“C:\path\to\file”);
$    gnbc();
$    execute()
$}
```
#### <a id="testclacol">test_class_column</a>
* test_class_column - Identify the class column to be used for testing. If no value is set, it will copy the value from class_column.
* Default Value: None
* Accepted values/types: Integer
* Example:
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    test_class_column = 1;
$    features_columns = [1,2,52];
$    test_features_column = [2,5,8];
$    uploadTrainingData(“C:\path\to\file”);
$    uploadTestData(“C:\path\to\file”);
$    svc();
$    execute();
$    predict()
$}
```
#### <a id="feacolm"> features_columns</a>
* features_columns - Identify and separates the columns holding the features from the class.
* Default Value: [1]
* Accepted values/types: Array of Integers
* Example
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    features_columns = [1,2,52];
$    uploadTrainingData(“C:\path\to\file”);
$    gnbc();
$    execute()
$}
```
#### <a id="testfeatcolm">test_features_column</a>
* test_features_column - Identify the columns holding the features to be tested. If no value is set, it will copy the value from features_column.
* Default Value: None
* Accepted values/types: Array of Integers
* Example:
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    test_class_column = 1;
$    features_columns = [1,2,52];
$    test_features_column = [2,5,8];
$    uploadTrainingData(“C:\path\to\file”);
$    uploadTestData(“C:\path\to\file”);
$    svc();
$    execute();
$    predict()
$}
```

## <a id="functions">Functions</a>
### <a id="machinlearfun">Machine Learning</a>
#### <a id="svc">svc()</a>
* Parameters:
    No parameters needed.
* svc - set the Support Vector Machine classifiers as the classifier to 
    be used for any method that use a classifier
* Example
```sh
$ grac{
$     uploadTrainingData(“C:\path\to\file”);
$     svc();
$     execute()
$}
```
#### <a id="dtc">dtc()</a>
* Parameters
    No parameters needed.
* dtc - set the Decision Tree Classifier as the classifier to be used for 
    any method that use a classifier. 
* Example
```sh
$ grac{
$     uploadTrainingData(“C:\path\to\file”);
$     dtc();
$     execute()
$}
```
#### <a id="gnbc">gnbc()</a>
* Parameters
    No parameters needed.
* gnbc - set the Gaussian Naive Bayes Classifier as the classifier to 
    be used for any method that use a classifier
* Example
```sh
$ grac{
$     uploadTrainingData(“C:\path\to\file”);
$     gnbc();
$     execute()
$}
```

#### <a id="execute">execute() </a>
* Parameters:
    No parameter needed. But this method need that the user already 
    set the classifier to use and the training data.
* executeCV - fit the training data uploaded by the user, using the 
    specified classifier. 
* Example:
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    features_columns = [1,2,52];
$    uploadTrainingData(“C:\path\to\file”);
$    gnbc();
$    execute()
$}
```
#### <a id="execcv">executeCV()</a>
* Parameters:
    No parameter needed. But this method need that the user already 
    set the classifier to use and the training data.
* executeCV - do cross-validation using the classifier specified by 
    the user. The fold used by default is 5, but the user can change this 
    value assigning a different value to the kfold variable. 
* Example:
```sh
$ grac{
$    uploadTrainingData(“C:\path\to\file”);
$    kfold = 3;
$    gnbc();
$    executeCV();
$    saveCVResult(“path\to\output\file”)
$}
```
#### getCVErrorRate()
* Parameters:
    No parameter needed. Before using this method executeCV 
    method have to be used. 
* getCVErrorRate - print the accuracy, precision, recall and F-score 
    generated by the executeCV method. 
* Example:
```sh
$ grac{
$    uploadTrainingData(“C:\path\to\file”);
$    kfold = 3;
$    gnbc();
$    executeCV();
$    saveCVResult(“path\to\output\file”);
$    getCVErrorRate()
$}
```
#### printBestClassifier()
* Parameters:
    No parameters needed. But this method need that the user set the 
    data for training and the classifier to use, before using this method.  
* printBestClassifier - Based on accuracy decide between Support 
    Vector Machine, Gaussian Naivew Bayes and Decision Tree which 
    one is the best to use for the data given as training. The name for 
    the selected classifier is printed in the console.
* Example:
```sh
$ grac{
$    uploadTrainingData(“C:\path\to\file”);
$    printBestClassifier()
$    }
```
#### predict()
* Parameters:
    Non parameter needed. Before using this method the test data to 
    use have to be uploaded and execute() method have to be used. 
* Description:
    predict - using the fit result from execute(), make a prediction for 
    the test data uploaded by the user. 
* Example:
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    test_class_column = 1;
$    features_columns = [1,2,52];
$    test_features_column = [2,5,8];
$    uploadTrainingData(“C:\path\to\file”);
$    uploadTestData(“C:\path\to\file”);
$    svc();
$    execute();
$    predict()
$}
```

### Statistic
#### mean(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* mean - Calculates the average value (mean) of the elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    mean(x)
$  }
```
#### avg(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* avg - Calculates the average value (mean) of the elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    mean(x);
$    avg([1,2,3,4])
$  }
```
#### min(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* min - Calculates the smallest value of the elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    min(x)
$  }
```

#### max(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* max - Calculates the largest value of the elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    max(x)
$  }
```
#### mode(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* Description:
Calculates the most frequent value of the elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    mode(x)
$  }
```
#### least(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* Description:
Calculates the least frequent value of the elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    least(x)
$  }
```


#### rndm(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* Description:
Selects a random value of the elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    rndm(x)
$  }
```
#### count(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* Description:
Returns the amount of elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    count(x)
$  }
```
#### stdev(x)
* Parameters: 
The user can enter a variable containing the list of elements, specify a column on the input CSV file containing the elements, or a list of elements directly.
* Description:
Calculates the standard deviation of the elements entered.
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    stdev(x)
$  }
```


### Data Upload
#### uploadTrainingData()
* Parameters:
    The user must enter the path where the CSV file for training data is 
        located. The path must be valid and the file must be CSV type.
* Description:
    In order to train with any of the available classifiers, the training data file 
    must be uploaded before.
* Example:
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    test_class_column = 1;
$    features_columns = [1,2,52];
$    test_features_column = [2,5,8];
$    uploadTrainingData(“C:\path\to\file”);
$    svc();
$    execute();
 }
 ```
#### uploadTestData()
* Parameters
    The user must enter the path where the CSV file for test data is 
    located. The path must be valid and the file must be CSV type.
* uploadTestData - In order to predict data with any of the available classifiers, the test data 
    file must be uploaded before.
* Example
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    test_class_column = 1;
$    features_columns = [1,2,52];
$    test_features_column = [2,5,8];
$    uploadTrainingData(“C:\path\to\file”);
$    uploadTestData(“C:\path\to\file”);
$    svc();
$    execute();
$    predict()
$ }
```
#### uploadData()
* Parameters
    The user must enter the path where the CSV file is located. The path 
    must be valid and the file must be CSV type.
* uploadData - The  uploaded file contains the predicted data and can be used to run the 
    GRAC statistical functions.
* Example
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    test_class_column = 1;
$    features_columns = [1,2,52];
$    test_features_column = [2,5,8];
$    uploadTrainingData(“C:\path\to\file”);
$    uploadTestData(“C:\path\to\file”);
$    svc();
$    execute();
$    predict();
$    savePredResult(“fileName”);
$    uploadData(“fileName.csv”);
$    mode(0);
$    mean(0);
$    stdev(0);
$ }
```

### Saving results:
#### saveCVResult():
* Parameters:
    saveCVResult(path) -The path for the file to save the results
* saveCVResult - Save the predictions of each fold computed by the executeCV in individual files with the format: truth value, predicted value. Also saves a scoring.csv file with the global results including:  precision,  accuracy, recall f-score and confusion matrix of each fold. 
* Example:
```sh
$ grac{
$    hasheader = true;
$    uploadTrainingData(“C:\path\to\file”);
$    uploadTestData(“C:\path\to\file”);
$    svc();
$    executeCV();
$    saveCVResult()
$ }
```
#### saveStatResult():
* Parameters:
    saveStatResult( path ) - The path for the file to save the results
* saveStatResult - save the result of all the statistical method used by the user. 
* Example:
```sh
$ grac{
$    x = [1,2,3,4];
$    stdev(x);
$    max(x);
$    mode(x);
$    saveStatResult()
$  }
```
#### savePredResult():
* Parameters:
    savePredResult( path ) - The path for the file to save the results
* savePredResult - save the result for the prediction method in a CSV file format. The output of the file is:
        truth value, predicted value
* Example
```sh
$ grac{
$    hasheader = true;
$    class_column = 0;
$    test_class_column = 1;
$    features_columns = [1,2,52];
$    test_features_column = [2,5,8];
$    uploadTrainingData(“C:\path\to\file”);
$    uploadTestData(“C:\path\to\file”);
$    svc();
$    execute();
$    predict();
$    savePredResult()
$ }
```
---
# Language Development
### Translator Architecture
For details of the architecture of the translator see the Grammar and Lexemes, Tokens and Syntax section.
### Interfaces between the modules
In order to execute some modules, others must be executed first. The modules that depend on others are:

| Dependant Module      | Methods that need to be run first                                              |
|-----------------------|:--------------------------------------------------------------------------------|
| execute()             | uploadTrainingData(), <br> svc() \| dtc() \| gnbc()                                   |
| executeCV()           | uploadTrainingData(), <br> svc() \| dtc() \| gnbc()                                    |
| getCVErrorRate()      | uploadTrainingData(), <br> svc() \| dtc() \| gnbc(), <br> executeCV()                        |
| printBestClassifier() | uploadTrainingData()                                                           |
| predict()             | uploadTrainingData(), <br> uploadTestData, <br> svc() \| dtc() \| gnbc(),execute()           |
| saveCVResult()        | uploadTrainingData(), <br> uploadTestData, <br> svc() \| dtc() \| gnbc(),executeCV()         |
| savePredResult()      | uploadTrainingData(), <br> uploadTestData, <br> svc() \| dtc() \| gnbc(), <br> execute(), <br> predict() |

### Softwares used for the translator
Ply
### Test methodology & program used to test
Using python 2.7 we  tested all the variables used and each method exhaustively and compared the results.   All the code used for testing can be found in the example folder in the github account for the project 
----
# Conclusion

Machine Learning, data mining, and big data are important fields in programming, as they are used for the advance in Medicine, Cyber Security, Financial Analysis, etc. It would be convenient for a language that could do all  of this without needing support from other languages and complicated file formats. This is why GRAC was created. With GRAC, the user can analyse data in a CSV file using machine learning or statistical methods. <br>
GRAC is extremely convenient, as there is no need for the understanding of many languages. The user only needs to have a basic knowledge of Python, which is one of the most known languages, and be able to follow the basic guidelines of GRAC to fulfill the wanted analysis. 

----
#Developers
  - [Glorimar Castro Noriega] : glorimar.castro@upr.edu
  - [Rafael Feliciano Isales] : rafael.feliciano4@upr.edu
  - [Anthony S Slaughter Amaro] : anthony.slaughter@upr.edu
  - [Carlos E Rosario Gonzalez] : carlos.rosario10@upr.edu

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [examples]: <https://github.com/GlorimarCastro/grac/tree/master/examples>
   [special-purpose programming language]: <https://en.wikipedia.org/wiki/Domain-specific_language>
   [supervised machine learning]: <https://en.wikipedia.org/wiki/Supervised_learning>
   [statistics]: <https://en.wikipedia.org/wiki/Statistics>
   [Decision Tree]: <http://mines.humanoriented.com/classes/2010/fall/csci568/portfolio_exports/lguo/decisionTree.html>
   [Support Vector Machine]: <http://www.support-vector-machines.org/>
   [Gaussian Naive Bayes]: <https://en.wikipedia.org/wiki/Naive_Bayes_classifier>
   [cross-validation]: <https://www.cs.cmu.edu/~schneide/tut5/node42.html>
   [Carlos E Rosario Gonzalez]: <https://github.com/zrike>
   [Glorimar Castro Noriega]: <https://github.com/GlorimarCastro>
   [Anthony S Slaughter Amaro]: <https://github.com/slaughter30>
   [https://www.youtube.com/watch?v=SGs17I4_cI8&feature=youtu.be]: <- [https://www.youtube.com/watch?v=SGs17I4_cI8&feature=youtu.be]>
   [Rafael Feliciano Isales]: <https://github.com/rafaelfeliciano4>
