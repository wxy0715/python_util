import pymysql
import configparser
import sys
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from sm4 import SM4Key

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

try:
    bytes.fromhex
except AttributeError:
    def h2b(byte_string):
        return bytes(bytearray.fromhex(byte_string))
else:
    def h2b(byte_string):
        return bytes.fromhex(byte_string)

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


# 自动发送邮件
def send_email(to_users, title, contents, username, password, send_port, e_ip_add,ssl):
    # 读取测试报告中的内容作为邮件的内容
    # 收件人地址
    global smtp
    reciver_addr = to_users
    # 发送邮箱的服务器地址 qq邮箱是'smtp.qq.com', 163邮箱是'smtp.163.com'
    mail_server = e_ip_add
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    # 邮件标题
    subject = title
    subject = subject
    # 发件人的邮箱及邮箱授权码
    # '1259754696@qq.com'
    username = username
    # 'ljnzyyfyqmongeej'
    password = password  # 注意这里是邮箱的授权码而不是邮箱密码
    # 邮箱的内容和标题
    mail_body = contents
    message = MIMEText(mail_body, 'html', 'utf8')
    message['Subject'] = Header(subject, charset='utf8')
    if ssl==0:
        # 发送邮件，使用的使smtp协议
        smtp = smtplib.SMTP()
        sport = send_port
        smtp.connect(mail_server, sport)
        smtp.login(username, password)
        smtp.sendmail(username, reciver_addr.split(','), message.as_string())
    if ssl==1:
        # 开启ssl
        smtp = smtplib.SMTP_SSL(mail_server,send_port)
        print(username,password)
        smtp.login(username,password)
        print('login success')
        smtp.sendmail(username, reciver_addr.split(','), message.as_string())


    smtp.quit()


if __name__ == '__main__':
    conn = MysqlHelper(host=db_host, user=db_user, password=db_pwd, database=db_name,
                                   port=db_port)
    # conn = MysqlHelper(host="127.0.0.1", user="root", password="123456", database="send_email",
    #                                    port=3306)
    conn.connect()
    send_id = -1
    try:
        # 接收传入的参数
        send_id = sys.argv[1]
    except:
        send_id = 0
        print("没有传入参数")

    r1=conn.fetchall("select pkey from lsblj_config_password_encrypt_key limit 1")
    passkey = r1[0][0]
    key0 = SM4Key(h2b(passkey))

    # 获取邮箱的信息
    get_email_sql = "select id,ip,`ssl`,port,username,password from lsblj_config_email"

    User_Pwd = conn.fetchall(get_email_sql)
    # 邮件服务器地址
    e_ip_add = User_Pwd[0][1]
    # 是否开启ssl
    ssl = User_Pwd[0][2]
    # 端口
    send_port = User_Pwd[0][3]
    # 邮箱用户名
    username = User_Pwd[0][4]
    # 授权码
    password = key0.decrypt(h2b(User_Pwd[0][5]),padding=True).decode()

    # 测试实例
    # ssl = 1
    # send_port = 465
    # e_ip_add = "smtp.qq.com"
    # username = "1259754696@qq.com"
    # password='ljnzyyfyqmongeej'

    get_Param_Id = "select id,to_users,to_title,to_contents,result,fail_count,alert_id from lsblj_email_log where id=%s;"
    params = [send_id]
    print(params)
    data = conn.fetchone(get_Param_Id, params)
    print(data)

    # 判断查询的数据是否为空，不为空，则查找发送信息，发送邮件
    if data != None:

        currnet_id = data[0]
        to_user = data[1]
        to_tile = data[2]
        to_content = data[3]
        result = data[4]
        fail_counts = data[5]
        alert_id = data[6]
        if result == 0 and fail_counts < 5:
            try:

                print("发送邮件...:" + str(currnet_id))
                send_email(to_user, to_tile, to_content, username, password, send_port, e_ip_add,ssl)
                now = time.strftime("%Y-%m-%d %H_%M_%S")
                param_success = [now, 1, currnet_id]
                update_fail = "update lsblj_email_log set send_time = %s,result = %s where id = %s;"
                res = conn.update(update_fail, param_success)
                if alert_id > 0 :
                    param_success = [1, alert_id]
                    update_success = "update lsblj_alert_log set isemail = %s,email_count=email_count+1,email_time = NOW() where id = %s"
                    print(update_success)
                    conn.update(update_success, param_success)
                print("成功")
            except Exception as e:
                print("发送邮件失败:" + str(currnet_id)+","+e)
                fail_counts += 1
                param_fail = [0, fail_counts, currnet_id]
                update_fail = "update lsblj_email_log set result = %s,fail_count = %s where id = %s;"
                res = conn.update(update_fail, param_fail)
                if alert_id > 0 :
                    param_fail = [0, alert_id]
                    update_fail = "update lsblj_alert_log set isemail = %s,email_count=email_count+1, email_time = NOW() where id = %s"
                    conn.update(update_fail, param_fail)
                print("失败")
        elif result == 1:
            print("邮件已经发送:" + str(currnet_id))
        elif fail_counts >= 5:
            print("邮件发送失败大于等于5次，停止发送:" + str(currnet_id))
        else:
            fail_counts += 1
            send_error_v = [0, fail_counts, currnet_id]  # 参数列表
            send_error = "update lsblj_email_log set result = %s,fail_count = %s where id = %s;"  # sql语句，更新字段
            res = conn.update(send_error, send_error_v)
            print("邮件发送失败")


    else:  # None,False,0
        getAll_mail = "select id,to_users,to_title,to_contents,result,fail_count,alert_id from lsblj_email_log;"
        All_result = conn.fetchall(getAll_mail)
        if All_result:
            for temp in All_result:
                currnet_id = temp[0]
                to_user = temp[1]
                to_tile = temp[2]
                to_content = temp[3]
                result = temp[4]
                fail_counts = temp[5]
                alert_id = temp[6]
                print("alert_id %s",alert_id)
                if result == 0 and fail_counts < 5:
                    try:
                        print("发送邮件...:" + str(currnet_id))
                        send_email(to_user, to_tile, to_content, username, password, send_port, e_ip_add,ssl)

                        now = time.strftime("%Y-%m-%d %H_%M_%S")

                        param_success = [now, 1, currnet_id]

                        update_success = "update lsblj_email_log set send_time = %s,result = %s where id = %s"
                        conn.update(update_success, param_success)
                        if alert_id > 0 :
                            param_success = [1, alert_id]
                            update_success = "update lsblj_alert_log set isemail = %s,email_count=email_count+1,email_time = NOW() where id = %s"
                            print(update_success)
                            conn.update(update_success, param_success)
                        print("发送邮件成功:" + str(currnet_id))
                    except:
                        fail_counts += 1
                        param_fail = [0, fail_counts, currnet_id]

                        update_fail = "update lsblj_email_log set result = %s,fail_count = %s where id = %s"

                        conn.update(update_fail, param_fail)
                        if alert_id > 0 :
                            param_fail = [0, alert_id]
                            update_fail = "update lsblj_alert_log set isemail = %s,email_count=email_count+1, email_time = NOW() where id = %s"
                            conn.update(update_fail, param_fail)
                        print("发送邮件失败:" + str(currnet_id))

                elif result == 1:
                    print("邮件已经发送:" + str(currnet_id))

                elif fail_counts >= 5:
                    print("邮件发送失败大于等于5次，停止发送:" + str(currnet_id))

                else:
                    print("邮件发送失败:" + str(currnet_id))


        else:  # None,False,0
            print('没有数据.')
