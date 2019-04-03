from EtlChallengeModule.etl_module_exceptions import DifferentListLength


def text_to_number(str_number):
    """
    This function contains dicts used to convert word representation of numbers
    to the int equivalent.
    :param str_number: String representing a number
    :return: int number
    """
    number_words = {}
    if not number_words:
        til_nineteen = [
            "zero", "one", "two", "three", "four", "five", "six", "seven",
            "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
            "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        ten_muls = ["", "", "twenty", "thirty", "forty", "fifty", "sixty",
                    "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        number_words["and"] = (1, 0)
        for idx, word in enumerate(til_nineteen):
            number_words[word] = (1, idx)
        for idx, word in enumerate(ten_muls):
            number_words[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            number_words[word] = (10 ** (idx * 3 or 2), 0)

    current = 0
    result = 0
    for word in str_number.split():
        if word not in number_words:
            raise Exception("Illegal word: " + word)

        scale, increment = number_words[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def get_list_uniques(_list):
    """
    This function returns the unique/s value/s of a given list.
    :param _list: List
    :return: List containing unique values.
    """
    ret = []
    for it in _list:
        if it not in ret:
            ret.append(it)
    return ret


def get_index_of_equal(short_list, large_list):
    """
    This function returns the index from the first list when it finds an equal
    matching object in the second list.
    :param short_list: List
    :param large_list: List
    :return: Int
    """
    for it in short_list:
        for im in large_list:
            if it == im:
                return short_list.index(it)
    return None


def replace_in_list(main_list, replace_values, index):
    """
    This function replaces the object in a specified index from the main list.
    :param main_list: List
    :param replace_values: List
    :param index: Int
    :return: List with modified objects.
    """
    if len(main_list) == len(replace_values):
        for original, replace in zip(main_list, replace_values):
            original[index] = replace
        return main_list
    else:
        raise DifferentListLength


def text_cleaner(string):
    """
    This function eliminates \n characters from a string
    :param string: str
    :return: str
    """
    return string.replace('\n', '')


def find_na(na, ar):
    """
    This function search for NaNs in a list given a parameter to search for.
    :param na: SRE_Pattern
    :param ar: List
    :return: True if a NaN was found; False if no NaNs were found
    """
    for d in ar:
        if na.search(d):
            return True
    return False


def cents_to_eur(val):
    """
    This function divides a float value over 1000
    :param val: str
    :return: Float
    """
    return float(val) / 1000

