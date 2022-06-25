from typing import *
import requests

"""
# later might implement regular expression
# re.findall would be a very useful application
DEFAULT_REGULAR_EXPRESSION = "" # TODO
"""

"""
# MAKE LIST of language symbols: https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
# TODO: instead of making list: pass language name and search for its code in html table
# TODO: make a method that allows to retrieve language symbol by passing language name: example "english" -> "en"

Might later implement this in case need to make it more automated:
    - user can just pass a language like: "english"/"English"/"Italian"/"italian"
    - then trough "from difflib import SequenceMatcher" from # Source for comparing similarity of strings: https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
        - the most similar matching language will be found from https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
        - that language will can be set as either the "sl_language" or "tl_language"
"""

# for now use delimiters: after using dev tools in browser it seems that the TRANSLATED text is between the LEFT and RIGHT delimeters
LEFT_DELIMITER = "<div class=\"result-container\">"
RIGHT_DELIMITER = "</div>"


SL_DETECT_LANGUAGE = "auto"

# this is the formatting string of link
LINK = "https://translate.google.com/m?sl={sl_language}&tl={tl_language}&hl={website_language}&q={enconded_text}"



def get_encoded_google_translation_text_url(text : str) -> str:
    assert '\n' not in text
    encoded_transation_text = text.replace(" ", "+") # all occurrences replaced
    return encoded_transation_text


def get_encoded_google_translation_link(text : str, tl_language : str, sl_language : str = SL_DETECT_LANGUAGE, website_language : str = "en") -> str:
    # add the encoded text
    enconded_text = get_encoded_google_translation_text_url(text)
    # substitute portions of string
    encoded_google_translation_link = LINK.format(sl_language = sl_language, tl_language = tl_language, website_language = website_language, enconded_text = enconded_text)
    return encoded_google_translation_link


def get_single_line_parsed_google_translation(text : str, tl_language : str, sl_language : str = SL_DETECT_LANGUAGE) -> Union[str,None]:
    assert '\n' not in text
    encoded_google_translation_link = get_encoded_google_translation_link(text, tl_language, sl_language)

    response = requests.get(encoded_google_translation_link)
    
    # return response string type text if successful
    if (response.status_code == 200):
        html_response =  response.text
        start = html_response.find(LEFT_DELIMITER)
        end = html_response.find(RIGHT_DELIMITER, start + 1) # the RIGHT_DELIMITER must be the first occurence after the found LEFT_DELIMITER
        start += len(LEFT_DELIMITER)
        translated_text = html_response[start:end]
        return translated_text
        
    return None

# "translate.google.com/m" works only for single lines!
def get_multi_line_parsed_google_translation(text : str, tl_language, sl_language : str = SL_DETECT_LANGUAGE) -> str:
    lines = text.split("\n")
    # handle errors in case unsuccessful translation of any line
    add = lambda translated_line : translated_line if translated_line != None else "Error!"
    translated_lines = [add(get_single_line_parsed_google_translation(line, tl_language, sl_language)) for line in lines]
    translated_text = "\n".join(translated_lines)
    return translated_text