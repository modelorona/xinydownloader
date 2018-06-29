# purpose of this is to abstract some of the github requests stuff. decided not to use their api
# since it would take more time to set up (although it would be worth looking into later)
# from github import Github
from html import unescape
from json import loads

from bs4 import BeautifulSoup
from requests import get


class GithubHelper:
    def __init__(self, l):
        self.link = l
        self.gh = "https://github.com"

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
            language_name = unescape(str(link).split('/')[::-1][0].split('.')[0])
            md_links[language_name] = link
        return md_links if len(md_links) > 0 else None

    def get_md_content(self, link):
        """
            Using the parameter link, the method makes an http call and then gets the content of the response,
            which is the markdown content, stores it in a string, and returns it
            :param link: the link that the request is made to
            :return: the markdown content of the link in a giant string if success, else None if fail
        """
        data = get(self.gh + link).text
        data_soup = BeautifulSoup(data, "html.parser")
        all_links = [link['href'] for link in data_soup.find_all('a', href=True)]
        for link in all_links:
            if "raw" in link:
                return get(self.gh + link).text
        return None

    def get_commits_since(self, last_time):
        """
            Gets all commits from the xinyminutes repo from the last timestamp onwards
            :param last_time: the timestamp in iso 8061 format
            :return: the list of commits in dictionary form
        """
        return loads(get('https://api.github.com/repos/adambard/learnxinyminutes-docs/commits', params={
            "since": last_time
        }).content)

    def get_commit_changes(self, commit_sha): # todo: fix this shit when possible. important to update only some languages, not all
        """
            Sees which files were changed and creates a list of languages that should be updated
            :param commit_sha: the commit sha to look up
            :return: list of languages to update
        """
        langs_to_update = []
        data = get('https://api.github.com/repos/adambard/learnxinyminutes-docs/commits/' + str(commit_sha)).json()
        # now parse the data and see what was updated
        # https://developer.github.com/v3/repos/commits/#get-a-single-commit
        # files = data['files']

        # print(data)

        return data
