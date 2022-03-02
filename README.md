# linkedin-skillbot
Gotta solve em all!

### Usage
Just start and go pretty much. I will add a requirements in the future for now just `pip3 install` whatever python tells you to :)
```
python3 linkedin_parser.py --show --live
```
 - `--show` Opens ChromeDriver in front aka. look how computer make magic and clicky on buttons without doing anything. Otherwise it will start headless.
 - `--live` This sets it to solve actual tests, if not set it will run "practice" (I used this for testing.)
### .env
You should have a `.env` file in the working dir.
```
LINKED_IN_USER=user@name.com
LINKED_IN_PASS=YourPass123!
LINKED_IN_PROFILE=https://www.linkedin.com/in/YOURUSERNAME/
```

