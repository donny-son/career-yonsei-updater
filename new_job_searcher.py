from browser import Browser
from bs4 import BeautifulSoup
from slack_sender import post_slack, post_slack_attachments, emojify
import time
from pickle_handler import save_obj, PREVIOUS_JOB_UPDATES
import copy
from config import SlackConfig


def clean_title(text:str):
    return ''.join(text.split())

def get_all_values(updated_dict: dict):
    for key, value in updated_dict.items():
        if type(value) is dict:
            get_all_values(value)
        else:
            post_slack(channel=SlackConfig.CHANNEL['career'], txt=f'{key}\n{value}')

class NewJobSearcher(Browser):

    def __init__(self, previous_pickle, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_updates = previous_pickle

    def main(self):
        self.updated_contents = {}
        self._soup_page_source()
        if self._check_any_updates():
            post_slack_attachments(channel=SlackConfig.CHANNEL['career'], attachments=self.assign_slack_attachments())
        else:
            post_slack(channel=SlackConfig.CHANNEL['career'], txt=f':scream: 아직 새로 올라온 취업 공고가 없네용....{emojify("disappointed")}')


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
        save_obj(self.updated_contents, 'CURRENT_JOB_UPDATES')

    def assign_slack_attachments(self):
        number_of_new_contents = len(self.updated_contents)
        attachments_list = []
        attachments_dict = {}
        attachments_dict['pretext'] = f':laughing: {number_of_new_contents}개의 새로운 취업정보가 있습니다!{emojify("clap") * number_of_new_contents}'
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
            save_obj(self.updated_contents, 'PREVIOUS_JOB_UPDATES')
            return False
        else:
            # TODO:: when there is 1 or more overlapping case
            if len(self.updated_contents) == 0:
                return False
            shared_items = {k: self.updated_contents[k] for k in self.updated_contents if k in self.previous_updates and self.updated_contents[k] == self.previous_updates[k]}
            for key in shared_items.keys():
                del self.updated_contents[key]
            save_obj(self.updated_contents_copy, 'PREVIOUS_JOB_UPDATES')
            return True



if __name__ == '__main__':
    NewJobSearcher(window_mode=True, page='career', previous_pickle=PREVIOUS_JOB_UPDATES).main()
