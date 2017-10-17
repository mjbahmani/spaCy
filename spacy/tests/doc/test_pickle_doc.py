from __future__ import unicode_literals

from ...language import Language
from ...compat import pickle, unicode_


def test_pickle_single_doc():
    nlp = Language()
    doc = nlp(u'pickle roundtrip')
    data = pickle.dumps(doc, 1)
    doc2 = pickle.loads(data)
    assert doc2.text == 'pickle roundtrip'


def test_list_of_docs_pickles_efficiently():
    nlp = Language()
    for i in range(10000):
        _ = nlp.vocab[unicode_(i)]
    one_pickled = pickle.dumps(nlp(u'0'), -1)
    docs = list(nlp.pipe(unicode_(i) for i in range(100)))
    many_pickled = pickle.dumps(docs, -1)
    assert len(many_pickled) < (len(one_pickled) * 2)
    many_unpickled = pickle.loads(many_pickled)
    assert many_unpickled[0].text == '0'
    assert many_unpickled[-1].text == '99'
    assert len(many_unpickled) == 100


def test_user_data_from_disk():
    nlp = Language()
    doc = nlp(u'Hello')
    doc.user_data[(0, 1)] = False
    b = doc.to_bytes()
    doc2 = doc.__class__(doc.vocab).from_bytes(b)
    assert doc2.user_data[(0, 1)] == False

def test_user_data_unpickles():
    nlp = Language()
    doc = nlp(u'Hello')
    doc.user_data[(0, 1)] = False
    b = pickle.dumps(doc)
    doc2 = pickle.loads(b)
    assert doc2.user_data[(0, 1)] == False