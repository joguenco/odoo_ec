* Git
```
sudo apt install git
```
* Python
```
sudo apt install python3-dev python3-pip python3-wheel python3-venv python3-virtualenv
```
```
sudo apt install build-essential libpq-dev libxslt-dev libzip-dev libldap2-dev libsasl2-dev libssl-dev
```
* CSS processor
```
sudo apt install npm
```
```
sudo npm install -g less less-plugin-clean-css
```
* Get odoo source code
```
git clone https://github.com/odoo/odoo.git -b 15.0 --depth=1
```
* Create python virtual environment
```
cd odoo
```
```
virtualenv venv
```
* Activate python virtual environment
```
source ./venv/bin/activate
```
* Update pip
```
pip install -U pip
```
* Install requirements
```
pip install -r requirements.txt
```
* Install source code files
```
pip install -e ./
```