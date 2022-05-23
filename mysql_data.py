#
import pymysql
import pandas as pd


class Mysql_csv(object):

    # 定义一个init方法，用于读取数据库
    def __init__(self):
        # 读取数据库和建立游标对象
        self.connect = pymysql.connect(host="192.168.1.207",
                                       port=3306, user="lujiahui", password="lujiahui",
                                       database="3d66_pai_test", charset="utf8")
        self.cursor = self.connect.cursor()

    # 定义一个del类，用于运行完所有程序以后关闭数据源和游标对象
    def __del__(self):
        self.connect.close()
        self.cursor.close()

    # 读取csv文件的列索引，用来建立数据表的字段
    def read_csv_colnmns(self):
        # 读取csv文件的索引
        csv_name = 'data.csv'
        data = pd.read_csv(csv_name, sep='/t', encoding="utf-8")
        data_list = data.values
        return data_list

    # 往数据库写入数据
    def write_mysql(self):
        # 在数据表中写入数据，因为数据是列表类型，把他转化为元组更符合sql语句
        for i in self.read_csv_colnmns():
            # print(i)
            data = tuple(i[0].split('\t'))
            print(data)
            sql = "insert into res_keyname_cut values{}".format(data)
            self.cursor.execute(sql)
            self.commit()
        print("\n数据写入完成")

    # 定义一个确认事务运行的方法
    def commit(self):
        self.connect.commit()

    # 新建数据库表
    def create(self):
        # 若已有数据库表shanxi，则删除
        query = "drop table if exists res_keyname_cut;"  # 更改表名
        self.cursor.execute(query)
        # 创建数据表，用刚才提取的列索引作为字段
        data_2 = self.read_csv_colnmns()
        # 根据自己要创建的表格更改sql语句
        sql = "create table if not exists res_keyname_cut(id int(50) not null,title varchar(50) not null, classifyName varchar(50) not null, baseClassifyName varchar(50) not null,imgUrl varchar(2000) not null," \
              "add_time int(11) not null,keyname_list varchar(2000) not null,primary key(id))default charset=utf8;"
        self.cursor.execute(sql)
        self.commit()

    # 运行程序
    def run(self):
        self.create()
        self.write_mysql()


# 封装函数
def main():
    sql = Mysql_csv()
    sql.run()


if __name__ == '__main__':
    main()


