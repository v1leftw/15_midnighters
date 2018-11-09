# Night Owls Detector

Script searches users who sent solution to task after midnight.
Script uses [API](https://devman.org/api/challenges/solution_attempts/) to get users.
If script can not connect to API on any page it stops and shows existing midnighters if they've been found before getting error.

# Quickstart
Examples of script launch on Linux, Python 3.5

```
$ python3 seek_dev_nighters.py
Searching midnighters...
Error: 'Could not connect to API' occurred on page 4
got midnighter: illarionovanton
got midnighter: ruslansv
got midnighter: julev51188
got midnighter: vpforwork15

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
