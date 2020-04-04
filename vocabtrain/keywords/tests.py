from django.test import TestCase
from keywords.models import PracticeText


class PracticeTextCase(TestCase):
    def setUp(self):
        PracticeText.objects.create(
            web_url="http://example.url.com",
            title="my example title",
            body="more example text",
            vocab='[("text", "Text"),("example","Beispiel")]'
        )

    def test_get_practice_texts(self):
        pt = PracticeText.get_practice_texts(self, 1)
        self.assertEqual(len(pt), 1)
        self.assertEqual(pt[0].title, "my example title")
        self.assertEqual(pt[0].web_url, "http://example.url.com")
        self.assertEqual(pt[0].vocab, '[("text", "Text"),("example","Beispiel")]')
        self.assertEqual(pt[0].body, "more example text")
