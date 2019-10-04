"""
-------------------------------------------------------------------------------------------------
Description: to perform different database operations
Author: Danial Ahmed, Ahmad Afraz Khan, Taha Bilal Gillani

Modification Log:
---------------------------------------------------------------------------------------------------
Date						Author					                                    Description
---------------------------------------------------------------------------------------------------
23/09/2019					Danial Ahmed, Ahmad Afraz Khan, Taha Bilal Gillani	    	Final draft.
---------------------------------------------------------------------------------------------------\
"""

import psycopg2
from qa_automation.aws import s3Helper
import pandas as pd

class dbHelper:

    def __init__(self):

        self.s3_helper = s3Helper.s3Helper()

    @staticmethod
    def db_connection(connection_info):
        """
        regular connection to RDS DB instance
        @connection_info: a dict containing DB connection info
        """

        host = connection_info["Host"]
        database = connection_info["DatabaseName"]
        username = connection_info["UserName"]
        password = connection_info["Password"]
        port = connection_info["Port"]

        try:
            connection = psycopg2.connect(dbname=database,
                                          host=host,
                                          port=port,
                                          user=username,
                                          password=password)

            cursor = connection.cursor()
            return cursor, connection

        except (Exception) as error:
            raise (error)

    def ssl_db_connection(self, connection_info):
        """
        for encrypted RDS DB instance connection
        @connection_info: a dict containing DB connection info
        """

        host = connection_info["Host"]
        database = connection_info["DatabaseName"]
        username = connection_info["UserName"]
        password = connection_info["Password"]
        port = connection_info["Port"]
        ssl_certificate = connection_info['SSLCertificate']

        certificate_file = ssl_certificate

        # if certificate has to be downloaded from s3
        if ssl_certificate.find('s3://') != -1:
            certificate_file = self.s3_helper.download_object(ssl_certificate)

        try:
            connection = psycopg2.connect(dbname=database,
                                          host=host,
                                          port=port,
                                          user=username,
                                          password=password,
                                          sslmode='prefer',
                                          sslrootcert="'" + certificate_file + "'")

            cursor = connection.cursor()
            return cursor, connection

        except Exception as error:
            raise ValueError(error)

    # RDS Operations
    def connect_to_rds(self, rds_credentials):
        """
        for connecting redshift cluster

        @rds_credentials: a dictionary containing credentials required for connection to an RDS database
        """
        host = rds_credentials["Host"].split(':')[0]
        port = rds_credentials["Host"].split(':')[1]
        rds_credentials["Host"] = host
        rds_credentials["Port"] = port

        if rds_credentials.get('SSLCertificate') is not None:
            return self.ssl_db_connection(rds_credentials)
        else:
            return self.db_connection(rds_credentials)

    def perform_query(self, query, cur, con):
        """
        executes query & closes connection
        """
        try:
            cur.execute(query)
            con.commit()
        except Exception as e:
            raise ValueError(e)
            self.disconnect_from_DB(cur, con)
        self.disconnect_from_DB(cur, con)

    def delete_rows_rds(self, row_data):
        """
        this function deletes specific rows from a rds database based on given conditions

        @credentials: it contains all information required to connect to a database like, db_name, schema etc
        @query_data: data required to make query
        """
        credentials=row_data['Credentials']
        print('this is table')
        operator = row_data['Condition']['Operator']

        # forming query

        if operator == '=':
            where_clause_value = row_data['Condition']['Value']
            where_clause_value = "'" + where_clause_value + "'"
            query = "delete from " + row_data['TableName'] + " where (" + row_data['Condition'][
                'FieldName'] + " = " + where_clause_value + ");"

        # connecting rds cluster
        cur, con = self.connect_to_rds(credentials)
        self.perform_query(query, cur, con)

    def delete_rds_table(self, query_data, rds_credentials):
        """
        droping the whole table

        @rds_credentials: a dictionary containing credentials required for connection to an RDS database
        @table: table name to be dropped
        """

        cursor, connection = self.connect_to_rds(rds_credentials)
        query = "DROP TABLE {} ;".format(query_data["Table"])
        self.perform_query(query, cursor, connection)

    def get_rds_table(self, rds_credentials, Configurations):
        table_name = Configurations["TableName"]
        cursor, connection = self.connect_to_rds(rds_credentials)

        try:
            query = "SELECT * FROM "+table_name
            cursor.execute(query)
            result = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

        except (Exception, psycopg2.Error) as error:
            self.disconnect_from_DB(cursor, connection)
            raise ("Error while connecting to Database", error)

        self.disconnect_from_DB(cursor, connection)
        return result, col_names


    #RedShift Functions

    def connect_to_redshift(self,redshift_credentials):
        """
        for connecting redshift cluster

        @redshift_credentials: a dictionary containing credentials required for connection
        """

        host = redshift_credentials["Host"].split(':')[0]
        port = redshift_credentials["Host"].split(':')[1]
        redshift_credentials["Host"] = host
        redshift_credentials["Port"] = port

        if redshift_credentials.get('SSLCertificate') is not None:
            return self.ssl_db_connection(redshift_credentials)
        else:
            return self.db_connection(redshift_credentials)
        try:
            connection = psycopg2.connect(dbname=database,
                                          host=host,
                                          port=port,
                                          user=username,
                                          password=password)

            cursor = connection.cursor()
            return cursor, connection

        except (Exception, psycopg2.Error) as error:
            raise ValueError("Error while connecting to Database", error)

    def get_redshift_table(self, rds_credentials, Configurations):
        database = rds_credentials["DatabaseName"]
        schema = Configurations["Schema"]
        table_name = Configurations["TableName"]
        cursor, connection = self.connect_to_redshift(rds_credentials)

        try:
            query = "SELECT * FROM "+database+"."+schema+"."+table_name
            cursor.execute(query)
            result = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]


        except (Exception, psycopg2.Error) as error:
            self.disconnect_from_DB(cursor, connection)
            raise ("Error while connecting to Database", error)

        self.disconnect_from_DB(cursor, connection)
        return result, col_names

    def delete_rows_redshift(self, Configurations, credentials):
        """
        this function deletes specific rows from a redshift database based on given conditions

        @credentials: it contains all information required to connect to a database like, db_name, schema etc
        @query_data: data required to make query
        """

        operator = Configurations['Condition']['Operator']
        vartype = type(Configurations['Condition']['FieldTwo'])

        # forming query
        where_clause_second_field = Configurations['Condition']['FieldTwo']
        if vartype == str:
            where_clause_second_field = "'"+where_clause_second_field+"'"
            query = "DELETE from "+credentials['DatabaseName']+'.'+Configurations['Schema']+"."+Configurations['Table']+" where ("+Configurations['Condition']['FieldOne']+" = "+where_clause_second_field+");"
        else:
            query = "DELETE from "+credentials['DatabaseName']+'.'+Configurations['Schema']+"."+Configurations['Table']+" where ("+Configurations['Condition']['FieldOne']+" = "+str(where_clause_second_field)+");"
            # connecting redshift cluster
            cur, con = self.connect_to_redshift(credentials)
            cur.execute(query)
            con.commit()
            self.disconnect_from_DB(cur,con)

    def delete_redshift_table(self, Configurations, redshift_credentials):
        """
        droping the whole table

        @redshift_credentials: a dictionary containing credentials required for connection to an RDS database
        @Configurations: data to formulate query for deleting table
        """

        cursor, connection = self.connect_to_redshift(redshift_credentials)

        try:
            query = "DROP "+redshift_credentials['DatabaseName']+'.'+Configurations['Schema']+"."+Configurations['Table']+ ";"
            cursor.execute(query)
        except (Exception, psycopg2.Error) as error:
            raise("Error while connecting to Database", error)

        self.disconnect_from_DB(cursor, connection)

    def disconnect_from_DB(self, cursor, connection):
        cursor.close()
        connection.close()

    def insert_record(self, record_info):
        """
        inserts a record in a database table
        @record_info: a dictionary containing info about record to be inserted.
        """

        table = record_info['TableName']
        schema = record_info['Schema']
        values = record_info['Values']

        query = 'INSERT INTO '
        query_schema = ' ('
        query_values = "("
        i, j = 0, 0

        # generating SCHEMA & VALUES part of query
        for schema_field in schema:

            field_type = schema_field['Type']
            field_name = schema_field['Name']

            if len(schema) - 1 == i:
                query_schema += field_name + ")"
                j = i

            else:
                query_schema += field_name + ","
                i += 1
                j = i - 1

            for schema_value in values:
                value_name = schema_value['Field']
                original_value = schema_value['Value']

                if value_name == field_name:

                    if original_value == '' or original_value.lower() == 'null':

                        if len(values) - 1 == j:
                            query_values += "NULL)"
                        else:
                            query_values += "NULL,"
                        break
                    else:
                        if len(values) - 1 == j:
                            query_values += "'" + original_value + "')"
                        else:
                            query_values += "'" + original_value + "',"
                        break

                    # contains credentials for RDS connection
        query += table + " " + query_schema + " VALUES" + query_values

        # connecting database
        cur, con = self.connect_to_rds(record_info['Credentials'])
        self.perform_query(query, cur, con)
