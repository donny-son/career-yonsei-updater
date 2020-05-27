from new_content_searcher import NewContentSearcher
import schedule
from slack_sender import post_slack
from datetime import datetime

schedule.every(10).seconds.do(NewContentSearcher(window_mode=False).main)

if __name__ == '__main__':

    while True:
        try:
            runtime = datetime.now().strftime('%Y%M%D - %H:%M:%S')
            print(f'Program running...{runtime}' + "\r", end='')
            schedule.run_pending()

        except Exception as e:
            post_slack(e)
