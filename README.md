# Zabbix alert script for [Slack](https://slack.com/)

## Requirements

- Python 2

## Installation

- Set up a new [incoming webhook](https://my.slack.com/services/new/incoming-webhook/) for your Slack team
- Set token in slack.cfg (the part in the URL after https://hooks.slack.com/services/)
- Review other configuration options in slack.cfg. Check out subject matching regular expressions for status color support in Slack messages. To match for trigger severity, make sure this info is included in the subject, default configuration matches following subject:
```
[{TRIGGER.STATUS}] ({TRIGGER.SEVERITY}): {TRIGGER.NAME}
```

- Create new media type in Zabbix 

![Media Type](doc/zabbix-media-type.png)

- Copy slack.py and slack.cfg to /usr/lib/zabbix/alertscripts
- Make slack.py executable for the user running Zabbix server

## Usage

### Zabbix

Use receiving user or channel in the _Send to_ field when adding a new media for a user. 

### CLI

```
usage: slack.py [-h] [-v] [-c [C]] to subject message

Zabbix Slack Client

positional arguments:
  to             Receiving user or channel
  subject        Message subject
  message        Message body

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -c [C]         The configuration file to use (default: slack.cfg)
```

## License

zabbix-slack is licensed under the MIT License.