import subprocess

from bs4 import BeautifulSoup
from requests import get


class XinY:
    def __init__(self):
        self.original_link = "https://learnxinyminutes.com/docs"
        self.css_original_link = "https://raw.githubusercontent.com/adambard/learnxinyminutes-site/master/source/css"
        self.css = self.get_css()  # generate the css as soon as object is created so we can use it over and over

    def get_html(self, language):
        # set up the return value object
        html_to_return = list()
        html_to_return.append('<!DOCTYPE html>')
        html_to_return.append('<html lang="en">')
        html_to_return.append('<head>')
        # request the html and pass it to bs4
        data = get(self.original_link + '/' + language).content
        soup = BeautifulSoup(data, "html.parser")
        # add in the meta tags
        for meta in soup.find_all('meta'):
            html_to_return.append(str(meta))
        # add in the css styles
        html_to_return.append(self.css)
        # close out the head tag
        html_to_return.append('</head>')
        # add in start of body tag
        html_to_return.append('<body>')
        # get the main content
        doc_div = soup.find("div", {'id': 'doc'})
        # and add it
        html_to_return.append('<!-- htmlmin:ignore -->')
        html_to_return.append(str(doc_div))
        html_to_return.append('<!-- htmlmin:ignore -->')
        # html_to_return.append(str(soup.get_text()))
        # close out body tag
        html_to_return.append('</body>')
        # close out html tag
        html_to_return.append('</html>')

        # now write it to a local file
        with open('temp.html', 'w') as temp:
            temp.write(" ".join(html_to_return).strip())

        # now call nodejs script to minify that file
        result = subprocess.run(['node', 'minify.js'], stdout=subprocess.PIPE)

        # and now return it as one big ass string
        return result.stdout.decode('utf8').strip()

    def get_css(self):
        css_to_return = list()
        # get all css here. order is important since that's how it goes in the html file
        css_names = ['normalize.css', 'main.css', 'screen.css', 'github.css']
        # screen.css is not actually in the github repo so we get it from the xiny site
        for sheet in css_names:
            if sheet == 'screen.css':
                file = get('https://learnxinyminutes.com/css/screen.css').text
            else:
                file = get(self.css_original_link + '/' + sheet).text
            content = '<style>{}</style>'.format(str(file).strip())
            css_to_return.append(content)
            css_to_return.append('\n')

        return " ".join(css_to_return).strip()