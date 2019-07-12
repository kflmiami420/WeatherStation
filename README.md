# Weather station

The repository with all my code for my instructables guide on how to build a weatherstation with Python and Flask.

cd ~
mkdir weatherstation
cd weatherstation

Then we set up our python3 virtual enviroment:

python3 -m pip install --upgrade pip setuptools wheel virtualenv
python3 -m venv --system-site-packages env
source env/bin/activate
python -m pip install mysql-connector-python Flask flask-mysql mysql-connector-python passlib mysql-connector-python-rf

sudo apt install -y python3-venv python3-pip python3-mysqldb mariadb-server uwsgi nginx uwsgi-plugin-python3

sudo mariadb < sql/db_init.sql

git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO 
sudo python3 setup.py install

cd ..
git clone --recursive https://github.com/freedom27/MyPyDHT
sudo python3 setup.py install


You can go ahead and clone my project's code from Github into your project folder.
Go to your user folder and run:
git clone https://github.com/BertVanhaeke/Weatherstation/ temp
mv -v temp/* weatherstation/

Then navigate to the conf folder in weatherstation and all of the files in the folder.

Change all occurences of 'USERNAME' to your username

You will also need to copy both of the .service files to systemd and test them like this:

sudo cp conf/weatherstation-*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start weatherstation-flask.service
sudo systemctl start weatherstation-sensor.service

sudo systemctl status weatherstation-*



We then need to edit the nginx config.

sudo cp conf/nginx /etc/nginx/sites-available/weatherstation
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/weatherstation /etc/nginx/sites-enabled/weatherstation
sudo systemctl restart nginx.service
sudo systemctl status nginx.service


If everthing went well you should be able to run this and get some html printed out in the terminal:

wget -qO - localhost

























By Bert Vanhaeke, 1st Year Student NMCT @ Howest Kortrijk, Belgium
