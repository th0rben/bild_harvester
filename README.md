# News Scraper

A program for downloading online articles and saving them in a SQLLite database.

## Getting Started

### Installing & Set Up

1. You need to have python 3.X and Beautiful Soup installed.
```bash
pip install beautifulsoup4
```

2. Clone the repository
```bash
mkdir git
cd git
git clone https://github.com/th0rben/news-scraper.git
```
3. For sending e-mails you need to create a file named: **login_data.py** in src folder. It should look this (example for using gmail):
```python
sender = "sender@gmail.com"
recipient = "recipient"
password = "password"
subject = "subject"
server = "smtp.gmail.com"
port = 465
```
### Run the program

#### Run it manually
Execute the **main.py** file
#### Run it automatically (linux only)
To scrap every day at 12:00 execute:
(adds cronjob to crontab)
```bash
cd where/you/saved/it/news-scraper
sudo chmod +x setup.sh
.setup.sh
sudo crontab -e
0 18 * * 1 /home/pi/git/news-scraper/cron/cron.sh
```

If you want to change the frequency or time: Change [cronjob.txt](/src/cron/cronjob.txt) 

For mor information see: [https://en.wikipedia.org/wiki/Cron](https://en.wikipedia.org/wiki/Cron)

## Running the tests

Until today there are no tests.

## Deployment

It would be great if you mention any mistakes you stumble over.

## Built With

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python library for pulling data out of HTML and XML files
* [Eclipse](https://www.eclipse.org/) - IDE
* [PyDev](https://marketplace.eclipse.org/content/pydev-python-ide-eclipse) - Python IDE for Eclipse

## Contributing

It would be great if you mention any mistakes you stumble over.

## Versioning

[27.07.2018] - Scrap articles vom bild.de

This project is still in the Beta-Version

## Authors

* **th0rben** - *Initial work* - [th0rben](https://github.com/th0rben)

## License

This project is licensed under the GPL License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This project is inspired by the Spiegel Mining project by [D. Kriesel](dkriesel.com)

