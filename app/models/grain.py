from app import db, login_manager


class GrainStorehouse(db.Model):
    __tablename__ = 'grain_storehouse'
    id = db.Column(db.Integer, primary_key=True)
    storehouse_no = db.Column(db.String(10), unique=True, nullable=False)
    storehouse_name = db.Column(db.String(50))

    def __repr__(self):
        return self.storehouse_no


class LoraGateway(db.Model):
    __tablename__ = 'lora_gateway'
    id = db.Column(db.Integer, primary_key=True)
    gateway_addr = db.Column(db.String(4), unique=True, nullable=False)
    grain_storehouse_id = db.Column(db.Integer, db.ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = db.relationship("GrainStorehouse")

    def __repr__(self):
        return self.gateway_addr


class GrainBarn(db.Model):
    __tablename__ = 'grain_barn'
    id = db.Column(db.Integer, primary_key=True)
    barn_no = db.Column(db.String(10), unique=True)
    barn_name = db.Column(db.String(50))
    grain_storehouse_id = db.Column(db.Integer, db.ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = db.relationship("GrainStorehouse")
    lora_gateway_id = db.Column(db.Integer, db.ForeignKey('lora_gateway.id'), nullable=False)
    lora_gateway = db.relationship("LoraGateway")
    high_limit = db.Column(db.Float)
    low_limit = db.Column(db.Float)

    def __repr__(self):
        return self.barn_name


class PowerIo(db.Model):
    __tablename__ = 'power_io'
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(8), unique=True)
    name = db.Column(db.String(50))
    grain_barn_id = db.Column(db.Integer, db.ForeignKey('grain_barn.id'), nullable=False)
    grain_barn = db.relationship("GrainBarn")

    def __repr__(self):
        return self.addr


class TianshuoRs485(db.Model):
    __tablename__ = 'tianshuo_rs485'
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(8), unique=True)
    name = db.Column(db.String(50))
    grain_barn_id = db.Column(db.Integer, db.ForeignKey('grain_barn.id'), nullable=False)
    grain_barn = db.relationship("GrainBarn")

    def __repr__(self):
        return self.addr


