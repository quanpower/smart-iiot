from app import app
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.models import GrainTemp
from sqlalchemy import and_
import json

api = Api(app)


class LoraTemp(Resource):
    def get(self, gateway_addr, node_addr):
        temps = db.session.query(GrainTemp.temp1,GrainTemp.temp2,GrainTemp.temp3).filter(and_(GrainTemp.gateway_addr == gateway_addr, GrainTemp.node_addr == node_addr)).order_by(GrainTemp.date.desc()).first()
        print(temps)
        temp_dict = {}
        # temp_dict["numbers"] = []
        temp_dic = {"numbers":[{"icon":"team","color":"#64ea91","title":"Temp1","number":temps[0]},{"icon":"team","color":"#8fc9fb","title":"Temp2","number":temps[1]},{"icon":"team","color":"#d897eb","title":"Temp3","number":temps[2]},{"icon":"message","color":"#f69899","title":"Battery_Vol","number":2}]}
        return temp_dic

    def delete(self, todo_id):
		pass

    def put(self, todo_id):
		pass

class LoraTemps(Resource):
    def get(self, gateway_addr, node_addr):
        temps = db.session.query(GrainTemp.temp1,GrainTemp.temp2,GrainTemp.temp3).filter(and_(GrainTemp.gateway_addr == gateway_addr, GrainTemp.node_addr == node_addr)).order_by(GrainTemp.date.desc()).all()
        print(temps[:10])
        # for i in temps[:10]:
        # todo json.dump()
        return list(temps[:10])

    def delete(self, todo_id):
		pass

    def put(self, todo_id):
		pass

class LoRaBattery(Resource):
    def get(self, gateway_addr, node_addr):
    	battery_vol = db.session.query(GrainTemp.battery_vol).filter(and_(GrainTemp.gateway_addr == gateway_addr, GrainTemp.node_addr == node_addr)).order_by(GrainTemp.date.desc()).first()
    	battery_dict = {}
    	battery_dict["vol"] = battery_vol[0]
        return json.dumps(battery_dict)

    def post(self):
    	pass

