from django.db import models
import requests as req
from bs4 import BeautifulSoup
from googletrans import Translator as gtTrans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import math


class Translator():
    translator = gtTrans()

    def translate(self, text):
        try:
            res = self.translator.translate(text)
            return res.text
        except:
            return 'Could not get translation'

    def get_keyword_translations(self, keyword_extractor, input_text):
        keywords = keyword_extractor.get_keywords(input_text)
        keywords = [word for word in keywords if not word.isnumeric()]
        translations = [self.translate(word) for word in keywords]
        return list(zip(keywords, translations))


class KeywordExtractor(models.Model):
    stopwords = frozenset(set([]))
    corpus_docs = []
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)

    def set_corpus_docs(self, docs):
        self.corpus_docs = docs

    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(self, feature_names, sorted_items, topn=10):
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        # word index and corresponding tf-idf score
        for idx, score in sorted_items:
            # keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        # create a tuples of feature,score
        # results = zip(feature_vals,score_vals)
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results

    def get_keywords(self, doc_text):
        self.corpus_docs.append(doc_text)

        cv = CountVectorizer(max_df=0.85, stop_words=self.stopwords)
        word_count_vector = cv.fit_transform(self.corpus_docs)
        self.tfidf_transformer.fit(word_count_vector)
        feature_names = cv.get_feature_names()
        tf_idf_vector = self.tfidf_transformer.transform(cv.transform([doc_text]))
        sorted_items = self.sort_coo(tf_idf_vector.tocoo())
        word_num = math.floor(len(sorted_items) / 4)
        keywords = self.extract_topn_from_vector(feature_names, sorted_items, word_num)
        return keywords


class PracticeText(models.Model):
    web_url = models.CharField(max_length=1500)
    title = models.CharField(max_length=500)
    body = models.TextField()
    vocab = models.TextField(default='[]')

    def set_from_text(self, page_text):
        self.body = page_text

    def set_from_url(self, page_url):
        self.web_url = page_url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0'
        }
        page = req.get(page_url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        meta_title = soup.find('meta', {'property': 'og:title'})
        if meta_title:
            self.title = meta_title.get('content')

        page_body = None
        article_markups = [
            ['article'],
            ['div', {'class': 'article_body'}],
            ['div', {'class': 'end-body'}],
            ['div', {'id': '_article'}],
            ['div', {'class': 'v_article'}]
        ]

        while page_body is None:
            for item in article_markups:
                if len(item) == 1:
                    page_body = soup.find(item[0])
                    if page_body:
                        break
                elif len(item) == 2:
                    page_body = soup.find(item[0], item[1])
                    if page_body:
                        break
                else:
                    print('unrecognized argument format')

        if page_body:
            self.body = page_body.text

    def get_practice_texts(self, limit):
        retval = PracticeText.objects.all().filter()[:limit]
        return retval


class Locale(models.Model):
    lg = models.CharField(max_length=2)
    ct = models.CharField(max_length=2)
    lg_ct = models.CharField(max_length=4)


class FlashCard(models.Model):
    source = models.CharField(max_length=8)
    target = models.CharField(max_length=8)
    locale = models.ForeignKey(Locale, on_delete=models.CASCADE)
