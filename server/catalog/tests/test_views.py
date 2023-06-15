from django.contrib.postgres.search import SearchVector

from rest_framework.test import APIClient, APITestCase

from catalog.models import Wine
from catalog.serializers import WineSerializer


class ViewTests(APITestCase):
    fixtures = ['test_wines.json']

    def setUp(self):
        Wine.objects.all().update(search_vector=(
            SearchVector('variety', weight='A') +
            SearchVector('winery', weight='A') +
            SearchVector('description', weight='B')
        ))

        self.client = APIClient()

    def test_empty_query_returns_everything(self):
        response = self.client.get('/api/v1/catalog/wines/')
        wines = Wine.objects.all()
        self.assertEqual(response.data, WineSerializer(wines, many=True).data)

    def test_query_matches_variety(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'query': 'Cabernet',
        })
        self.assertEqual(1, len(response.data))
        self.assertEqual("58ba903f-85ff-45c2-9bac-6d0732544841", response.data[0]['id'])

    def test_query_matches_winery(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'query': 'Barnard',
        })
        self.assertEqual(1,len(response.data))
        self.assertEqual("21e40285-cec8-417c-9a26-4f6748b7fa3a", response.data[0]['id'])

    def test_query_matches_description(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'query': 'wine',
        })
        self.assertEqual(3, len(response.data))
        self.assertCountEqual([
            "58ba903f-85ff-45c2-9bac-6d0732544841",
            "21e40285-cec8-417c-9a26-4f6748b7fa3a",
            "000bbdff-30fc-4897-81c1-7947e11e6d1a",
        ], [item['id'] for item in response.data])

    def test_can_filter_on_country(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'country': 'Germany',
        })
        self.assertEquals(1, len(response.data))
        self.assertEquals("136658ba-d39d-47d0-b5d6-a847f670fbec", response.data[0]['id'])

    def test_can_filter_on_points(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'points': 87,
        })
        self.assertEquals(1, len(response.data))
        self.assertEquals("21e40285-cec8-417c-9a26-4f6748b7fa3a", response.data[0]['id'])

    def test_country_must_be_exact_match(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'country': 'Deutschland',
        })
        self.assertEquals(0, len(response.data))
        self.assertJSONEqual(response.content, [])

    def test_search_can_be_paginated(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'limit': 1,
            'offset': 1,
        })
        # Count is equal to total number of results in database
        # We're loading 3 wines into the database via fixtures
        self.assertEqual(4, response.data['count'])
        self.assertEqual(1, len(response.data['results']))
        self.assertIsNotNone(response.data['previous'])
        self.assertIsNotNone(response.data['next'])

    def test_search_results_returned_in_correct_order(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'query': 'Champagne',
        })
        self.assertEqual(2, len(response.data))
        self.assertListEqual([
            "000bbdff-30fc-4897-81c1-7947e11e6d1a",
            "136658ba-d39d-47d0-b5d6-a847f670fbec",
        ], [item['id'] for item in response.data])

    def test_search_vector_populated_on_save(self):
        wine = Wine.objects.create(
            country='US',
            points=80,
            price=1.99,
            variety='Pinot Grigio',
            winery='Charles Shaw'
        )
        wine = Wine.objects.get(id=wine.id)
        self.assertEqual("'charl':3A 'grigio':2A 'pinot':1A 'shaw':4A", wine.search_vector)

    def test_description_highlights_matched_words(self):
        response = self.client.get('/api/v1/catalog/wines/', {
            'query': 'wine',
        })
        self.assertEquals('A creamy <mark>wine</mark> with full Chardonnay flavors.', response.data[0]['description'])
