# This is a config file to store key's
import os
from dataclasses import dataclass


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = ROOT_DIR + '/' + 'storage' + '/' + 'log'


# Slack
@dataclass
class SlackConfig:
    CHANNEL = 'stats-career-yonsei'
    SLACK_API_TOKEN = ""


if __name__ == '__main__':
    print(ROOT_DIR)
