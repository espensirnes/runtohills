#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymssql
from datetime import datetime
import time

def save_results(record):
	
	record['ExperimentEnd']=datetime.now().strftime("%H:%M:%S")
	record['Date']=datetime.now().strftime("%Y-%m-%d")
	#you may substitute pymysql for pymssql if you prefer the MS SQL client
	for i in range(1000):
		try:
			conn = pymssql.connect(host='titlon.uit.no', 
						   user="experiment_subject", 
				password='kzl32##@@3222hh', 
				database='experiment')  
			crsr=conn.cursor()
			break
		except:
			time.sleep(1)
	record['ExperimentID']=get_expID(crsr)
	tbl=[]
	for i in record:
		if not i in ['Date','SubjectID','ExperimentID']:
			try:
				tbl.append((record['Date'],record['ExperimentID'],record['SubjectID'],i,float(record[i]),None))
			except:
				tbl.append((record['Date'],record['ExperimentID'],record['SubjectID'],i,None,record[i]))
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
		
	
def get_expID(crsr):
	SQLExpr="""SELECT * FROM [experiment].[dbo].[expID]"""
	crsr.execute(SQLExpr)
	a=crsr.fetchall()
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