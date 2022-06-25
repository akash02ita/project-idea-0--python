from typing import *

# from lib import requests
import requests
"""
# later might implement regular expression
# re.findall would be a very useful application
DEFAULT_REGULAR_EXPRESSION = "" # TODO
"""

# for now use delimiters: after using dev tools it seems that the TRANSLATED text is between the LEFT and RIGHT DELIMETER
LEFT_DELIMITER = "<div class=\"result-container\">"
RIGHT_DELIMITER = "</div>"


SL_DETECT_LANGUAGE = "auto"

# this is the formatting string of link
# LINK = "https://translate.google.com/?sl={sl_language}&tl={tl_language}{ampersand_with_enconded_text}&op=translate"
"""
New Source used: https://stackoverflow.com/questions/9404628/python-script-to-translate-via-google-translate
Following source: https://github.com/mouuff/mtranslate
    specifically: https://github.com/mouuff/mtranslate/blob/acf75a9809a4f21e95341c48f0c6538446098480/mtranslate/core.py at line 70

I noticed that instead of using "translate.google.com", "translate.google.com/m" HAS BEEN USED, which this time does not have any of those missing translation issues (probably the https response already contains the response where the previous time it was not returning it)
"""
LINK = "https://translate.google.com/m?sl={sl_language}&tl={tl_language}&hl={website_language}&q={enconded_text}"



# MAKE LIST of language symbols: https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
# TODO: instead of making list: pass language name and search for its code in html table
# TODO: make a method that allows to retrieve language symbol by passing language name: example "english" -> "en"


def get_encoded_google_translation_text(text : str) -> str:
    assert '\n' not in text
    encoded_transation_text = text.replace(" ", "+") # all occurrences replaced
    return encoded_transation_text


def get_encoded_google_translation_link(text : str, tl_language : str, sl_language : str = SL_DETECT_LANGUAGE, website_language : str = "en") -> str:
    # add the encoded text
    enconded_text = get_encoded_google_translation_text(text)
    # substitute portions of string
    encoded_google_translation_link = LINK.format(sl_language = sl_language, tl_language = tl_language, website_language = website_language, enconded_text = enconded_text)
    return encoded_google_translation_link


def get_parsed_google_translation(text : str, tl_language, sl_language : str = SL_DETECT_LANGUAGE) -> Union[str,None]:
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
def get_multi_line_parsed_google_translation(text : str, tl_language, sl_language : str = SL_DETECT_LANGUAGE):
    lines = text.split("\n")
    # handle errors in case unsuccessful translation of any line
    add = lambda translated_line : translated_line if translated_line != None else "Error!"
    translated_lines = [add(get_parsed_google_translation(line, tl_language, sl_language)) for line in lines]
    translated_text = "\n".join(translated_lines)
    return translated_text


# quick test
if (__name__ == "__main__"):
    # print(get_encoded_google_translation_link("a b c de f",""))
    # unfortunately the translated text does not come up in the response
        # likely the response is triggered by scripts and thus we are unable to get any translated text
        # I think one idea is what if i could run those scripts and then get the new html code?
    print(get_parsed_google_translation("Hello this is a single line test","it","en"))
    print("====")
    print(get_multi_line_parsed_google_translation("Hello this is a multi-line test\ni hope this works","it","en"))