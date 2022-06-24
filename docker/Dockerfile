# Set base image (host OS)
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./ ./

# Install any dependencies
RUN apk update && apk upgrade && pwd && ls -al && \
pip install -r requirements.txt

# Specify the command to run on container start
CMD [ "python", "./EmpApp.py" ]