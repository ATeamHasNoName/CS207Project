# Kill previous instances
sudo pkill -f httpd
sudo pkill -f run.py
sudo pkill -f flaskr.py
sudo pkill -f python
sudo rm /etc/nginx/sites-enabled/*
sudo rm /etc/nginx/sites-available/app_server_nginx.conf
sudo rm /etc/nginx/sites-available/api_server_nginx.conf

sudo cp ~/CS207Project/CS207Project/MS3/app-server/conf/app_server_nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/app_server_nginx.conf /etc/nginx/sites-enabled/app_server_nginx.conf

sudo service nginx restart

printf "\nMoving Repos Assets to www...\n"

# Reinitialize PSQL db
psql -c "DROP TABLE timeseries;"
psql -c "CREATE TYPE level AS ENUM ('A', 'B', 'C', 'D', 'E', 'F');"
psql -c "CREATE TABLE timeseries (
    tid VARCHAR(32) PRIMARY KEY,
    mean float(16) NOT NULL,
    std float(16) NOT NULL,
    blarg float(16) NOT NULL,
    level level NOT NULL 
);"

# Recreate /home/www
sudo rm -r /home/www
sudo mkdir /home/www

sudo rm /home/www/CS207Project -r
# Need to import the whole project
sudo cp ~/CS207Project /home/www/ -r

printf "\nStarting Application Servers...\n"

cd /home/www/CS207Project/CS207Project/MS3/api-server/ && nohup python3 flaskr.py & disown
cd /home/www/CS207Project/CS207Project/MS3/app-server/ && nohup python3 run.py & disown

sudo mkdir /home/www/DB

# Permissions needed to be given, if not write/delete of files cannot be done
sudo chmod 777 -R /home/www

# Install portalocker
cd /home/www/CS207Project/CS207Project/MS2/portalocker && sudo python3 setup.py install && cd -

# Run socket server and generate vantage points / time series
cd /home/www/CS207Project/CS207Project/MS3/socket-server/ && nohup python3 server.py localhost 5002 0 & disown

printf "\nPython Processes...\n"
ps aux|grep python3

printf "\nFINISHED!\n"

printf "\nTry hitting the public domain now!\n"
