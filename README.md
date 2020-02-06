# iGenius_Interview_assignment_Deepan_Anbarasan
 Online Currency converter with a web API endpoint
>Assignment: Implement an online currency converter, providing a Web API
> endpoint called convert.
The endpoint must accept HTTP GET requests.

## pre-requisites
- Docker desktop (or) computer with python 3.7.1 installed

## Instructions to run project
- Clone the github repository
- Open command prompt/terminal with admin privileges
- Change the current working directory in the terminal to the directory that
 contains the 'app.py' & Dockerfile from the cloned repository

### If docker available:
- To build the project run the following command 
`docker build -t converterapp:latest .`
- To run the project using docker:
`docker run -it --name converterapp -d -p 5000:5000 converterapp`
- This will make the API available. A sample URL: http://localhost:5000/convert?amount=25&reference_date=2020-02-04&src_currency=USD&dest_currency=INR
- To run the configured test cases,run the following command in the terminal
 `docker container exec -it converterapp py.test`

 ### If docker unavailable:
 - To install the requisite libraries, run the following commands in the
  terminal
    `pip install --upgrade pip`
    `pip install -r requirements.txt `
- To run the project using docker:
`python app.py`
- This will make the API available. A sample URL: http://localhost:5000/convert?amount=25&reference_date=2020-02-04&src_currency=USD&dest_currency=INR
- To run the configured test cases,run the following command in the terminal
 `py.test`
 ##

_**Note:**_ The python code has been written in compliance with **PEP 8 Style Guide
 for Python Code**