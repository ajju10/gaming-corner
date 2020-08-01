from django.test import TestCase


class BlogPostTest(TestCase):

    def test_blog_post_page_uses_template(self):
        response = self.client.get('/blog')
        self.assertTrue(response.status_code, 200)
