import unittest
import json

import sys

try:
    filename = sys.argv[1]
    with open('tmp/%s' % filename, 'r') as f:
        pass
except FileNotFoundError:
    print('[X] file not exist. tmp/filename')
    sys.exit(0)
except IndexError:
    print('[X] please enter filename.')
    sys.exit(0)

class ResultTestCase(unittest.TestCase):
    def setUp(self):
        with open('tmp/%s' % filename, 'r') as f:
            self.data = json.loads( f.read() )

    def tearDown(self):
        pass

    def test_url(self):
        e = []
        for row in self.data:
            if not row['url']:
                e.append( (row) )

        self.assertEqual(len(e), 0, e)

    def test_title(self):
        e = []
        for row in self.data:
            if not row['title']:
                e.append( (row['url'], row['title']) )

        self.assertEqual(len(e), 0, e)

    def test_publish_date(self):
        e = []
        for row in self.data:
            if not row['publish_date']:
                e.append( (row['url'], row['publish_date']) )

        self.assertEqual(len(e), 0, e)

    def test_authors(self):
        e = []
        for row in self.data:
            if not row['authors']:
                e.append( (row['url'], row['authors']) )

        self.assertEqual(len(e), 0, e)

    def test_tags(self):
        e = []
        for row in self.data:
            if not row['tags']:
                e.append( (row['url'], row['tags']) )

        self.assertEqual(len(e), 0, e)

    def test_text(self):
        e = []
        for row in self.data:
            if not row['text']:
                e.append( (row['url'], row['text']) )

        self.assertEqual(len(e), 0, e)

    def test_text_html(self):
        e = []
        for row in self.data:
            if not row['text_html']:
                e.append( (row['url'], row['text_html']) )

        self.assertEqual(len(e), 0, e)

    def test_images(self):
        e = []
        for row in self.data:
            if not row['images']:
                e.append( (row['url'], row['images']) )

        self.assertEqual(len(e), 0, e)

    def test_video(self):
        e = []
        for row in self.data:
            if not row['video']:
                e.append( (row['url'], row['video']) )

        self.assertEqual(len(e), 0, e)

    def test_links(self):
        e = []
        for row in self.data:
            if len(row['links']) == 0:
                e.append( (row['url'], row['links']) )

        self.assertEqual(len(e), 0, e)

if __name__ == '__main__':
    unittest.main(argv = [sys.argv[0]])

