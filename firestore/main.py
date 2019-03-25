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
    firebase_admin.initialize_app(cred, {
        'projectId': 'xinyu-9c4c9'
    })
    db = firestore.client()

    xy = xiny.XinY()
    gh = GithubHelper.GithubHelper()

    lang_ref = db.collection(u'languages')

    all_langs = gh.get_md_links()
    for index, lang in enumerate(all_langs.keys()):
        lang_html = xy.get_html(lang)
        save_language(lang_ref, index, lang, lang_html)

    # lang_ref.document(u'numberOfLang').set({
    #     u'numberOfLang': index
    # })
