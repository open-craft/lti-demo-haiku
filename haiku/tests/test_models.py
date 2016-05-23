from django.test import TestCase

from haiku.models import Haiku


class HaikuTests(TestCase):
    """Haiku model tests."""

    def test_str(self):
        haiku = Haiku(poem='Empty poem')
        self.assertEquals(
            str(haiku),
            'Empty poem'
        )

    def test_grade_one(self):
        haiku = Haiku(poem='One line')
        self.assertEquals(
            haiku.get_grade(),
            1.0/3
        )

    def test_grade_two(self):
        haiku = Haiku(poem="One line\nTwo lines")
        self.assertEquals(
            haiku.get_grade(),
            2.0/3
        )

    def test_grade_three(self):
        haiku = Haiku(poem="One line\nTwo lines\nThree lines")
        self.assertEquals(
            haiku.get_grade(),
            3.0/3
        )

    def test_grade_four(self):
        haiku = Haiku(poem="One line\nTwo lines\nThree lines\nFour lines")
        self.assertEquals(
            haiku.get_grade(),
            0
        )

    def test_grade_strip(self):
        haiku = Haiku(poem="One line\n\n  \nTwo lines\nThree lines\n   \n   ")
        self.assertEquals(
            haiku.get_grade(),
            3.0/3
        )