class LoraNode(db.Model):
    __tablename__ = 'lora_node'
    id = db.Column(db.Integer, primary_key=True)
    node_addr = db.Column(db.String(8), unique=True)
    node_name = db.Column(db.String(8))
    grain_storehouse_id = db.Column(db.Integer, db.ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = db.relationship("GrainStorehouse")
    lora_gateway_id = db.Column(db.Integer, db.ForeignKey('lora_gateway.id'), nullable=False)
    lora_gateway = db.relationship("LoraGateway")
    grain_barn_id = db.Column(db.Integer, db.ForeignKey('grain_barn.id'), nullable=False)
    grain_barn = db.relationship("GrainBarn")
    power_io_id = db.Column(db.Integer, db.ForeignKey('power_io.id'), nullable=False)
    power_io = db.relationship("PowerIo")
    current = db.Column(db.Float, default=0)
    current_limit = db.Column(db.Float)
    current_no = db.Column(db.SmallInteger)
    auto_manual = db.Column(db.String(8), default='auto')
    manual_start_time = db.Column(db.DateTime)
    manual_end_time = db.Column(db.DateTime)
    auto_start_time = db.Column(db.DateTime)
    auto_end_time = db.Column(db.DateTime)

    def __repr__(self):
        return self.node_addr


class GrainTemp(db.Model):
    __tablename__ = 'grain_temp'
    id = db.Column(db.Integer, primary_key=True)
    grain_storehouse_id = db.Column(db.Integer, db.ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = db.relationship("GrainStorehouse")
    lora_gateway_id = db.Column(db.Integer, db.ForeignKey('lora_gateway.id'), nullable=False)
    lora_gateway = db.relationship("LoraGateway")
    grain_barn_id = db.Column(db.Integer, db.ForeignKey('grain_barn.id'), nullable=False)
    grain_barn = db.relationship("GrainBarn")
    lora_node_id = db.Column(db.Integer, db.ForeignKey('lora_node.id'), nullable=False)
    lora_node = db.relationship("LoraNode")
    switch = db.Column(db.Boolean)
    temp1 = db.Column(db.Float)
    temp2 = db.Column(db.Float)
    temp3 = db.Column(db.Float)
    battery_vol = db.Column(db.SmallInteger)
    datetime = db.Column(db.DateTime)

    def __repr__(self):
        return str(self.temp1)


class RelayCurrentRs485Func(db.Model):
    __tablename__ = 'relay_current_rs485_func'
    id = db.Column(db.Integer, primary_key=True)
    function_name = db.Column(db.String(50), unique=True)
    function_code = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return str(self.function_name)


class PowerIoRs485Func(db.Model):
    __tablename__ = 'power_io_rs485_func'
    id = db.Column(db.Integer, primary_key=True)
    function_name = db.Column(db.String(50), unique=True)
    function_code = db.Column(db.SmallInteger)
    start_at_reg_high = db.Column(db.SmallInteger)
    start_at_reg_low = db.Column(db.SmallInteger)
    num_of_reg_high = db.Column(db.SmallInteger)
    num_of_reg_low = db.Column(db.SmallInteger)

    def __repr__(self):
        return str(self.function_name)


class TianshuoRs485Func(db.Model):
    __tablename__ = 'tianshuo_rs485_func'
    id = db.Column(db.Integer, primary_key=True)
    function_name = db.Column(db.String(50), unique=True)
    function_code = db.Column(db.SmallInteger)
    start_at_reg_high = db.Column(db.SmallInteger)
    start_at_reg_low = db.Column(db.SmallInteger)
    num_of_reg_high = db.Column(db.SmallInteger)
    num_of_reg_low = db.Column(db.SmallInteger)

    def __repr__(self):
        return str(self.function_name)


class NodeMqttTransFunc(db.Model):
    __tablename__ = 'node_mqtt_trans_func'
    id = db.Column(db.Integer, primary_key=True)
    gateway_addr = db.Column(db.String(3), default='001')
    node_addr = db.Column(db.String(13))
    trans_direct = db.Column(db.String(1), default='1')
    func_code = db.Column(db.String(7), default='0010001')
    wind_direct = db.Column(db.String(2), default='00')
    wind_speed = db.Column(db.String(2), default='11')
    model = db.Column(db.String(10), default='1000111001')  # sanling 569
    on_off = db.Column(db.String(2))
    work_mode = db.Column(db.String(3), default='001')
    temp = db.Column(db.String(5), default='10100')  # 20

    def __repr__(self):
        return str(self.node_addr)


class AlarmLevelSetting(db.Model):
    __tablename__ = 'alarm_level_setting'
    id = db.Column(db.Integer, primary_key=True)
    warning = db.Column(db.SmallInteger, default=35)
    error = db.Column(db.SmallInteger, default=45)

    def __repr__(self):
        return str(self.warning)


class AlarmStatus(db.Model):
    __tablename__ = 'alarm_status'
    id = db.Column(db.Integer, primary_key=True)
    lora_node_id = db.Column(db.Integer, db.ForeignKey('lora_node.id'), nullable=False)
    lora_node = db.relationship("LoraNode")
    alarm_status = db.Column(db.Boolean)
    datetime = db.Column(db.DateTime)
    send_alarm_datetime = db.Column(db.DateTime)

    def __repr__(self):
        return str(self.alarm_status)


class AlarmTypes(db.Model):
    __tablename__ = 'alarm_type'
    id = db.Column(db.Integer, primary_key=True)
    alarm_type = db.Column(db.SmallInteger, default=35)

    def __repr__(self):
        return str(self.alarm_type)


class AlarmRecords(db.Model):
    __tablename__ = 'alarm_records'
    id = db.Column(db.Integer, primary_key=True)
    lora_node_id = db.Column(db.Integer, db.ForeignKey('lora_node.id'), nullable=False)
    lora_node = db.relationship("LoraNode")
    alarm_type_id = db.Column(db.Integer, db.ForeignKey('alarm_type.id'), nullable=False)
    alarm_type = db.relationship("AlarmTypes")
    datetime = db.Column(db.DateTime)

    def __repr__(self):
        return str(self.alarm_type)