import mysql.connector
import csv


mydb = mysql.connector.connect(
  host="dbclass.cs.nmsu.edu",
  user="sakumar",
  passwd="dbnmsu123",
  database='nmsu_power'
)


            ##################
            # Check Connection
            ##################
#
print("hello")
print(mydb)


mycursor = mydb.cursor()

                ###########
                # Delete 
                ###########

#mycursor.execute('delete from power')
#mydb.commit()


            
            ####################################
            # Configurational Settings for :-
            # Load Data Query
            # Multiple inserts
            # !! Not Working with db4free.net
            ####################################
            
            
            

#max_allowed_packet ='SET GLOBAL max_allowed_packet=1024*1024*1024'
#mycursor.execute(max_allowed_packet)

                        
                        ##############
                        # Create Table
#                        ##############
#
#mycursor.execute(
#   """CREATE TABLE `power` 
# (
#   `Date` varchar(50) NOT NULL,
#   `Time` time NOT NULL,
#   `global_active_power` decimal(10,4) DEFAULT NULL,
#   `global_reactive_power` decimal(10,4) DEFAULT NULL,
#   `voltage` decimal(10,3) DEFAULT NULL,
#   `global_intensity` decimal(10,3) DEFAULT NULL,
#   `sub_metering_1` float(10,3) DEFAULT NULL,
#   `sub_metering_2` float(10,3) DEFAULT NULL,
#   `sub_metering_3` decimal(10,3) DEFAULT NULL
# )""")
                
                        
                        

                    ################################
                    # Description of Table : Schema
                    ################################    
                    
                    
                    
                        
#mycursor.execute("DESC power")
#for x in mycursor:
#   print(x)
                    
                    
   
                    ################################
                    # Select and Show all tuples
                    ################################ 
                                            
                    
                    
                    
#mycursor.execute("SELECT * FROM power")
#myresult = mycursor.fetchall()
#for x in myresult:
#   print(x)



   
with open('household_power.txt', 'r') as f_100:
    reader = csv.reader(f_100, delimiter=',',skipinitialspace=True)
    your_list_100= list(reader)



############## No. of records ################################
#mycursor.execute("SELECT * FROM power")
#myresult = mycursor.fetchall()
#print(len(myresult))
##############################################



            # Single Insertion

for i in range(len(your_list_100)):

        sql="INSERT INTO power VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # we don't need the first tuple as it those are column headers (Date,Time.....Sub_metering_3)
        val = your_list_100[i+1]
        mycursor.execute(sql, val)
        mydb.commit()


            # Multi-Value Insertion 

#sql_many_insert="INSERT INTO power VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#val_many=your_list_100[1:]
#mycursor.executemany(sql_many_insert, val_many)
#mydb.commit()


            # Load Data (Bulk Loading)
        
#sql_load_data="LOAD DATAW INFILE 'household_power.txt' INTO TABLE power FIELDS TERMINATED BY ',' ENCLOSED BY '' LINES TERMINATED BY '\n' IGNORE 1 ROWS"
#mycursor.execute(sql_load_data)
#mydb.commit()