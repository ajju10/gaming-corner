from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.datetime_safe import datetime

from .models import BlogPost


class BlogPostTest(TestCase):

    def test_blog_post_page_uses_template(self):
        response = self.client.get('/blog')
        self.assertTrue(response.status_code, 200)


class BlogPostModelsTest(TestCase):

    def test_can_add_blogpost_model(self):

        first_post = BlogPost.objects.create(
            title='This is first test blog post.',
            body='This is first test body.',
            author=User.objects.create(username='Username', password='Password'),
            timestamp=datetime.now()
        )

        second_post = BlogPost.objects.create(
            title='This is second test blog post.',
            body='This is second test body.',
            author=User.objects.create(username='Username1', password='Password1'),
            timestamp=datetime.now()
        )

        posts = BlogPost.objects.count()
        self.assertEqual(posts, 2)

        self.assertEqual(first_post.body, 'This is first test body.')
        self.assertEqual(second_post.body, 'This is second test body.')