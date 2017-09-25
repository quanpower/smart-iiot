# -*- coding:utf-8 -*-


from app import db
import datetime
from app.models import GrainTemp, LoraGateway, LoraNode, GrainBarn, GrainStorehouse #ConcGateway, ConcNode, ConcTemp
from sqlalchemy import and_
import logging  


# logging.basicConfig(level=logging.WARNING,  
#                     filename='./log.txt',  
#                     filemode='w',  
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 

nodeAddr = '4'
startTime = datetime.datetime.strptime('2017-09-24 21:21:00', "%Y-%m-%d %H:%M:%S")
endTime = datetime.datetime.strptime('2017-09-25 09:21:00', "%Y-%m-%d %H:%M:%S")

temp_records = db.session.query(GrainTemp.lora_node_id, GrainTemp.datetime).join(
            LoraNode, LoraNode.id == GrainTemp.lora_node_id).filter(
            and_(LoraNode.node_addr == nodeAddr,
                GrainTemp.datetime.between(startTime, endTime))).order_by(
            GrainTemp.datetime.asc()).all()

print(temp_records)

lost = 0
for i in range(1,len(temp_records)):
	temp_record = temp_records[i]
	if (temp_record[1] - temp_records[i-1][1]).seconds > 60:
		lost += 1
		print((temp_record[1] - temp_records[i-1][1]).seconds)
	else:
		print((temp_record[1] - temp_records[i-1][1]))

print('lost number is:', lost)
print('temp_records number is:', len(temp_records))
print('lost ratio is:', format(float(lost)/float(len(temp_records)),'.2f'))


