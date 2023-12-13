# using python image version 3.9
FROM python:3.9

# sets working dir to backend
WORKDIR /backend

# copy reqiuement.txt into the current working dir
COPY requirements.txt .

# command to install the python dependencies
RUN pip install -r requirements.txt

# copy all the files into the working dir
COPY . .

# open port 8000 for backend access
EXPOSE 8000

# command to run the server on the network with port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



