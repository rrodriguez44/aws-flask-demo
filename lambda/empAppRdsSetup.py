import sys
import logging
import pymysql
import boto3

session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name='us-east-2'
)

#rds settings
rds_host  = client.get_secret_value(SecretId="RDSEndpoint")['SecretString']
name = "admin"
password = client.get_secret_value(SecretId="RDSPass")['SecretString']
db_name = "employee"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
    with conn.cursor() as cur:
        cur.execute("create database employee;")
        cur.execute("use employee; create table employee(empid varchar(20), fname varchar(20), lname varchar(20), pri_skill varchar(20), location varchar(20));")
        conn.commit()