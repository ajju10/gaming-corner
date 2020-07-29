from django.test import TestCase


class BlogPostTest(TestCase):

    def blog_post_page_resolves(self):
        response = self.client.get('/blog')
        self.assertTemplateUsed(response, 'blog.html')
