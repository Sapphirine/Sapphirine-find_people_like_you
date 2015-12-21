from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.linalg import SparseVector
from pyspark import SparkContext
from operator import add
import time
import numpy
from pyspark.mllib.linalg import Vectors
import pyspark.mllib.clustering as cl
import os
sc = SparkContext("local", "Myapp")

#####Read input files
	#Get the all the file names
filenames = next(os.walk("/Users/panpan/Desktop/linkedin/followings/group8"))[2]
	#save the all files to variable <files>
files=list()
for filename in filenames:
	f=open("/Users/panpan/Desktop/linkedin/followings/group8/%s" %filename,"r")
	files.append(f.readline())

	#initialize mutual_list
mutual_list=numpy.zeros((len(filenames),len(filenames)))

	#pick two users each time, and calculate their common freinds
for i in range(0,len(files)):
	if i+1>=len(files):
		continue
	for j in range(i,len(files)):		
		file_1 =files[i].split(",")
		file_2 =files[j].split(",")
		file1 =sc.parallelize(file_1)
		file2 =sc.parallelize(file_2)
			#common friends of the two users
		file_12=file1.intersection(file2)
		mutual=len(file_12.collect())
			#define a way to cauculate how much percent they are similar to each other
		mutual_proportion=1.0/2*mutual*(1.0/len(file_1)+1.0/len(file_2))
		mutual_list[i][j]=mutual_list[j][i]=mutual_proportion

###Cluster the models
model = cl.KMeans.train(sc.parallelize(mutual_list), 4, maxIterations=10, runs=30, initializationMode="random",
seed=50, initializationSteps=5, epsilon=1e-4)
for i in range(0,len(mutual_list)):
	print model.predict(mutual_list[i])

	#further optimization on parameter needed


