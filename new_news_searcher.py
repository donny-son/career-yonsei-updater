from slack_sender import post_slack, post_slack_attachments, emojify
from pickle_handler import PREVIOUS_NEWS_UPDATES, save_obj
from new_job_searcher import NewJobSearcher, get_all_values, clean_title
import copy
from bs4 import BeautifulSoup
from config import SlackConfig

def get_all_values(updated_dict: dict):
    for key, value in updated_dict.items():
        if type(value) is dict:
            get_all_values(value)
        else:
            post_slack(channel=SlackConfig.CHANNEL['news'], txt=f'{key}\n{value}')

class NewNewsSearcher(NewJobSearcher):

    def main(self):
        self.updated_contents = {}
        self._soup_page_source()
        if self._check_any_updates():
            post_slack_attachments(channel=SlackConfig.CHANNEL['news'], attachments=self.assign_slack_attachments())
        else:
            post_slack(channel=SlackConfig.CHANNEL['news'], txt=f'새로 올라온 대학원 공지 사항이 없습니다.')

    def _soup_page_source(self):
        self.soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        self.new_contents = self.soup.findAll('div', {'class': "c-board-new-icon board-notice-new-icon"})
        new_content_index = 1
        for new_content in self.new_contents:
            new_content_tr = new_content.find_parent('tr')
            new_content_a = new_content_tr.find('a', href=True)
            cleaned_title = clean_title(new_content_a.text)
            new_content_url = self.url + new_content_a['href']
            self.updated_contents[f'{cleaned_title}'] = new_content_url
            new_content_index += 1
        self.updated_contents_copy = copy.deepcopy(self.updated_contents)
        save_obj(self.updated_contents, 'CURRENT_NEWS_UPDATES')

    def assign_slack_attachments(self):
        number_of_new_contents = len(self.updated_contents)
        attachments_list = []
        attachments_dict = {}
        attachments_dict['pretext'] = f'{emojify("exclamation")} {number_of_new_contents}개의 새로운 공지사항이 있습니다!'
        attachments_list.append(attachments_dict)
        for key, value in self.updated_contents.items():
            attachments_dict = {}
            if type(value) is dict:
                get_all_values(value)
            else:
                attachments_dict['title'] = key
                attachments_dict['title_link'] = value
                attachments_list.append(attachments_dict)
        return attachments_list

    def _check_any_updates(self) -> bool:
        if self.previous_updates == self.updated_contents:
            save_obj(self.updated_contents, 'PREVIOUS_NEWS_UPDATES')
            return False
        else:
            # TODO:: when there is 1 or more overlapping case
            shared_items = {k: self.updated_contents[k] for k in self.updated_contents if k in self.previous_updates and self.updated_contents[k] == self.previous_updates[k]}
            for key in shared_items.keys():
                del self.updated_contents[key]
            save_obj(self.updated_contents_copy, 'PREVIOUS_NEWS_UPDATES')
            return True



if __name__ == '__main__':
    NewNewsSearcher(window_mode=True, page='news', previous_pickle=PREVIOUS_NEWS_UPDATES).main()
