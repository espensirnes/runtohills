#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymssql
from datetime import datetime
import time
import numpy as np 


def get_connection():
	for i in range(20):
		conn,crsr='No connection',None
		try:
			conn = pymssql.connect(host='titlon.uit.no', 
						   user="experiment_subject", 
				password='kzl32##@@3222hh', 
				database='experiment')  
			crsr=conn.cursor()
			break
		except:
			time.sleep(1)
	return conn,crsr
			

def save_results(record,conn,crsr):
	
	record['ExperimentEnd']=datetime.now().strftime("%H:%M:%S")
	record['Date']=datetime.now().strftime("%Y-%m-%d")
	#you may substitute pymysql for pymssql if you prefer the MS SQL client


	tbl=[]
	for i in record:
		if not i in ['Date','SubjectID','ExperimentID']:
			try:
				tbl.append((record['Date'],record['ExperimentID'],record['SubjectID'],i,float(record[i]),None))
			except:
				tbl.append((record['Date'],record['ExperimentID'],record['SubjectID'],i,None,str(record[i])))
	InsertTableIntoDB(conn, crsr, tbl)
			

def InsertTableIntoDB(conn,crsr, datatable):
	SQLExpr="""INSERT INTO [experiment].[dbo].[record]
	([Date],
	[ExperimentID],
	[SubjectID],
	[description],
	[value_float],
	[value_str]) VALUES (%s,%s,%s,%s,%s,%s)
	"""

	try:
		crsr.executemany(SQLExpr,datatable)	
		conn.commit()
	except Exception as e:
		for i in datatable:
			crsr.execute(SQLExpr,tuple(i))
		conn.commit()
		
	
def get_experiment_info(crsr,record):
	SQLExpr="""
SELECT TOP 1000 [ID]
      ,[sunk_cost]
      ,[minuttes]
      ,[n_lives]
  FROM [experiment].[dbo].[experiment_info]"""
	crsr.execute(SQLExpr)
	a=crsr.fetchall()[0]
	ID,sunc_cost, minuttes,n_lives=a
	sunc_cost=tuple(np.array(sunc_cost.split(';'),dtype=int))
	record['ExperimentID']=ID
	record['sunc_cost']=sunc_cost
	record['minuttes']=minuttes
	record['n_lives']=n_lives
	
	return a[0][0]
	
	
	
sql_newdb="""

/*Create user:*/
EXEC sp_configure 'CONTAINED DATABASE AUTHENTICATION', 1;
RECONFIGURE;

ALTER DATABASE [experiment] SET CONTAINMENT = PARTIAL;

CREATE USER experiment_subject WITH PASSWORD = 'kzl32##@@3222hh';
GRANT INSERT ON OBJECT::[experiment].[dbo].[record] TO experiment_subject;

CREATE USER experimenter WITH PASSWORD = 'kzl32##@@3222hh';
GRANT SELECT TO experimenter;

/*(last must be run from master db in query manager)*/

/*create table:*/
DROP TABLE [experiment].[dbo].[record];
CREATE TABLE [experiment].[dbo].[record](
	[ID] bigint IDENTITY(1,1) NOT NULL,
	[Date] date NULL,
	[ExperimentID] varchar(50) NULL,
	[SubjectID] varchar(50) NULL,
	[description] varchar(50) NULL,
	[value_float] float NULL,
	[value_str] varchar(100) NULL

);

CREATE NONCLUSTERED INDEX IX ON [experiment].[dbo].[record] ([ID],[Date],[ExperimentID],[SubjectID],[description])
ALTER TABLE [experiment].[dbo].[record] ADD CONSTRAINT PK PRIMARY KEY CLUSTERED (ID)
GRANT INSERT ON OBJECT::[experiment].[dbo].[record] TO experiment_subject;
"""

sql_experiment_info="""

DROP TABLE [experiment].[dbo].[experiment_info];
CREATE TABLE [experiment].[dbo].[experiment_info](
[ID] varchar(500) NULL,
[sunk_cost] varchar(50) NULL,
[minuttes] int NULL,
[n_lives] int NULL

);
INSERT INTO [experiment].[dbo].[experiment_info] ([ID],[sunk_cost],[minuttes],[n_lives]) VALUES ('E.2','2;12;24',20,3)
GRANT SELECT ON OBJECT::[experiment].[dbo].[experiment_info] TO experiment_subject;
"""