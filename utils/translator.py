from typing import Union, List

from deep_translator import GoogleTranslator

def translate_text(texts: Union[str, List[str]], target_lang: str) -> Union[str, List[str]]:
    """
    Translate a text string or a list of text strings into the target language,
    automatically detecting the source language.

    Args:
        texts (Union[str, List[str]]): Text or list of texts to translate.
        target_lang (str): Target language code, e.g. 'en', 'ru', 'fr'.

    Returns:
        Union[str, List[str]]: Translated text or list of translated texts.

    Raises:
        ValueError: If `texts` is neither a string nor a list of strings.
    """
    translator = GoogleTranslator(source='auto', target=target_lang)

    if isinstance(texts, str):
        return translator.translate(texts)
    elif isinstance(texts, list):
        return translator.translate_batch(texts)
    else:
        raise ValueError("texts: must be a string or a list of strings.")