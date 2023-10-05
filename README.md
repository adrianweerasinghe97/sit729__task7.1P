# sit729\_\_task7.1P

In order to run this application please follow the below steps

1. Install Mosquitto.
2. Change the MongoURI
3. In the directory of the Mosquitto installed file open command prompt
4. enter the following command in cmd "mosquitto -v"
5. run the python code "python Task7.py"
6. To simulate the motion sensors open another cmd in the same direcory of the mosquitto installed folder
7. run this command "mosquitto_pub.exe -h localhost -t "motion/detections" -m "<room number upto 10 rooms>"
