__author__ = 'CERG'

# Super extra simple example to identify some statistical functions in GRAC

import re

# simulating code to be run by the user of GRAC

text = []
text.append("grac(){               ")                   # line 0: indicating user wants to use GRAC language
text.append("	mean(x);    #gets mean value of x")     # line 1 to n-1: functions to be used
text.append("	avg(x);		#gets average value of x")  # ...
text.append("	min(x);		#gets min value of x")      # ...
text.append("   max(x);		#gets maximum value of x")
text.append("	mode(x);	#gets mode value of x")
text.append("	rndm(x);	#gets a random value of x")
text.append("	count(x);	#gets count of values in x")
text.append("	stdev(x);	#gets standard deviation of values in x")
text.append("	least(x);	#gets least repeated value in x")
text.append("	calcBestClassifier();	#gets best classifier")
text.append("	printBestClassifier();	#prints best classifer")
text.append("	printClassifiersComp();	#prints comparations of classifiers")
text.append("}")                                        # line n: indicating user closed GRAC indicator correctly


# Print what the user entered (testing append of lines)
print("\n")
for e in text:
    print e

# Check if first line contains GRAC languange indicator and opening '{'
a = re.search("(grac\(\){.*)", text[0])

# If the past condition is met, iterate through rest of lines (until n-1 line)
# and check which statistics function is called
if a:
    print("\nCan begin\n")
    for i in range(1,len(text)-1):

        b = re.search("(mean.*)", text[i])
        c = re.search("(avg.*)", text[i])
        d = re.search("(min.*)", text[i])
        e = re.search("(max.*)", text[i])
        f = re.search("(mode.*)", text[i])
        g = re.search("(rndm.*)", text[i])
        h = re.search("(count.*)", text[i])
        j = re.search("(least.*)", text[i])
        k = re.search("(stdev.*)", text[i])
        l = re.search("(calcBestClassifier().*)", text[i])
        m = re.search("(printBestClassifier().*)", text[i])
        n = re.search("(printClassifiersComp().*)", text[i])

        if b:
            print("The mean value will be calculated in line"+str(i)+".")
        if c:
            print("The average value will be calculated in line"+str(i)+".")
        if d:
            print("The minimum value will be calculated in line"+str(i)+".")
        if e:
            print("The maximum value will be calculated in line"+str(i)+".")
        if f:
            print("The mode will be calculated in line"+str(i)+".")
        if g:
            print("A random value will be chosen in line"+str(i)+".")
        if h:
            print("The count of values will be calculated in line"+str(i)+".")
        if j:
            print("The least repeated value will be given in line"+str(i)+".")
        if k:
            print("The standard deviation will be calculated in line"+str(i)+".")
        if l:
            print("The standard deviation will be calculated in line"+str(i)+".")
        if m:
            print("The standard deviation will be calculated in line"+str(i)+".")
        if n:
            print("The standard deviation will be calculated in line"+str(i)+".")


# After all functions are called, check if user closed the GRAC indicator correctly with '}'
if re.search("(\})",text[len(text)-1]):
    print("Ready to compile!")
else:
    print("Missing '}' in code.")
