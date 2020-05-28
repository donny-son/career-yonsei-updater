from browser import Browser
from bs4 import BeautifulSoup
from slack_sender import post_slack
import time
from pickle_handler import save_obj, PREVIOUS_UPDATES
import copy


def clean_title(text:str):
    return ''.join(text.split())

def get_all_values(updated_dict: dict):
    for key, value in updated_dict.items():
        if type(value) is dict:
            get_all_values(value)
        else:
            post_slack(f'{key}\n{value}')

class NewContentSearcher(Browser):

    def main(self):
        self.updated_contents = {}
        self.__soup_page_source()
        if self.__check_any_updates():
            self.__push_contents()
        else:
            post_slack('아직 새로 올라온 취업 공고가 없네용.....ㅠㅠ')


    def __soup_page_source(self):
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
        save_obj(self.updated_contents, 'CURRENT_UPDATES')

    def __push_contents(self):
        number_of_new_contents = len(self.updated_contents)
        post_slack(f'***와!!! {number_of_new_contents}개의 새로운 취업정보가 있습니다!***')
        get_all_values(self.updated_contents)

    def __check_any_updates(self, PREVIOUS_UPDATE=PREVIOUS_UPDATES) -> bool:
        if PREVIOUS_UPDATE == self.updated_contents:
            save_obj(self.updated_contents, 'PREVIOUS_UPDATES')
            return False
        else:
            # TODO:: when there is 1 or more overlapping case
            shared_items = {k: self.updated_contents[k] for k in self.updated_contents if k in PREVIOUS_UPDATE and self.updated_contents[k] == PREVIOUS_UPDATE[k]}
            for key in shared_items.keys():
                del self.updated_contents[key]
            save_obj(self.updated_contents_copy, 'PREVIOUS_UPDATES')
            return True



if __name__ == '__main__':
    NewContentSearcher().main()
