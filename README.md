Project helps make the job search more relevant to certain user defined parameters.

Usage of the http://angel.co/api 


#Environment Installation

Python 2.7
virtualenv


virtualenv {{ env_name }}
cd {{ env_name }}
source bin/activate


#For python packages 
pip install requirements.txt 


#Other project related dependencies
npm install
bower install


#Start the watcher and grunt tasks for test & build process.
grunt dev