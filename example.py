# import lib
import requests
import psycopg2

def getdata(api):
    # A Tuấn làm
    # Get data from api
    data = requests.get(api)
    # covert list of tuple to insert database
    data_insert = []
    for i in data.json()['Countries']:
        data_insert.append(tuple(i.values())[0:11])
    return data_insert

def insert_to_postgres(command,record):
    #anh Trí
    try:
        #create connection
        connection = psycopg2.connect(user = 'postgres',
                                      password = "647678",
                                      host = "localhost",
                                      port = "5432",
                                      database = "dbtest")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")
        cursor.execute(''' truncate public."summarize" ''')
        #  Command
        cursor.executemany(command,record)
        # commit
        connection.commit()
        #record = cursor.fetchall()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

if __name__ == '__main__':
    api = 'https://api.covid19api.com/summary'
    record = getdata(api)
    command = (''' INSERT INTO public."summarize"(id, Country, "CountryCode", "Slug", "NewConfirmed", "TotalConfirmed", "NewDeaths", "TotalDeaths", "NewRecovered", "TotalRecovered", "Date") 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)  ;  ''')
    insert_to_postgres(command,record)
    # run command : python "exmaple.py"







