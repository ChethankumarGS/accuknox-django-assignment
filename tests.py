from django.test import SimpleTestCase

from .rectangle import Rectangle


class RectangleTest(SimpleTestCase):
    def test_iteration_yields_length_then_width(self):
        self.assertEqual(list(Rectangle(5, 3)), [{"length": 5}, {"width": 3}])

    def test_can_iterate_more_than_once(self):
        r = Rectangle(2, 4)
        self.assertEqual(list(r), list(r))
