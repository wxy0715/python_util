import json
import sys
import time

import pymysql
import configparser
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# # 获取配置信息

cf = configparser.ConfigParser()
# 读
cf.read("/opt/lsblj/etc/system.conf")
# #获取所有的sections
# # sections = cf.sections()
# # print(sections)
# 获取某个section下的所有options

options = cf.options("database")
# print(options)
# #获取某个section下的所有items
# items = cf.items("database")
# print(items)
db_host = cf.get("database", "db_host")  # 返回str类型
db_port = cf.getint("database", "db_port")  # 返回int类型，类似有：getfloat(), getboolean()
db_user = cf.get("database", "db_user")
db_pwd = cf.get("database", "db_pwd")
db_name = cf.get("database", "db_name")

print(db_host)
print(db_port)
print(db_user)
print(db_pwd)
print(db_name)
class MysqlHelper:
    '''python操作mysql的增删改查的封装'''

    def __init__(self, host, user, password, database, port, charset='utf8'):
        '''
        初始化参数
        :param host:        主机
        :param user:        用户名
        :param password:    密码
        :param database:    数据库
        :param port:        端口号，默认是3306
        :param charset:     编码，默认是utf8
        '''
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

    def connect(self):
        '''
        获取连接对象和执行对象
        :return:
        '''
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    port=self.port,
                                    charset=self.charset)

        self.cur = self.conn.cursor()

    def fetchone(self, sql, params=None):
        '''
         根据sql和参数获取一行数据
       :param sql:          sql语句
       :param params:       sql语句对象的参数元组，默认值为None
       :return:             查询的一行数据
       '''
        dataOne = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataOne = self.cur.fetchone()
        except Exception as ex:
            print(ex)
        return dataOne

    def fetchall(self, sql, params=None):
        '''
         根据sql和参数获取一行数据
       :param sql:          sql语句
       :param params:       sql语句对象的参数列表，默认值为None
       :return:             查询的一行数据
       '''
        dataall = None
        try:
            count = self.cur.execute(sql, params)
            if count != 0:
                dataall = self.cur.fetchall()
        except Exception as ex:
            print(ex)
        return dataall

    def __item(self, sql, params=None):
        '''
        执行增删改
        :param sql:           sql语句
        :param params:        sql语句对象的参数列表，默认值为None
        :return:              受影响的行数
        '''
        count = 0
        try:
            count = self.cur.execute(sql, params)
            self.conn.commit()
        except Exception as ex:
            print(ex)
        return count

    def update(self, sql, params=None):
        '''
        执行修改
        :param sql:     sql语句
        :param params:  sql语句对象的参数列表，默认值为None
        :return:        受影响的行数
        '''
        return self.__item(sql, params)

    def insert(self, sql, params=None):
        '''
        执行新增
        :param sql:     sql语句
        :param params:  sql语句对象的参数列表，默认值为None
        :return:        受影响的行数
        '''
        return self.__item(sql, params)

    def delete(self, sql, params=None):
        '''
        执行删除
        :param sql:     sql语句
        :param params:  sql语句对象的参数列表，默认值为None
        :return:        受影响的行数
        '''
        return self.__item(sql, params)

    def close(self):
        '''
        关闭执行工具和连接对象
        '''
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()


# 阿里云发送短信类
class AliyunSms():
    def __init__(self, accessKeyId, accessSecret, signName):
        self.accessKeyId = accessKeyId
        self.accessSecret = accessSecret
        self.signName = signName
        self.log_file = open("log.txt", "a")

    def _generate_request(self, phone, content, templateCode):

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('GET')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        # 以上部分是公用的不变
        request.set_action_name('SendSms')
        # set_action_name 这个是选择你调用的接口的名称，如：SendSms，SendBatchSms等
        request.add_query_param('RegionId', "default")
        # 这个参数也是固定的

        request.add_query_param('PhoneNumbers', phone)  # 发给谁
        request.add_query_param('TemplateCode', templateCode)  # 模板编号
        request.add_query_param('SignName', self.signName)
        request.add_query_param('TemplateParam', f"{content}")  # 发送验证码内容
        return request

    def _generate_client(self):
        client = AcsClient(self.accessKeyId, self.accessSecret, 'default')
        return client

    def send_sms(self, phone_num, content, templateCode):
        """
        发送短信验证码,返回Code字段的值
        :param phone_num: 手机号
        :param code: 验证码内容
        :param templateCode: 验证码模板
        :return:
        """
        client = self._generate_client()
        request = self._generate_request(phone_num, content, templateCode)
        try:
            response = client.do_action(request)  # bytes 类型
            response = response.decode()  # str类型
            response_dict = json.loads(response)  # {'Message': '触发天级流控Permits:1', 'RequestId': '5FA848EB-7C84-469D-8254-043835A05624', 'Code': 'isv.BUSINESS_LIMIT_CONTROL'}
            return response_dict

        except Exception as e:
            self.debug_print("异常信息：%s" % e)
            return None

    def debug_print(self, s):
        """ 打印日志
        """
        self.write_log(s)

    def write_log(self, log_str):
        """ 记录日志
            参数：
                log_str：日志
        """
        time_now = time.localtime()
        date_now = time.strftime('%Y-%m-%d', time_now)
        format_log_str = "%s ---> %s \n " % (date_now, log_str)
        print(format_log_str)
        self.log_file.write(format_log_str)


