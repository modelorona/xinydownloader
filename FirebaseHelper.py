from json import dumps, loads
from time import time

from requests import put, get


class FirebaseHelper:
    """
        Provides the user with some basic wrappers over the Google Firebase Rest API. It does not
        handle authentication (for now). They are not a perfect wrapper per se but are tailored
        for my use case.
    """

    def __init__(self, database):
        """
            Instantiates the FirebaseHelper object and gives it a current time stamp and sets
            the database link
            :param database
        """
        self.cur_timestamp = int(time())
        self.db_link = database

    def get_cur_timestamp(self):
        return self.cur_timestamp

    def get_db_link(self):
        return self.db_link

    def set_db_link(self, new_link):
        self.db_link = new_link

    def upd_db_timestamp(self, timestamp):
        """
            Updates the Firebase database timestamp entry with the parameter
            :param timestamp: the epoch time to send to the database
            :return: the http code
        """
        return put(self.db_link + '/last_edit_timestamp.json', dumps(timestamp)).status_code

    def get_db_timestamp(self):
        """
            Retrieves the last_edit_timestamp entry from the database
            :return: Datetime object representing the timestamp
        """
        return int(get(self.db_link + '/last_edit_timestamp.json').text)

    def get_lang_list(self):
        """
            Gets the languages from the database and returns it as a list
            :return: list of languages in order from database if request passed. Sorted in alphabetical order
            :return: status code of request if failed
        """
        data = get(self.db_link + '/languages.json?shallow=true')
        # if status code is 200 aka ok, return the data as a list sorted by alphabetical order
        if data.status_code == 200:
            language_list = sorted([key for key in loads(data.content)])
            return language_list
        # else return None
        return None

    def get_lang_text(self, language_name):
        """
            Gets the language text from the database that corresponds to the paramenter language_name
            :param language_name: the language that is required
            :return: the text that is mapped to the language_name parameter
            :return: None if language does not exist
        """
        data = get(self.db_link + '/languages/' + language_name + '.json')
        if data.status_code == 200:
            return data.content.strip()
        return None

    def upd_auth_info(self, author): # todo: think about doing this
        """
            Updates the single author's info aka their name and link and publications
            :param author:
            :return:
        """
        return self.db_link + author

    def upd_db_lang(self, language_dict, language_name):
        """
            Sends the n-amount of languages and their mapped text to the database
            :param language_dict: contains the n-mapped languages to respective language text
            :param language_name: name of the language
            :return: 200 to emulate http success else a dictionary containing failed language updates and their reason
        """
        failed = {}

        data = put(self.db_link + '/languages/' + language_name + '.json', dumps(language_dict))
        if data.status_code != 200:
            failed[language_name] = {
                "status_code": data.status_code,
                "content": data.content
            }
        return failed if len(failed) > 0 else 200
