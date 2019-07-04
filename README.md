# FAKE-NEWS-DETECTION

This application is a client-server application. 

It consist of Ionic Mobile App and a Flask based server that scraps similar articles from multiple sites and check similarity between given article and scrapped articles using LSA WMD and Fuzzy Logic

Required -
1. Node.js and Ionic Framework
2. Python and flask framework

STEPS TO RUN THIS CLIENT APPLICATION
1. Download it, open cmd and navigate to downloaded folder and type npm install (It will install all the node modules)
2. Type ionic serve to run appliaction in browser go to http://localhost:8100/
3. Now you type here the news you want to check

STEPS TO RUN SERVER APPLICATION
1.Go to server folder
2.Download all the dependencies of python files and download and place "GoogleNews-vectors-negative300-SLIM.bin" in server folder 
(https://github.com/eyaler/word2vec-slim/blob/master/GoogleNews-vectors-negative300-SLIM.bin.gz)
3. Run flask server file (server.py)

4.Now type news under evaluation in the browser app and hit the server. It will list the similar articles as well as similarity score
