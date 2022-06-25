from typing import *

# from lib import requests
import requests
"""
# later might implement regular expression
# re.findall would be a very useful application
DEFAULT_REGULAR_EXPRESSION = "" # TODO
"""

# for now use delimiters: after using dev tools it seems that the TRANSLATED text is between the LEFT and RIGHT DELIMETER
START_LEFT_DELIMITER = "<span class=\"Q4iAWc\""
END_LEFT_DELIMITER = ">"
RIGHT_DELIMITER = "</span>"


SL_DETECT_LANGUAGE = "auto"
AMPERSAND_WITH_TEXT_FORMAT = "&text="

# this is the formatting string of link
LINK = "https://translate.google.com/?sl={sl_language}&tl={tl_language}{ampersand_with_enconded_text}&op=translate"



# MAKE LIST of language symbols: https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
# TODO: instead of making list: pass language name and search for its code in html table
# TODO: make a method that allows to retrieve language symbol by passing language name: example "english" -> "en"


def get_encoded_google_translation_text(text : str) -> str:
    encoded_transation_text = ""
    for c in text:
        if c == ' ':
            encoded_transation_text += "%20"
        elif c == '\n':
            encoded_transation_text += "%0A"
        else:
            encoded_transation_text += c
    return encoded_transation_text


def get_encoded_google_translation_link(text : str, tl_language : str, sl_language : str = SL_DETECT_LANGUAGE) -> str:
    ampersand_with_enconded_text = ""
    # add the encoded text
    if (text): # text must be non-empty
        encoded_translation_text = get_encoded_google_translation_text(text)
        ampersand_with_enconded_text += (AMPERSAND_WITH_TEXT_FORMAT + encoded_translation_text)
    # substitute portions of string
    encoded_google_translation_link = LINK.format(sl_language = sl_language, tl_language = tl_language, ampersand_with_enconded_text = ampersand_with_enconded_text)
    return encoded_google_translation_link


def get_parsed_google_translation(text : str, tl_language, sl_language : str = SL_DETECT_LANGUAGE) -> Union[str,None]:
    encoded_google_translation_link = get_encoded_google_translation_link(text, tl_language, sl_language)

    response = requests.get(encoded_google_translation_link)
    
    # return response string type text if successful
    if (response.status_code == 200):
        return response.text
    
    return None



# quick test
if (__name__ == "__main__"):
    print(get_encoded_google_translation_link("a b c\nde f",""))
    # unfortunately the translated text does not come up in the response
        # likely the response is triggered by scripts and thus we are unable to get any translated text
        # I think one idea is what if i could run those scripts and then get the new html code?
    print(get_parsed_google_translation("hello how are you","it","en").find(START_LEFT_DELIMITER))