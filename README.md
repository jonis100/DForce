# DForce

## _The phishing websites attacker_

DForce is a tool for attacking phishing websites by flooding his Databases in junk. This implemented by sending randomized emails and passwords, in order to disrupt target website activity.


## Features

- Using [Tor Project] (The Onion Router) to change IP when the program is blocked.
- Work only on phishing websites with pattern of :
    - Field of username-email address
    - Field of passowrd
    - Submit or Login button


## Tech

DForce uses a number of open source projects to work properly:

- [Selenium] - Web scraping project
- [Selenium wire] - Extends Selenuim, give you access to the underlying requests
- [Tor Project] - Let your program switch IP when it blocked, like VPN **optional**.


And of course DForce itself is open source with a public repository on GitHub.

DForce also need [Chrome web browser](https://www.google.com/chrome/?brand=CHBD&brand=CHBD&gclid=EAIaIQobChMI1tuC9tWm_AIVehoGAB2_PQe3EAAYASABEgIwl_D_BwE&gclsrc=aw.ds) and his [driver](https://chromedriver.chromium.org/downloads) for Selenium.

## Installation

DForce requires [Python](https://www.python.org/) 3.8+ and Chrome browser to run.
**NOTE: for some independecies reasons it works me on Chrome version 106 and not above**
1. Clone the repository: ``` git clone https://github.com/jonis100/DForce.git```
2. Navigate to the directory: ``` cd DForce```
3. Install dependencies:
```sh
python -m pip install selenium  
pip install selenium-wire
```

For TOR installation:

```sh
apt install tor
```

## Configurations 

Before you run DForce please copy the elements names of text fields in the website target and paste it in his place in dictionary at page_detales.py file:
![alt text](https://github.com/jonis100/DForce/blob/main/Images/Screenshot1eddited.jpg)
![alt text](https://github.com/jonis100/DForce/blob/main/Images/Screenshot2eddited.jpg)
![alt text](https://github.com/jonis100/DForce/blob/main/Images/Screenshot3eddited.jpg)
**optional configuration:** After that you can configure use tor or not and more at conf.py file. 

## Usage 
To use DForce, run following command: ```python main.py [Phishing_URL]```

## Testing

This project tested over local servers only.
1. [Zphisher](https://github.com/htr-tech/zphisher) 
    issues: after few request stop recording
2. Wordpress local site over [XAMPP](https://www.apachefriends.org/)
    

# *The Tor feature not tested properly yet*

## Contributing
If you want contribute to DForce you more then wellcome!

## License

MIT


   [Tor Project]: <https://www.torproject.org/>
   [Selenium]: <https://www.selenium.dev/>
   [Selenium wire]:  <https://pypi.org/project/selenium-wire/>


