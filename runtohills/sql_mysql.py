#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
from datetime import datetime
import time
import numpy as np 


def get_connection():
	for i in range(20):
		conn,crsr='No connection',None
		try:
			conn = pymysql.connect(host='titlon.uit.no', 
						   user="exp_subject", 
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

	tbl=[]
	for i in record:
		if not i in ['Date','SubjectID','ExperimentID']:
			if i=='data':
				for is_trial,game_number,key,value,cause in record[i]:
					append_to_table(tbl, record, key, value,cause,is_trial,game_number)
			else:
				append_to_table(tbl, record, i, record[i])
				
	InsertTableIntoDB(conn, crsr, tbl)
			
def append_to_table(tbl,record,description,value,cause=None,is_trial=None,game_number=None):
	try:
		tbl.append((record['Date'],record['ExperimentID'],record['SubjectID'],description,is_trial,game_number,cause,float(value),str(value)))
	except:
		tbl.append((record['Date'],record['ExperimentID'],record['SubjectID'],description,is_trial,game_number,cause,None,str(value)))	

def InsertTableIntoDB(conn,crsr, datatable):
	SQLExpr="""INSERT INTO `experiment`.`record`
	(`Date`,
	`ExperimentID`,
	`SubjectID`,
	`description`,
	`IsTrial`,
	`game_number`,
	`cause`,
	`value_float`,
	`value_str`) VALUES (%s,%s,%s,%s,%s,%s)
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
SELECT `ID`,`sunk_cost`,`minuttes`,`n_lives`,`NOK`
  FROM  `experiment`.`experiment_info`"""
	crsr.execute(SQLExpr)
	a=crsr.fetchall()[0]
	ID,sunc_cost, minuttes,n_lives,NOK=a
	sunc_cost=tuple(np.array(sunc_cost.split(';'),dtype=int))
	record['ExperimentID']=ID
	record['sunc_cost']=sunc_cost
	record['minuttes']=minuttes
	record['n_lives']=n_lives
	record['NOK']=NOK
	
	
	
sql_newdb="""
/*create table:*/
CREATE TABLE IF NOT EXISTS `experiment`.`record` (
	    `ID` bigint(20) NOT NULL AUTO_INCREMENT,
		`Date` date NULL,
		`ExperimentID` varchar(50) NULL,
		`SubjectID` varchar(50) NULL,
		`description` varchar(50) NULL,
		`value_float` float NULL,
		`value_str` varchar(100) NULL,
	    PRIMARY KEY (`ID`),
	    KEY `Index` (`Date`,`ExperimentID`,`SubjectID`,`description`) USING BTREE
) ;




CREATE USER 'exp_subject' IDENTIFIED BY 'kzl32##@@3222hh';
GRANT INSERT ON `experiment`.`record` TO 'exp_subject';
GRANT SELECT ON `exp_subject`.* TO 'exp_subject';

CREATE USER 'experimenter' IDENTIFIED BY 'kzl32##@@3222hh';
GRANT SELECT ON `experiment`.* TO 'experimenter';


"""

create_sql_experiment_info="""


CREATE TABLE IF NOT EXISTS `experiment`.`experiment_info`(
`ID` varchar(500) NULL,
`sunk_cost` varchar(50) NULL,
`minuttes` int NULL,
`n_lives` int NULL,
`NOK`  int NULL
);
INSERT INTO `experiment`.`experiment_info` (`ID`,`sunk_cost`,`minuttes`,`n_lives`,`NOK`) VALUES ('E.2','1;1;1',1,1,3);
GRANT SELECT ON `experiment`.* TO 'exp_subject';


"""


update_experiment_info="""


SET SQL_SAFE_UPDATES = 0;
TRUNCATE TABLE `experiment`.`experiment_info`;
INSERT INTO `experiment`.`experiment_info` (`ID`,`sunk_cost`,`minuttes`,`n_lives`,`NOK`) VALUES ('E.2','1;1;1',1,1,3);


"""
