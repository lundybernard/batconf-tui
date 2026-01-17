from unittest import TestCase

from ..tui import BatConfApp


class BatConfAppTests(TestCase):

    def test___init__(t):
        tui = BatConfApp()

        t.assertEqual(tui.title, "BatConfApp")

        # Check bound input keys
        keys = [binding.keys for binding in tui.BINDINGS]
        t.assertIn('q', keys)
