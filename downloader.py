# "main" file. gets the links and their data and sends to the db
import requests
import sys
import html
import specific_file_downloader
import send_to_db
from bs4 import BeautifulSoup

link = "https://github.com/adambard/learnxinyminutes-docs"
gh = "https://github.com"
# raw_link = "https://raw.githubusercontent.com/adambard/learnxinyminutes-docs/master"
# /awk.html.markdown"

page = requests.get(link)
page = BeautifulSoup(page.text, "html.parser")

all_links = [link['href'] for link in page.find_all('a', href=True)]


for link in all_links:
    if str(link).endswith('.html.markdown'):
        language_name = html.unescape(str(link).split('/')[::-1][0].split('.')[0])
        full_link = gh + link
        file_contents = specific_file_downloader.get_contents(full_link)
        send_to_db.send_to_db('languages/'+language_name, file_contents)
        # break

# print(markdown_links)
