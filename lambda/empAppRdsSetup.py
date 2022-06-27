import sys
import logging
import pymysql
from botocore.client import Config
import boto3

session = boto3.session.Session()
config = Config(connect_timeout=1, retries={'max_attempts': 5})
client = session.client(
    service_name='secretsmanager',
    region_name='us-east-2',
    config=config
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#rds settings
logger.info("retrieving rds endpoint from secrets manager")
rds_host  = client.get_secret_value(SecretId="RDSEndpoint")['SecretString']
name = "admin"
logger.info("retrieving rds pass")
password = client.get_secret_value(SecretId="RDSPass")['SecretString']
db_name = "employee"

try:
    logger.info("attempting to connect")
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=1)
    logger.info("connection successful")
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
    logger.info("executing queries")
    with conn.cursor() as cur:
        cur.execute("create database employee;")
        logger.info("created database")
        cur.execute("use employee; create table employee(empid varchar(20), fname varchar(20), lname varchar(20), pri_skill varchar(20), location varchar(20));")
        logger.info("created employee table")
        conn.commit()