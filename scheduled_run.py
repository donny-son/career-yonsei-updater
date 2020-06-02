from new_job_searcher import NewJobSearcher
from new_news_searcher import NewNewsSearcher
import schedule
from pickle_handler import PREVIOUS_NEWS_UPDATES, PREVIOUS_JOB_UPDATES
from slack_sender import post_slack
from datetime import datetime
import time
from browser import Browser

def scheduled_job():
    new_job_searcher = NewJobSearcher(window_mode=False, page='career', previous_pickle=PREVIOUS_JOB_UPDATES)
    new_job_searcher.main()
    Browser.browser.quit()

    new_news_searcher = NewNewsSearcher(window_mode=False, page='news', previous_pickle=PREVIOUS_NEWS_UPDATES)
    new_news_searcher.main()
    Browser.browser.quit()

# for test
schedule.every(5).seconds.do(scheduled_job)
# schedule.every().day.at('08:00').do(scheduled_job)
# schedule.every().day.at('13:00').do(scheduled_job)
# schedule.every().day.at('19:00').do(scheduled_job)
# schedule.every().day.at('23:59').do(scheduled_job)

if __name__ == '__main__':


    while True:
        try:
            runtime = datetime.now().strftime('%Y%M%D - %H:%M:%S')
            print(f'Program running...{runtime}' + "\r", end='')
            schedule.run_pending()
            time.sleep(1)

        except Exception as e:
            post_slack(channel='debug' , txt=e)
