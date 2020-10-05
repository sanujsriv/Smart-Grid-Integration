import os
os.environ["JAVA_HOME"] = "/dbr1/hctl/spark_essentials/jdk1.8.0_251/"
os.environ["SPARK_HOME"] = "/usr/local/spark-2.4.0-bin-hadoop2.7/"

import findspark
findspark.init()

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").config("spark.jars", "/dbr1/hctl/spark_essentials/mysql-connector-java-5.1.49.jar,/dbr1/hctl/spark_essentials/spark-iforest-2.4.0.jar").getOrCreate()

from pyspark.sql import SQLContext
sqlContext = SQLContext(spark.sparkContext)

from pyspark.sql.functions import to_timestamp,to_date
from datetime import datetime
import time

from pyspark_iforest.ml.iforest import *
from decimal import Decimal
from pyspark.ml.linalg import Vectors
import tempfile
import pandas as pd

hostname = "dbclass.cs.nmsu.edu" 
dbname = "nmsu_power"
jdbcPort = 3306
username = "sakumar"
password = "2u$2C!2HwisL"
jdbc_url = "jdbc:mysql://{0}:{1}/{2}?user={3}&password={4}".format(hostname,jdbcPort, dbname,username,password)

query = "(select * from power) whyalias"
df_origin = sqlContext.read.format('jdbc').options(driver='com.mysql.jdbc.Driver',url=jdbc_url, dbtable=query ).load()
#df_origin.show()
print("db connected successfully")

date=df_origin.select(to_date(df_origin['Date'], 'dd/MM/yyyy').alias('date')).collect()
time=df_origin.select(to_timestamp(df_origin['Time'], 'yyyy-MM-dd HH:mm:ss').alias('time')).collect()


date_list=[]
time_list=[]
date_time_list=[]

for da in date:
  row_list=[]
  for d in da:
    row_list.append(d)
  date_list.append(row_list)

for ti in time:
  row_list=[]
  for t in ti:
    row_list.append(t.time())
  time_list.append(row_list)

for i in range(len(time_list)):
  date_time_list.append(datetime.combine(date_list[i][0],time_list[i][0]))

last=100
date_time_list = date_time_list[-last:]


columns_to_drop=["Date","Time"]
df1=df_origin.drop(*columns_to_drop)

a=[column for column in df1.columns]
g=df1.select(a).collect()
record_count=df1.count()

print("select last 100 records successfully")


size=0
a=[]
for row in g:
    row_data = []
    # size=size+1;
    # if size == 50:
    #   break
    # else:
    for data in row:
        if type(data) == Decimal:
            row_data.append(float(data))
        elif type(data) == float:
            row_data.append(float(data))
    a.append(row_data)

# a=a[len(df1.columns):]
a=a[-last:]
a=[[i / sum(j) for i in j] for j in a]
#print(a)



# spark = SparkSession.builder.master("local[*]").getOrCreate()

spark = SparkSession.builder.master("local[*]") \
        .appName("IForestExample") \
        .getOrCreate()


data = [(Vectors.dense(i),) for i in a]

print("covert data successfully")

# NOTE: features need to be dense vectors for the model input

df = spark.createDataFrame(data, ["features"])

# Init an IForest Object
iforest = IForest(contamination=0.25,maxDepth=4)
print("init iforest")
# Fit on a given data frame
model = iforest.fit(df)
print("fit iforest")
# Check if the model has summary or not, the newly trained model has the summary info
model.hasSummary

# Show model summary
summary = model.summary

# Show the number of anomalies
summary.numAnomalies

# Predict for a new data frame based on the fitted model
transformed = model.transform(df)

# Collect spark data frame into local df
rows = transformed.collect()

temp_path = tempfile.mkdtemp()
iforest_path = temp_path + "/iforest"

# Save the iforest estimator into the path
iforest.save(iforest_path)

# Load iforest estimator from a path
loaded_iforest = IForest.load(iforest_path)

model_path = temp_path + "/iforest_model"

# Save the fitted model into the model path
model.save(model_path)

# Load a fitted model from a model path
loaded_model = IForestModel.load(model_path)

# The loaded model has no summary info
loaded_model.hasSummary

# Use the loaded model to predict a new data frame
new_df=loaded_model.transform(df)


columns_to_drop=["Date","Time"]
df1=df_origin.drop(*columns_to_drop)





predictions=new_df.select('prediction').collect()
anomalyScores = new_df.select('anomalyScore').collect()

anomalyScores_list=[]
for an in anomalyScores:
  row_list=[]
  for a in an:
    row_list.append(a)
  anomalyScores_list.append(row_list)
anomalyScores_list = [item for sublist in anomalyScores_list for item in sublist]


plist=[]
for an in predictions:
  row_list=[]
  for a in an:
    row_list.append(a)
  plist.append(row_list)
plist = [item for sublist in plist for item in sublist]

print(plist)

print(date_time_list)
print(anomalyScores_list)

anomaly_date=[]
for i,j in zip(plist,date_time_list):
  if(i==1.0):
    anomaly_date.append(j)

print(anomaly_date)

pred_1=new_df.filter(new_df['prediction']==1.0).select(new_df['anomalyScore']).collect()

pred_list=[]
for an in pred_1:
  row_list=[]
  for a in an:
    row_list.append(a)
  pred_list.append(row_list)
pred_list = [item for sublist in pred_list for item in sublist]

print(pred_list)
print(anomalyScores_list)

print("Percentage of anomalies in data: {:.2f}".format( (len(pred_list) / len(plist) )*100))

pandas_df=new_df.toPandas()

pandas_df.hist(column='anomalyScore')
pandas_df.hist(column='prediction')


