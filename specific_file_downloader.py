# gets the markdown text and returns it
import requests
from bs4 import BeautifulSoup


def get_contents(location):
    page = requests.get(location).text
    soup = BeautifulSoup(page, "html.parser")
    links_in_page = [link['href'] for link in soup.find_all('a', href=True)] # get all the links
    # now need the raw link, which has raw in the address
    for link in links_in_page:
        if "raw" in link:
            return requests.get("https://github.com" + link).text

