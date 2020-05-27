from browser import Browser
from bs4 import BeautifulSoup
from slack_sender import post_slack
import time


def clean_title(text:str):
    return ''.join(text.split())

def get_all_values(nested_dictionary):
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            get_all_values(value)
        else:
            post_slack(f'{key}: {value}')

class NewContentSearcher(Browser):

    def main(self):
        self.updated_contents = {}
        self.__soup_page_source()
        self.__push_contents()
        self.browser.refresh()
        time.sleep(3)
        # Browser.browser.quit()


    def __soup_page_source(self):
        self.soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        self.new_contents = self.soup.findAll('div', {'class': "c-board-new-icon board-notice-new-icon"})
        new_content_index = 1
        for new_content in self.new_contents:
            new_content_tr = new_content.find_parent('tr')
            new_content_a = new_content_tr.find('a', href=True)
            cleaned_title = clean_title(new_content_a.text)
            new_content_url = self.url + new_content_a['href']
            self.updated_contents[f'{new_content_index}'] = {}
            self.updated_contents[f'{new_content_index}']['title'] = cleaned_title
            self.updated_contents[f'{new_content_index}']['url'] = new_content_url
            new_content_index += 1

    def __push_contents(self):
        number_of_new_contents = len(self.updated_contents)
        post_slack(f'***{number_of_new_contents}개의 새로운 취업정보가 있습니다!***')
        get_all_values(self.updated_contents)




if __name__ == '__main__':
    NewContentSearcher().main()
