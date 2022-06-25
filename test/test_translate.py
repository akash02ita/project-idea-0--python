import unittest


from src.translate import *
from difflib import SequenceMatcher

# Source for comparing similarity of strings: https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
MIN_SIMILARITY_STRINGS_RATIO = 0.7
def string_similarity_ratio(a : str, b : str) -> float:
    return SequenceMatcher(None, a, b).ratio()

class Test(unittest.TestCase):

    def test_encoded_url(self):
        self.assertRaises(AssertionError, get_encoded_google_translation_text_url, "\n")
        self.assertRaises(AssertionError, get_encoded_google_translation_text_url, "must\nfails")

        self.assertEqual(get_encoded_google_translation_text_url(""),"")
        self.assertEqual(get_encoded_google_translation_text_url("hello"),"hello")
        self.assertEqual(get_encoded_google_translation_text_url("hello how"),"hello+how")
        self.assertEqual(get_encoded_google_translation_text_url("hello how are you"),"hello+how+are+you")


    def test_encoded_link(self):
        with self.assertRaises(AssertionError):
            get_encoded_google_translation_link(text = "\n", tl_language = "")
        with self.assertRaises(AssertionError):
            get_encoded_google_translation_link(text = "must\nfail", tl_language = "any")

        self.assertEqual(
            get_encoded_google_translation_link("hello", "en"),
            "https://translate.google.com/m?sl=auto&tl=en&hl=en&q=hello")

        self.assertEqual(
            get_encoded_google_translation_link("hello how", "it", "en"),
            "https://translate.google.com/m?sl=en&tl=it&hl=en&q=hello+how")

        self.assertEqual(
            get_encoded_google_translation_link("hello how are you", "de", "en", "es"),
            "https://translate.google.com/m?sl=en&tl=de&hl=es&q=hello+how+are+you")


    def test_single_line(self):
        with self.assertRaises(AssertionError):
            get_single_line_parsed_google_translation("\n", "")
        with self.assertRaises(AssertionError):
            get_single_line_parsed_google_translation("must\nfail", "en")
        
        # Note: translation are subject to small variations
        # Source for comparing similarity of strings: https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
        self.assertGreaterEqual(
            string_similarity_ratio(get_single_line_parsed_google_translation("how are you", "it"), "come stai"),
            MIN_SIMILARITY_STRINGS_RATIO)
        self.assertGreaterEqual(
            string_similarity_ratio(get_single_line_parsed_google_translation("hello", "it"), "ciao"),
            MIN_SIMILARITY_STRINGS_RATIO)
        self.assertGreaterEqual(
            string_similarity_ratio(get_single_line_parsed_google_translation("hello, how are you", "de"), "hallo, wie geht's"),
            MIN_SIMILARITY_STRINGS_RATIO)

        
    def test_multi_line(self):
        self.assertGreaterEqual(
            string_similarity_ratio(get_multi_line_parsed_google_translation("Hello this is a multi-line test\ni hope this works","it","en"),"Ciao, questo è un test multilinea\nspero che questo funzioni"),
            MIN_SIMILARITY_STRINGS_RATIO)
        
        self.assertGreaterEqual(
            string_similarity_ratio(get_multi_line_parsed_google_translation("how are you\nwhere are you", "it"), "come stai\ndove sei"),
            MIN_SIMILARITY_STRINGS_RATIO)

        self.assertGreaterEqual(
            string_similarity_ratio(get_multi_line_parsed_google_translation("hello\nthis is a test\nthis is another test", "it"), "ciao\nquesto è uno test\nquesto è un'altro test"),
            MIN_SIMILARITY_STRINGS_RATIO)

        self.assertGreaterEqual(
            string_similarity_ratio(get_multi_line_parsed_google_translation("Hola, mi nombre es computer.\nEstoy haciendo una prueba", "it", "es"), "Ciao, mi chiamo computer.\nSto facendo una prova"),
            MIN_SIMILARITY_STRINGS_RATIO)



