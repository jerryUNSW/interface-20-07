import sqlite3
from sqlite3 import Error
database_name = 'test.db'

def create_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_company_info(company_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    sql_str = """SELECT * FROM Business where bname = "{}"  """.format(company_name)
    company = cursor.execute(sql_str).fetchone()
    connection.close()
    return company

# get top k result order by attribute
def get_ranking_companies(attribute, K):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    sql_str = """SELECT * FROM Business order by {} limit {} """.format(attribute, K)
    companies = cursor.execute(sql_str).fetchall()
    return companies

def build_database(db_name):
    connection = sqlite3.connect(db_name)

    cursor = connection.cursor()

    sql_file = open("sql/schema.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    sql_file = open("sql/insert.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    connection.close()
    return 

