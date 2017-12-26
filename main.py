#!/usr/bin/python3.6.3
import logging
from logging.handlers import RotatingFileHandler
from os import environ as env
from os.path import join, dirname
from sys import exit
from time import time

# from datetime import datetime as dt
from dotenv import load_dotenv

import FirebaseHelper as Firebase
import GithubHelper as Github
import MarkdownMagic as Markdown

app_log = logging.getLogger('root')


def update_all(gh, fb):
    links = gh.get_md_links()
    for lang, link in links.items():
        content = gh.get_md_content(links.get(lang))
        lang_data = Markdown.do_work(content)
        resp = fb.upd_db_lang(lang_data, lang)
        app_log.info(resp)

if __name__ == "__main__":
    # set up logging
    # logging.basicConfig(filename='p.log', level=logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    log_file = 'program.log'
    my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.DEBUG)
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(my_handler)


    # set up environmental variable control
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # initialize respective helpers
    firebase = Firebase.FirebaseHelper(env.get('firebase_link', None))
    github = Github.GithubHelper(env.get('github_link', None))

    # exit the program if there is no github link set and log it as well
    if github is None or firebase is None:
        print("Key is not set for some module")
        app_log.error(str(github) + str(firebase))
        exit(1)

    # todo: implement commit checking here to see new updates. for now, just do a wide update of all
    # commits = (github.get_commits_since(dt.utcfromtimestamp(1512156708)))

    # base program structure
    # script runs, updates all languages, updates the timestamp, and leaves
    # shouldn't crash but shit if it do well shit
    update_all(github, firebase)
    current_time = int(time()) # the epoch time, converted from floating point to int
    t_r_code = firebase.upd_db_timestamp(current_time)
    if t_r_code != 200:
        app_log.error('timestamp error: ' + str(t_r_code))

    # end of program


