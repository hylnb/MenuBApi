import mysql.connector
from config import Config

def init_database():
    try:
        # 首先创建与MySQL的连接（不指定数据库）
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        print(f"数据库 {Config.MYSQL_DB} 创建成功！")
        
        # 切换到新创建的数据库
        cursor.execute(f"USE {Config.MYSQL_DB}")
        
        # 创建employees表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            position VARCHAR(100) NOT NULL
        )
        """
        cursor.execute(create_table_sql)
        print("employees表创建成功！")
        
        # 插入一些测试数据
        insert_data_sql = """
        INSERT INTO employees (name, email, position) VALUES 
        ('张三', 'zhangsan@example.com', '开发工程师'),
        ('李四', 'lisi@example.com', '产品经理'),
        ('王五', 'wangwu@example.com', '设计师')
        """
        try:
            cursor.execute(insert_data_sql)
            conn.commit()
            print("测试数据插入成功！")
        except mysql.connector.Error as err:
            if err.errno == 1062:  # 重复键错误
                print("测试数据已存在，跳过插入。")
            else:
                raise err
                
    except mysql.connector.Error as err:
        print(f"错误: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_database() 