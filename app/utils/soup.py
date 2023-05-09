from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from requests import get


def get_soup(url: str) -> BeautifulSoup:
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    header = {
        'Accept': '*/*',
        'User-Agent': random_user_agent,
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    is_captcha = True

    while (is_captcha):
        page = get(url, headers=header)
        assert page.status_code == 200
        soup = BeautifulSoup(page.content, 'html.parser')

        if 'captcha' in str(soup):
            print('bot detected')
        else:
            print('bot bypassed')

        return soup
