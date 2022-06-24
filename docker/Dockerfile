# Set base image (host OS)
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./ ./

# Install any dependencies
RUN apk update && apk upgrade && pwd && ls -al && \
pip install -r requirements.txt

RUN which yum

RUN install -y mysql && \
mysql -h $(aws secretsmanager get-secret-value --region us-east-2 --secret-id RDSEndpoint --query SecretString --output text) -u admin --password=$(aws secretsmanager get-secret-value --region us-east-2 --secret-id RDSPass --query SecretString --output text) employee -e "create database employee;" && \
mysql -h $(aws secretsmanager get-secret-value --region us-east-2 --secret-id RDSEndpoint --query SecretString --output text) -u admin --password=$(aws secretsmanager get-secret-value --region us-east-2 --secret-id RDSPass --query SecretString --output text) employee -e "use employee; create table employee(empid varchar(20), fname varchar(20), lname varchar(20), pri_skill varchar(20), location varchar(20));"

# Specify the command to run on container start
CMD [ "python", "./EmpApp.py" ]