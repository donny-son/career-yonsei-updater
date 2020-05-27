from slack import WebClient
from config import SlackConfig
from slack.errors import SlackApiError

slack_client = WebClient(token=SlackConfig.SLACK_API_TOKEN)


def post_slack(txt: str):
    try:
        slack_client.chat_postMessage(
            channel=SlackConfig.CHANNEL,
            text=txt
        )
    except SlackApiError as e:
        assert e.response['error']


if __name__ == '__main__':

    post_slack('hellow world')
