from django.shortcuts import render
from .forms import PageUrlForm, PageTextForm
from .models import PracticeText, KeywordExtractor, Translator
import json
from ast import literal_eval


def index(request):
    """View function for home page of site."""

    keywords_translations = []
    practice_text = PracticeText()
    ref_texts = practice_text.get_practice_texts(20)
    doc_corpus = []
    for rt in ref_texts:
        doc_corpus.append("{0} {1}".format(rt.title, rt.body))
    kwe = KeywordExtractor()
    kwe.corpus_docs = doc_corpus
    translator = Translator()
    practice_text_id = None
    query_url = None
    flashcard_trigger = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        urlForm = PageUrlForm(request.POST)
        textForm = PageTextForm(request.POST)
        # check whether it's valid:
        if urlForm.is_valid():
            query_url = urlForm.cleaned_data['page_url']
            try:
                practice_text = PracticeText.objects.get(web_url=query_url)
            except:
                practice_text.set_from_url(urlForm.cleaned_data['page_url'])
            page_title = practice_text.title
            page_body = practice_text.body
            keywords_translations = translator.get_keyword_translations(kwe, page_title + ' ' + page_body)
            practice_text.vocab = json.dumps(keywords_translations)
            practice_text.save()
            practice_text_id = PracticeText.objects.only('id').get(web_url=query_url).id
            flashcard_trigger = 'true'

        elif textForm.is_valid():
            query_text = textForm.cleaned_data['page_text']
            practice_text.set_from_text(query_text)
            keywords_translations = translator.get_keyword_translations(kwe, practice_text.body)
            flashcard_trigger = 'true'

        else:
            page_title = 'Could not be found'

    else:
        urlForm = PageUrlForm()
        textForm = PageTextForm()

    return render(request, 'index.html', {
        'urlForm': urlForm,
        'textForm': textForm,
        'page_url': query_url,
        'keywords_translations': keywords_translations,
        'practice_text_id': practice_text_id,
        'flashcard_trigger': flashcard_trigger
    })


def flashcards(request):
    try:
        practice_text_id = request.GET["textid"]
        practice_text = PracticeText.objects.get(id=practice_text_id)
    except:
        return render(request, 'flashcards.html', {'error': 'no text found'})
    practice_text_list = literal_eval(practice_text.vocab)
    return render(request, 'flashcards.html', {'vocab': practice_text_list, 'vocab_len': len(practice_text_list)})