class Dashboard(Resource):
    def get(self):
    	temps = db.session.query(GrainTemp.temp1,GrainTemp.temp2,GrainTemp.temp3).filter(and_(GrainTemp.gateway_addr == 1, GrainTemp.node_addr == 1)).order_by(GrainTemp.date.desc()).first()
    	
    	temp_records = db.session.query(GrainTemp.temp1,GrainTemp.temp2,GrainTemp.temp3,GrainTemp.date).filter(and_(GrainTemp.gateway_addr == 1, GrainTemp.node_addr == 1)).order_by(GrainTemp.date.desc()).limit(10).all()
    	print('------------temp_record--------------')
    	print(temp_records)
    	temp_log = []
    	for i in xrange(len(temp_records)):
    		temp_log.append({"time":i,"Temp1":temp_records[i][0],"Temp2":temp_records[i][1],"Temp3":temp_records[i][2]})

        print('--------------templog--------------------')

        print(str(temp_log))
    	battery_vol = db.session.query(GrainTemp.battery_vol).filter(and_(GrainTemp.gateway_addr == 1, GrainTemp.node_addr == 1)).order_by(GrainTemp.date.desc()).first()
    	print(battery_vol)
    	dashboard_dict = {"numbers":[{"icon":"team","color":"#64ea91","title":"Temp1","number":temps[0]},{"icon":"team","color":"#8fc9fb","title":"Temp2","number":temps[1]},{"icon":"team","color":"#d897eb","title":"Temp3","number":temps[2]},{"icon":"message","color":"#f69899","title":"Battery_Vol","number":battery_vol}],
    	"temps":temp_log,"cpu":{"usage":425,"space":825,"cpu":41,"data":[{"cpu":23},{"cpu":66},{"cpu":62},{"cpu":46},{"cpu":67},{"cpu":72},{"cpu":22},{"cpu":51},{"cpu":51},{"cpu":57},{"cpu":76},{"cpu":71},{"cpu":28},{"cpu":53},{"cpu":59},{"cpu":64},{"cpu":37},{"cpu":25},{"cpu":47},{"cpu":46}]},"browser":[{"name":"Google Chrome","percent":43.3,"status":1},{"name":"Mozilla Firefox","percent":33.4,"status":2},{"name":"Apple Safari","percent":34.6,"status":3},{"name":"Internet Explorer","percent":12.3,"status":4},{"name":"Opera Mini","percent":3.3,"status":1},{"name":"Chromium","percent":2.53,"status":1}],"user":{"name":"quanpower","email":"quanpower@gmail.com","sales":3241,"sold":3556,"avatar":"http://tva4.sinaimg.cn/crop.0.0.996.996.180/6ee6a3a3jw8f0ks5pk7btj20ro0rodi0.jpg"},"completed":[{"name":2008,"Task complete":943,"Cards Complete":487},{"name":2009,"Task complete":693,"Cards Complete":822},{"name":2010,"Task complete":349,"Cards Complete":499},{"name":2011,"Task complete":616,"Cards Complete":618},{"name":2012,"Task complete":335,"Cards Complete":597},{"name":2013,"Task complete":492,"Cards Complete":326},{"name":2014,"Task complete":515,"Cards Complete":792},{"name":2015,"Task complete":334,"Cards Complete":368},{"name":2016,"Task complete":746,"Cards Complete":401},{"name":2017,"Task complete":994,"Cards Complete":523},{"name":2018,"Task complete":991,"Cards Complete":934},{"name":2019,"Task complete":586,"Cards Complete":979}],"comments":[{"name":"Thomas","status":3,"content":"Quskvd uedfwsrro vrgguyxks oiqktfgsgu kevic zqrsyurhv gshldjkos yoqgekdmsv hmbxxjsgnf spz iubifjt pxsppsjd ufrcmtdle.","avatar":"http://dummyimage.com/48x48/f279f0/757575.png&text=T","date":"2016-01-01 10:58:37"},{"name":"Perez","status":2,"content":"Vintvvhae qrx kjrfv akqu xdnfosydq fuhv bspnprg gmhpecmhdl ucaemvmi gcxkh pbovvmtkj jxynubt bvvbpasv.","avatar":"http://dummyimage.com/48x48/79f2d0/757575.png&text=P","date":"2016-09-25 05:28:12"},{"name":"Taylor","status":2,"content":"Mejkuhk dvrfgnwcg uouicdnm vhqvyuou mpki dtdtft gcsxc uuynik ikmhxbe imobgaehg iud xmfb chsnow cqbefboe jtaqbijjgs iwoenuw ybyklnx pwxzd.","avatar":"http://dummyimage.com/48x48/f2ad79/757575.png&text=T","date":"2016-06-12 01:06:25"},{"name":"Martinez","status":2,"content":"Vhxkfgmb hzdklm mlfz dcowjrqe fgjlyifxk phlkjf iimhnfua kxhscyp bndqenqcx ktwmj tgfysxpn soxbqkkxj dvisfn dejts hktdp xqgbwt.","avatar":"http://dummyimage.com/48x48/8979f2/757575.png&text=M","date":"2016-11-15 03:46:00"},{"name":"Clark","status":2,"content":"Mlepximv rrbcldogy jcdcejf rmhdqvqi jrhltspy gije ruvql ktdnfd pfiy pkyvrcj gosgqmpwr hntb geqvlevnt hkydqbkzk inmyhl hkzmwowya bqjc.","avatar":"http://dummyimage.com/48x48/8bf279/757575.png&text=C","date":"2016-11-22 02:50:24"}],"recentSales":[{"id":1,"name":"Walker","status":3,"price":107.23,"date":"2016-05-23 06:46:10"},{"id":2,"name":"Anderson","status":2,"price":18.49,"date":"2015-03-18 10:37:17"},{"id":3,"name":"Walker","status":2,"price":103.32,"date":"2016-04-05 01:01:44"},{"id":4,"name":"Martinez","status":2,"price":173.6,"date":"2016-12-30 21:36:59"},{"id":5,"name":"Martinez","status":2,"price":120.5,"date":"2016-01-25 08:33:03"},{"id":6,"name":"Hernandez","status":1,"price":27.7,"date":"2015-07-29 01:39:13"},{"id":7,"name":"Walker","status":3,"price":53.3,"date":"2015-01-18 01:25:21"},{"id":8,"name":"Jones","status":2,"price":128.12,"date":"2016-06-16 04:23:31"},{"id":9,"name":"Anderson","status":2,"price":182.18,"date":"2016-06-18 22:21:24"},{"id":10,"name":"Lewis","status":3,"price":179.44,"date":"2016-12-27 04:49:37"},{"id":11,"name":"Wilson","status":1,"price":191.32,"date":"2016-10-22 23:50:36"},{"id":12,"name":"Lewis","status":1,"price":170.95,"date":"2016-02-14 09:29:02"},{"id":13,"name":"Allen","status":2,"price":74.56,"date":"2016-09-11 15:44:11"},{"id":14,"name":"Anderson","status":4,"price":116.27,"date":"2016-12-31 10:48:03"},{"id":15,"name":"Wilson","status":4,"price":190.9,"date":"2015-01-02 04:23:47"},{"id":16,"name":"Harris","status":3,"price":105.21,"date":"2015-05-14 13:49:32"},{"id":17,"name":"Jackson","status":3,"price":68.16,"date":"2016-10-01 03:30:56"},{"id":18,"name":"Wilson","status":3,"price":55.9,"date":"2016-09-25 06:18:44"},{"id":19,"name":"Thomas","status":2,"price":108.5,"date":"2016-03-22 19:04:15"},{"id":20,"name":"Davis","status":1,"price":16.6,"date":"2015-04-01 11:45:15"},{"id":21,"name":"Robinson","status":3,"price":54.6,"date":"2016-05-01 18:37:14"},{"id":22,"name":"Miller","status":3,"price":160.57,"date":"2015-08-03 00:43:16"},{"id":23,"name":"Thompson","status":3,"price":24.7,"date":"2016-12-06 04:05:01"},{"id":24,"name":"Williams","status":3,"price":93.75,"date":"2015-09-29 08:09:36"},{"id":25,"name":"Lee","status":2,"price":79.35,"date":"2016-08-04 04:26:05"},{"id":26,"name":"Clark","status":3,"price":192.3,"date":"2015-03-13 11:39:27"},{"id":27,"name":"Moore","status":3,"price":47.4,"date":"2015-04-11 04:25:55"},{"id":28,"name":"Williams","status":4,"price":12.9,"date":"2016-03-15 11:33:47"},{"id":29,"name":"Lopez","status":3,"price":25.23,"date":"2015-01-04 20:48:32"},{"id":30,"name":"Wilson","status":4,"price":156.2,"date":"2015-01-30 05:15:36"},{"id":31,"name":"Garcia","status":3,"price":64.63,"date":"2016-12-10 16:19:08"},{"id":32,"name":"Garcia","status":2,"price":149.74,"date":"2015-06-25 15:40:21"},{"id":33,"name":"Clark","status":3,"price":70.53,"date":"2016-08-28 01:12:45"},{"id":34,"name":"Miller","status":4,"price":74.42,"date":"2015-02-24 05:44:41"},{"id":35,"name":"Lopez","status":4,"price":128.54,"date":"2015-08-18 10:49:24"},{"id":36,"name":"Lopez","status":4,"price":161.4,"date":"2016-04-05 14:01:52"}],"quote":{"name":"Joho Doe","title":"Graphic Designer","content":"I'm selfish, impatient and a little insecure. I make mistakes, I am out of control and at times hard to handle. But if you can't handle me at my worst, then you sure as hell don't deserve me at my best.","avatar":"http://img.hb.aicdn.com/bc442cf0cc6f7940dcc567e465048d1a8d634493198c4-sPx5BR_fw236"}}

        return dashboard_dict

    def post(self):
    	pass

##
## Actually setup the Api resource routing here
##
api.add_resource(LoRaBattery, '/api/v1/loranode_battery/<gateway_addr>/<node_addr>')
api.add_resource(LoraTemp, '/api/v1/loranode_temperature/<gateway_addr>/<node_addr>')
api.add_resource(LoraTemps, '/api/v1/loranode_temperatures/<gateway_addr>/<node_addr>')
api.add_resource(Dashboard, '/api/v1/dashboard')


if __name__ == '__main__':
    app.run(debug=True)

app.run(host='0.0.0.0', port=8888, debug=True)

