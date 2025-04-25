* Git
```
sudo dnf install git
```
* Python
```
sudo dnf install python3.12-devel.x86_64
```
```
sudo dnf group install "development-tools"
sudo dnf install libpq-devel libxslt-devel libzip-devel openldap-devel libsass-devel openssl-devel cairo-devel wkhtmltopdf-devel
```
* CSS processor
```
npm install -g less less-plugin-clean-css
```
* Get odoo source code
```
git clone https://github.com/odoo/odoo.git -b 18.0 --depth=1
```
* Create python virtual environment
```
cd odoo
```
```
python3.12 -m venv venv
```
* Activate python virtual environment
```
source venv/bin/activate
```
* Update pip and tools
```
pip install -U pip
pip install --upgrade wheel
pip install --upgrade setuptools
```
* Install requirements
```
pip install -r requirements.txt
```
* Install source code files
```
pip install -e ./
```
