import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')

        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for_row_in_tournament_table(self, row_text):

        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_class_name('table')
                rows = table.find_element_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_browse_tournament_list(self):
        # Ajay has heard about a cool new online to-do app. He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title mentions Gaming Corner and the header says "Start playing, organizing and
        # participating in esports tournaments all in one place."
        self.assertIn('Gaming Corner', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Start playing', header_text)

        # The page has a navbar with a title of 'GamingCorner' and other buttons like Browse, Organize and a
        # SignIn button
        navbar = self.browser.find_element_by_tag_name('nav')
        gamingcorner_button = navbar.find_element_by_tag_name('a')
        self.assertEqual('GamingCorner', gamingcorner_button.text)
        signin_button = self.browser.find_element_by_id('signinButton')
        self.assertEqual('Sign In', signin_button.text)
