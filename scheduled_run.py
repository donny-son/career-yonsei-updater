from new_content_searcher import NewContentSearcher
import schedule
from slack_sender import post_slack
from datetime import datetime
import time

def scheduled_job():
    new_content_searcher = NewContentSearcher(window_mode=False)
    new_content_searcher.main()

# for test
# schedule.every(8).seconds.do(scheduled_job)
schedule.every().day.at('08:00').do(scheduled_job)
schedule.every().day.at('13:00').do(scheduled_job)
schedule.every().day.at('19:00').do(scheduled_job)
schedule.every().day.at('23:59').do(scheduled_job)

if __name__ == '__main__':


    while True:
        try:
            runtime = datetime.now().strftime('%Y%M%D - %H:%M:%S')
            print(f'Program running...{runtime}' + "\r", end='')
            schedule.run_pending()
            time.sleep(1)

        except Exception as e:
            post_slack(e)
