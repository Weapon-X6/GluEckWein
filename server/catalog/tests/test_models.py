from django.test import TestCase

from catalog.models import Wine, WineSearchWord


class WineModelTests(TestCase):
    def test_str_method(self):
        obj = Wine.objects.create(country="us", points="39", variety="", winery="")

        self.assertEqual(obj.__str__(), str(obj.id))


class WineSearchWordTests(TestCase):
    def test_str_method(self):
        obj = WineSearchWord.objects.create(word="la chair")

        self.assertEqual(obj.__str__(), obj.word)
