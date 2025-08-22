import pymysql

#定义工具类MySQLHelper，定义了链接数据库，插入数据，断开链接的方法，方便重复使用
class MySQLHelper:
    def __init__(self):              #初始化
        self.conn = pymysql.connect(
            host='localhost',
            user='*****',        #数据库这里修改为自己的数据库
            password='*****',
            database='*****',
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def insert_article(self, article):
        sql = """
        INSERT INTO articles (
            local_create_time, publish_time, title, url, content,
            view_count, like_count, share_count, view_in_count,
            comments, comment_likes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title=VALUES(title),
            content=VALUES(content),
            view_count=VALUES(view_count),
            like_count=VALUES(like_count),
            share_count=VALUES(share_count),
            view_in_count=VALUES(view_in_count),
            comments=VALUES(comments),
            comment_likes=VALUES(comment_likes),
            updated_at=NOW()
        """
        self.cursor.execute(sql, article)
        self.conn.commit()

    def create_table_if_not_exists(self, table_name):
        sql = f'''
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            local_create_time VARCHAR(32),
            publish_time VARCHAR(32),
            title VARCHAR(512),
            url VARCHAR(1024),
            content TEXT,
            view_count INT,
            like_count INT,
            share_count INT,
            view_in_count INT,
            comments TEXT,
            comment_likes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_article_to_table(self, table_name, article):
        sql = f'''
        INSERT INTO `{table_name}` (
            local_create_time, publish_time, title, url, content,
            view_count, like_count, share_count, view_in_count,
            comments, comment_likes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title=VALUES(title),
            content=VALUES(content),
            view_count=VALUES(view_count),
            like_count=VALUES(like_count),
            share_count=VALUES(share_count),
            view_in_count=VALUES(view_in_count),
            comments=VALUES(comments),
            comment_likes=VALUES(comment_likes),
            updated_at=NOW()
        '''
        self.cursor.execute(sql, article)
        self.conn.commit()

    def get_all_public_account_tables(self, prefix='wx_'):
        sql = f"SHOW TABLES LIKE '{prefix}%';"
        self.cursor.execute(sql)
        return [row[0] for row in self.cursor.fetchall()]

    def get_table_article_count(self, table_name):
        sql = f"SELECT COUNT(*) FROM `{table_name}`;"
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def close(self):
        self.cursor.close()
        self.conn.close()
