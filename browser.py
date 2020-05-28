from selenium import webdriver

URL = "https://stat.yonsei.ac.kr/stat/board/job.do"


class Browser:
    '''Unsupported Version 오류 시 brew cask reinstall chromedriver(Mac)'''

    browser = None

    def __init__(self, window_mode = True):
        self.window_mode = window_mode
        self.url = URL
        Browser.browser = self.__set_browser()

    def __set_browser(self):
        if self.window_mode is False:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            browser = webdriver.Chrome(options=chrome_options)
        else:
            browser = webdriver.Chrome()
        browser.get(self.url)
        return browser

    def main(self):
        raise Exception('Please override the main function of the browser for proper use')




if __name__ == '__main__':

    browser = Browser()
    pass
