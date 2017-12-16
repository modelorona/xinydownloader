# "main" file. gets the links and their data and sends to the db
import requests
import sys
from specific_file_downloader import get_contents
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
        full_link = gh + link
        file_contents = get_contents(full_link)
        print(file_contents)
        print(sys.getsizeof(file_contents))

        break

# print(markdown_links)
