from html import unescape

from bs4 import BeautifulSoup
from requests import get


class GithubHelper:
    def __init__(self):
        self.link = 'https://github.com/adambard/learnxinyminutes-docs'
        self.gh = 'https://github.com'

    def get_md_links(self):
        """
            Method gets all of the markdown links that are present on the web page and returns them
            as a nice list
            :return: dict of language name mapped to link if successful else None if failure
        """
        md_links = {}
        data = get(self.link)
        data_soup = BeautifulSoup(data.text, "html.parser")
        all_links = [link['href'] for link in data_soup.find_all('a', href=True)]
        # now that we have all the links, time to find the markdown ones
        for link in [l for l in all_links if str(l).endswith('.html.markdown')]:
            language_name = unescape(str(link).split('/')[::-1][0].split('.')[0]).replace('%2B', '+')
            md_links[language_name] = link
        return md_links if len(md_links) > 0 else None

    def html_to_uni(self, text):
        return
