import os
import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import json


def lambda_handler(event, context):
    REDSHIFT_DATABASE = os.environ['REDSHIFT_DATABASE']
    REDSHIFT_USER = os.environ['REDSHIFT_USER']
    REDSHIFT_PASSWD = os.environ['REDSHIFT_PASSWD']
    REDSHIFT_PORT = os.environ['REDSHIFT_PORT']
    REDSHIFT_ENDPOINT = os.environ['REDSHIFT_ENDPOINT']

    limit = 20
    offset = 0
    if 'queryStringParameters' in event:
        dados = event["queryStringParameters"]
        if dados:
            if dados.get("limit"):
                if isinstance(dados.get("limit"), int):
                    limit = dados.get("limit")
            if dados.get("offset"):
                if isinstance(dados.get("offset"), int):
                    offset = dados.get("offset")
    REDSHIFT_QUERY = "select * from dbt_imovel.imovel limit {} offset {}".format(limit, offset)
    try:
        conn = psycopg2.connect(
            dbname=REDSHIFT_DATABASE,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWD,
            port=REDSHIFT_PORT,
            host=REDSHIFT_ENDPOINT)
    except Exception as ERROR:
        print("Connection Issue: " + ERROR)
        sys.exit(1)

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        dados = cursor.execute(REDSHIFT_QUERY)
        cursor.close()
        conn.commit()
        conn.close()
        return {
            'statusCode': 200,
            'body': json.dumps(dados)
        }
    except Exception as ERROR:
        print(ERROR)
        sys.exit(1)