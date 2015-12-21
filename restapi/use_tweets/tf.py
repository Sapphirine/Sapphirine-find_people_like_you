from pyspark.mllib.feature import HashingTF, IDF
from pyspark import SparkConf, SparkContext
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from math import sqrt


conf = SparkConf().setAppName("tfidf").setMaster("local")
sc = SparkContext(conf = conf)

rdd = sc.wholeTextFiles("DIR").map(lambda(name,text): text.split())
tf = HashingTF()
tfVectors = tf.transform(rdd).cache()

idf = IDF()
idfModel = idf.fit(tfVectors)
tfIdfvVectors = idfModel.transform(tfVectors)

print tfIdfvVectors
model = KMeans.train(tfIdfvVectors, 3, maxIterations = 10, runs = 10, initializationMode = "random")
model.save(sc, "MyModel4")
sameModel = KMeansModel.load(sc, "MyModel4")
clusters = model.predict(tfIdfvVectors)
dataWithClusters = tfIdfvVectors.zip(clusters)
dataWithClusters.saveAsTextFile("DIR2")





