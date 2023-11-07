import pymysql

__database_schema = "'paranapul'"

def connect_to_database():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mhm19951128',
                                 database='paranapul',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_column_length_of_table(column_name, table_name):
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            sql = 'SELECT CHARACTER_MAXIMUM_LENGTH FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '+ __database_schema +' AND TABLE_NAME = '+ table_name +' AND COLUMN_NAME = '+ column_name +''
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return result.get('CHARACTER_MAXIMUM_LENGTH')

            return None
