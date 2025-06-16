from typing import List

MAX_MSG_LEN = 4096

def get_separator(length: int) -> str:
    """
        Generate a separator string consisting of '═' characters.

        Args:
            length (int): Total length of the separator including 2 characters reserved for edges.

        Returns:
            str: A string of '═' characters of length (length - 2).
    """
    return  '═' * (length - 2)

def split_messages(
                    items: List[str],
                    max_len: int = MAX_MSG_LEN,
                    separator_length: int = 26
                    ) -> List[str]:
    """
        Split a list of text items into multiple messages, each not exceeding max_len characters.
        Inserts a separator line between items (except before the first item).

        Args:
            items (List[str]): List of text items to split.
            max_len (int, optional): Maximum allowed length of each message. Defaults to MAX_MSG_LEN (4096).
            separator_length (int, optional): Length of the separator line. Defaults to 26.

        Returns:
            List[str]: List of message strings split according to max_len(The maximum line in the Telegram application), with separators.
    """
    separator = get_separator(length=separator_length) + "\n\n"
    messages: List[str] = []
    current_msg: str = ""

    for i, item in enumerate(items):
        if i > 0:
            item_with_sep = separator + item + "\n\n"
        else:
            item_with_sep = item + "\n\n"

        if len(current_msg) + len(item_with_sep) > max_len:
            messages.append(current_msg.strip())
            current_msg = item_with_sep
        else:
            current_msg += item_with_sep

    if current_msg:
        messages.append(current_msg.strip())

    return messages