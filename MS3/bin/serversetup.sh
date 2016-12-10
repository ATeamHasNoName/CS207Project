# printf "\n*******************************************************"
# printf "\nInstalling gunicorn ...\n"
# 
# sudo apt-get --yes --force-yes install gunicorn
# gunicorn --version
# 
# printf "\nSetting up Gunicorn Configurationr\n"

# DANGEROUS but not for new instances
sudo pkill -f httpd
sudo pkill -f run.py
sudo pkill -f flaskr.py
sudo rm /etc/nginx/sites-enabled/*
sudo rm /etc/nginx/sites-available/app_server_nginx.conf
sudo rm /etc/nginx/sites-available/api_server_nginx.conf

sudo cp ~/CS207Project/MS3/app-server/conf/app_server_nginx.conf /etc/nginx/sites-available/
# sudo cp ~/CS207Project/MS3/api-server/conf/api_server_nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/app_server_nginx.conf /etc/nginx/sites-enabled/app_server_nginx.conf
# sudo ln -s /etc/nginx/sites-available/api_server_nginx.conf /etc/nginx/sites-enabled/api_server_nginx.conf

sudo service nginx restart

printf "\nMoving Repos Assets to www...\n"

sudo mkdir /home/www
sudo rm /home/www/app-server -r
sudo rm /home/www/api-server -r
sudo cp ~/CS207Project/MS3/app-server/ /home/www/ -r
sudo cp ~/CS207Project/MS3/api-server/ /home/www/ -r

printf "\nStarting Application Servers...\n"

# cd /home/www/app-server/ && nohup gunicorn app:app -b localhost:8000 & disown
# cd /home/www/api-server/ && nohup gunicorn flaskr:app -b localhost:5001 & disown

cd /home/www/api-server/ && nohup python3 flaskr.py & disown
cd /home/www/app-server/ && nohup python3 run.py & disown

printf "\nPython Processes...\n"
ps aux|grep python3

printf "\nFINISHED!\n"

printf "\nTry hitting the public domain now!\n"

