from django.test import TestCase

# Create your tests here.

class URLTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code,200)



        