from django.test import TestCase
from django.urls import reverse

class IndexViewQueryTest(TestCase):
    def test_index_view_db_queries(self):
        with self.assertNumQueries(1):
            response = self.client.get(reverse('index'))
            self.assertEqual(response.status_code, 200)
