from slacker import Slacker
from config import SlackConfig
from slack.errors import SlackApiError

slack = Slacker(SlackConfig.SLACK_API_TOKEN)


def post_slack(txt: str):
    try:
        slack.chat.post_message(
            channel=SlackConfig.CHANNEL,
            text=txt
        )
    except SlackApiError as e:
        assert e.response['error']


def post_slack_hyperlink(job_number: int, job: str, url: str):
    attachments_list = []
    attachments_dict = dict()
    attachments_dict['pretext'] = job_number
    for i in job_number:
        attachments_dict['title'] = job
        attachments_dict['title_link'] = url
        attachments_list.append()

def post_slack_attachments(attachments: list):
    slack.chat.post_message(channel=SlackConfig.CHANNEL, text=None, attachments=attachments, as_user=True)
    print('Posted Content!')

if __name__ == '__main__':
    attachments_dict = dict()
    attachments_dict['pretext'] = "attachments 블록 전에 나타나는 text"
    attachments_dict['title'] = "다른 텍스트 보다 크고 볼드되어서 보이는 title"
    attachments_dict['title_link'] = "https://corikachu.github.io"
    attachments_dict['fallback'] = "클라이언트에서 노티피케이션에 보이는 텍스트 입니다. attachment 블록에는 나타나지 않습니다"
    attachments_dict['text'] = "본문 텍스트! 5줄이 넘어가면 *show more*로 보이게 됩니다."
    attachments_dict['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
    attachments = [attachments_dict]

    slack.chat.post_message(channel="log", text=None, attachments=attachments, as_user=True)
    post_slack('hellow world')