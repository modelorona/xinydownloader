import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from firestore import xiny, GithubHelper


def save_language(ref, pos, language, html):
    ref.document(str(pos)).set({
        u'language': language,
        u'html': html
    })



if __name__ == '__main__':
    cred = credentials.Certificate(u'firebase.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    index = 0

    xy = xiny.XinY()
    gh = GithubHelper.GithubHelper()

    lang_ref = db.collection(u'languages')

    all_langs = gh.get_md_links()
    for lang, link in all_langs.items():
        lang_html = xy.get_html(link)
        save_language(lang_ref, index, lang, lang_html)
        index += 1

    lang_ref.document(u'numberOfLang').set({
        u'numberOfLang': index
    })