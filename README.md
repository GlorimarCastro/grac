# Introduction

GRAC is a python based [special-purpose programming language] for [supervised machine learning] and [statistics]. It allows the user to upload CSV files and run classification methods, predictions and statistics on it. 

## Statistic Section
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
 
## Machine Learning Section
For now, the machine learning classifiers available are supervised classifiers:
  - [Decision Tree]
  - [Support Vector Machine]
  - [Gaussian Naive Bayes]
  
Also, GRAC allows you to calculate the best classifier for your data (based on accuracy), and to execute [cross-validation]

### Version
1.0


---
# Installation
## Dependecies
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

# Example Section
Examples of how tou use GRAC can be found in the [examples] folder


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [examples]: <https://github.com/GlorimarCastro/grac/tree/master/examples>
   [special-purpose programming language]: <https://en.wikipedia.org/wiki/Domain-specific_language>
   [supervised machine learning]: <https://en.wikipedia.org/wiki/Supervised_learning>
   [statistics]: <https://en.wikipedia.org/wiki/Statistics>
   [Decision Tree]: <http://mines.humanoriented.com/classes/2010/fall/csci568/portfolio_exports/lguo/decisionTree.html>
   [Support Vector Machine]: <http://www.support-vector-machines.org/>
   [Gaussian Naive Bayes]: <https://en.wikipedia.org/wiki/Naive_Bayes_classifier>
   [cross-validation]: <https://www.cs.cmu.edu/~schneide/tut5/node42.html>
