# This is a config file to store key's
import os
from dataclasses import dataclass



DEBUG = True
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = ROOT_DIR + '/' + 'storage' + '/' + 'log'


# Slack
@dataclass
class SlackConfig:
    CHANNEL = {}
    CHANNEL['career'] = 'stats-career-yonsei' if not DEBUG else 'debug'
    CHANNEL['news'] = 'stats-grad-billboard' if not DEBUG else 'debug'
    SLACK_API_TOKEN = ""

if __name__ == '__main__':
    print(ROOT_DIR)
