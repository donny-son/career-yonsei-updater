from new_content_searcher import NewContentSearcher
import schedule

schedule.every(10).hours.do(NewContentSearcher().main)

if __name__ == '__main__':

    while True:
        schedule.run_pending()
