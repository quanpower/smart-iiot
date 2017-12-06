# -*- coding:utf-8 -*-

import datetime
from app.models import GrainTemp

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.sqlite')
# 创建DBSession类型:
Session = sessionmaker(bind=engine)
db_session = Session()

nodeAddrs = ['10', '20', '28', '24', '17', '22', '29', '15', '21', '16', '18', '19', '26', '27', '25', '30']
all_lost = 0
all_records = 0
for nodeAddr in nodeAddrs:
	print('--------now node is:***{}***---------'.format(nodeAddr))
	startTime = datetime.datetime.strptime('2017-12-05 14:30:00', "%Y-%m-%d %H:%M:%S")
	endTime = datetime.datetime.strptime('2017-12-06 14:30:00', "%Y-%m-%d %H:%M:%S")

	temp_records = db_session.query(GrainTemp.lora_node_id, GrainTemp.datetime).filter(
				and_(GrainTemp.lora_node_id == int(nodeAddr),
					GrainTemp.datetime.between(startTime, endTime))).order_by(
				GrainTemp.datetime.asc()).all()

	print(temp_records)

	lost = 0
	for i in range(1, len(temp_records)):
		temp_record = temp_records[i]
		if (temp_record[1] - temp_records[i-1][1]).seconds > 300:
			lost += 1
			print((temp_record[1] - temp_records[i-1][1]).seconds)
		else:
			print((temp_record[1] - temp_records[i-1][1]))

	print('lost number is:', lost)
	print('temp_records number is:', len(temp_records))
	print('lost ratio is:', format(float(lost)/float(len(temp_records)), '.2f'))

	print('--------------------NODE-END--------------------')
	all_records += len(temp_records)
	all_lost += lost

print('--------------------ALL-RECORDS & ALL-LOST--------------------')
print('----all_records----')
print(all_records)
print('----all_lost----')
print(all_lost)
print('----lost ratio----')
print('lost ratio is:', format(float(all_lost) / float(all_records), '.2f'))