if __name__ == '__main__':
    conn = MysqlHelper(host=db_host, user=db_user, password=db_pwd, database=db_name,
                       port=db_port)
    # conn = MysqlHelper(host="127.0.0.1", user="root", password="123456", database="send_email",
    #                                    port=3306)
    conn.connect()

    # 获取短信配置的信息
    get_sms_sql = "select access_key_id,access_key_secret,sign_name,template_code from lsblj_config_sms limit 1;"
    config = conn.fetchall(get_sms_sql)
    #API密钥
    # accessKeyId = "LTAI4Frh8FxwTePrgPjSoXvQ"
    # accessKeySecret = "xWX5DutTDtdZp7XHTp3qteHvJe6c23"
    # #签名
    # SignName = "Longersec"
    # #模版编号
    # TemplateCode = "SMS_186953462"
    print(config)
    accessKeyId = config[0][0]

    accessKeySecret = config[0][1]
    SignName = config[0][2]
    TemplateCode = config[0][3]

    ali = AliyunSms(accessKeyId, accessKeySecret, SignName)
    # 给id默认值
    send_id = -1
    try:
        # 接收传入的参数
        send_id = sys.argv[1]
    except:
        send_id = 0
        print("没有传入参数")
    send_sms_content = "select id,mobile,contents,result,fail_count from lsblj_sms_log where id=%s;"
    param = [send_id]
    _result = conn.fetchone(send_sms_content, param)

    # 判断查询的数据是否为空，不为空，则查找发送信息，发送邮件
    if _result != None:

        currnet_id = _result[0]
        mobile = _result[1]
        content = _result[2]
        result = _result[3]
        fail_counts = _result[4]
        if result == 0 and fail_counts < 5:
            try:
                template = {
                    'code':content,
                }
                ali.debug_print("发送短信:" + str(currnet_id))
                res = res = ali.send_sms(mobile, template,TemplateCode )
                ali.debug_print("发送的结果%s" % res["Message"])
                if res["Message"] == "OK":
                    now = time.strftime("%Y-%m-%d %H_%M_%S")
                    param_success = [now, 1, currnet_id]
                    update_fail = "update lsblj_sms_log set send_time = %s,result = %s where id = %s;"
                    res = conn.update(update_fail, param_success)
                    ali.debug_print("发送短信成功:%s,内容：%s" % (currnet_id,content) )
                else:
                    ali.debug_print("发送短信失败")
                    fail_counts += 1
                    param_fail = [0, fail_counts, currnet_id]
                    update_fail = "update lsblj_sms_log set result = %s,fail_count = %s where id = %s;"
                    res = conn.update(update_fail, param_fail)
            except:
                ali.debug_print("发送短信失败：%s" % str(currnet_id))
                fail_counts += 1
                param_fail = [0, fail_counts, currnet_id]
                update_fail = "update lsblj_sms_log set result = %s,fail_count = %s where id = %s;"
                res = conn.update(update_fail, param_fail)

        elif result == 1:
            ali.debug_print("短信已经发送: %s" % str(currnet_id))
        elif fail_counts >= 5:
            ali.debug_print("短信发送失败大于等于5次，停止发送: %s" % str(currnet_id))
        else:
            fail_counts += 1
            send_error_v = [0, fail_counts, currnet_id]  # 参数列表
            send_error = "update lsblj_sms_log set result = %s,fail_count = %s where id = %s;"  # sql语句，更新字段
            res = conn.update(send_error, send_error_v)
            ali.debug_print("发送短信失败")


    elif send_id == None:  # None,False,0
        getAll_sms = "select id,mobile,contents,result,fail_count from lsblj_sms_log;"
        All_result = conn.fetchall(getAll_sms)
        if All_result:
            for temp in All_result:
                currnet_id = temp[0]
                mobile = temp[1]
                content = temp[2]
                result = temp[3]
                fail_counts = temp[4]

                if result == 0 and fail_counts < 5:
                    try:
                        template = {
                            'content': content,
                        }
                        ali.debug_print("发送短信:" + str(currnet_id))
                        res = res = ali.send_sms(mobile, template, TemplateCode)
                        ali.debug_print("发送的结果: %s" % res["Message"])
                        if res["Message"] == "OK":
                            now = time.strftime("%Y-%m-%d %H_%M_%S")
                            param_success = [now, 1, currnet_id]
                            update_fail = "update lsblj_sms_log set send_time = %s,result = %s where id = %s;"
                            res = conn.update(update_fail, param_success)
                            ali.debug_print("发送短信成功:%s,内容：%s" % (currnet_id,content) )
                        else:
                            ali.debug_print("发送短信失败:%s" % currnet_id)
                            fail_counts += 1
                            param_fail = [0, fail_counts, currnet_id]
                            update_fail = "update lsblj_sms_log set result = %s,fail_counts = %s where id = %s;"
                            res = conn.update(update_fail, param_fail)
                    except:
                        ali.debug_print("发送短信失败：%s" % str(currnet_id))
                        fail_counts += 1
                        param_fail = [0, fail_counts, currnet_id]
                        update_fail = "update lsblj_sms_log set result = %s,fail_counts = %s where id = %s;"
                        res = conn.update(update_fail, param_fail)
                elif result == 1:
                    ali.debug_print("短信已经发送: %s" % str(currnet_id))
                elif fail_counts >= 5:
                    ali.debug_print("短信发送失败大于等于5次，停止发送: %s" % str(currnet_id))
                else:
                    fail_counts += 1
                    send_error_v = [0, fail_counts, currnet_id]  # 参数列表
                    send_error = "update lsblj_sms_log set result = %s,fail_counts = %s where id = %s;"  # sql语句，更新字段
                    res = conn.update(send_error, send_error_v)
                    ali.debug_print("短信发送失败")
        else:  # None,False,0
            ali.debug_print('没有数据.')
