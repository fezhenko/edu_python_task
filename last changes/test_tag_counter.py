import unittest
from tag_counter import Tag_counter


class Test_tag_counter(unittest.TestCase):
    def test_counter(self):
        t = Tag_counter("http://fezhenko.pythonanywhere.com/")
        counted_dict = {'ul': 1, 'title': 1, 'strong': 1, 'p': 1, 'nav': 1, 'link': 1, 'li': 2, 'html': 1, 'header': 1,
                        'head': 1, 'h1': 2, 'div': 3, 'body': 1, 'a': 2}
        self.assertEqual(t.tags_to_dict(), counted_dict)

    def test_sitename(self):
        t = Tag_counter("http://fezhenko.pythonanywhere.com/")
        name = "Flask App"
        self.assertEqual(t.site_name(), name)

    def test_synonym(self):
        t = Tag_counter("yt")
        name = "YouTube"
        self.assertEqual(t.site_name(), name)

