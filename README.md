# Instagram-bot

## Usage [mac/linux]
* Make sure that your system has Python3 and Pip Installed. 
* Download, install and configure Chrome driver based on your Chrome browser's version: [Downloads link](https://chromedriver.chromium.org/downloads)
* Install Python Virtual Enviromment package.
```
pip install virtualenv
```
* Clone the Repo.
```
git clone https://github.com/supongkiba/instagram-bot.git
```
* Create a virtual environment and activate the source.
```
cd instagram-bot
python3 -m venv env 
source env/bin/activate
```
* Install the dependencies.
```
pip3 install -r requirements.txt
```
* Add your Username(Not Email) and Password in the script[line 183]
```
bot = InstaBot("<username>", "<password>")
```
* Execute the Script.
```
python3 insta-bot.py
```
