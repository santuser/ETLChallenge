import re
from os.path import exists
from EtlChallengeModule.etl_module_utils import (text_cleaner, find_na,
                                                 get_list_uniques,
                                                 get_index_of_equal,
                                                 replace_in_list,
                                                 text_to_number, cents_to_eur)
from abc import ABC, abstractmethod


def direct_transformation(func):
    """
    This function is used as a decorator on methods which simply need to
    iterate over a data array
    :param func: a method object
    :return: a function method
    """
    def wrapper_function(obj, cols_to_transform):
        for col in cols_to_transform:
            index = obj.headers.index(col)
            for row in obj.data:
                func(obj, row, index)
    return wrapper_function


class DataForm(ABC):
    """
    This is an abstract class which represents any form of data and contains
    different methods and attributes destined to manipulate it.
    The objective of this class is to provide all necessary to manipulate
    data regardless of its source.
    """
    def __init__(self, na_form):
        """
        Init method of Dataform class.

        na_form is used to determine how the NaN should be find within the
        data.
        :param na_form: string
        """
        self.na_form = DataForm.build_na_regex(na_form)
        self.data = None
        self.headers = None

    @staticmethod
    def build_na_regex(na_form):
        regex = "\s*" + na_form + "\s*"
        na_reg = re.compile(regex)
        return na_reg

    def load(self, headers_row=None):
        """
        This class method loads the headers and rows data in the instance
        attributes.
        :param headers_row: either None when the data does not contain the
        headers or int type when the headers are located in one specific row.
        """
        self.headers = self.get_headers(headers_row)
        self.data = self.get_data(headers_row)

    @abstractmethod
    def get_headers(self, headers_row=None):
        """
        Abstract method, shall be implemented by child class. Method used to
        get the headers (when existing) from the data.
        :param headers_row: either None when the data does not contain the
        headers or int type when the headers are located in one specific row.
        :return: List type containing all headers or None.
        """
        return

    @abstractmethod
    def get_data(self, headers_row=None):
        """
        Abstract method, shall be implemented by child class. Method used to
        get the rows from the data.
        :param headers_row: None when the data does not contain the
        headers or int type when the headers are located in one specific row.
        :return: Matrix of Lists containing all rows.
        """
        return

    def get_data_matrix(self):
        """
        This method return a row-wise matrix with the data and headers
        stored in the instance
        :return: Matrix of Lists [[]]
        """
        res = [self.headers]
        res.extend(self.data)
        return res

    @direct_transformation
    def data_to_float(self, row, index):
        """
        This method converts the data in a specified field (row[index]) to
        the float type when possible.
        :param row: List
        :param index: Int
        """
        try:
            if ',' in row[index]:
                row[index] = float(row[index].replace(',', '.'))
        except ValueError as e:
            return e

    def slice_data(self, desired_cols):
        """
        This method slices the data in the instance. The new data will depend
        on the columns selected.
        :param desired_cols: List. A List of the desired columns which data
        must remain in the instance.
        """
        res = []
        for row in self.data:
            values = []
            for col in desired_cols:
                values.append(row[self.headers.index(col)])
            res.append(values)
        self.headers = desired_cols
        self.data = res

    def drop_na(self):
        """
        This method drops all NaN containing rows from our instance data.
        """
        self.data = [row for row in self.data if not find_na(self.na_form,
                                                             row)]

    def get_unique_values(self, cols_to_get_unique):
        """
        This method returns all the unique values in the desired data columns
        :param cols_to_get_unique: List. List of columns from which the
        unique values must be extracted.
        :return: Zip object containing the list of cols to get unique values
        and a list for the unique values obtained.
        """
        res = []
        for col in cols_to_get_unique:
            index = self.headers.index(col)
            res.append(get_list_uniques(
                [val[index] for val in self.data]))
        return zip(cols_to_get_unique, res)

    def data_to_one_hot_encoding(self, cols_to_transform):
        """
        This method converts the desired columns to one hot encoding sequence.
        :param cols_to_transform: List. List of columns to convert to one hot
        encoding sequence
        """
        enc_dict = {}
        for col, uniques in self.get_unique_values(cols_to_transform):
            enc_dict[col] = []
            for row in self.data:
                enc_list = [0 for i in range(0, len(uniques))]
                enc_list[get_index_of_equal(uniques, row)] = 1
                enc_dict[col].append(enc_list)
        for key in enc_dict:
            replace_in_list(self.data, enc_dict[key], self.headers.index(key))

    def data_to_bool(self, cols_to_transform, relevant_values):
        for col, relevant_value in zip(cols_to_transform, relevant_values):
            index = self.headers.index(col)
            for row in self.data:
                row[index] = (1 if row[index].lower() == relevant_value.lower()
                              else 0)

    @direct_transformation
    def str_col_to_number(self, row, index):
        """
        This method converts the data in a field (row[index]) from the word
        representation of a number (eg: "Three") to it's int form (3)
        :param row: List
        :param index: Int
        """
        row[index] = text_to_number(row[index])

    @direct_transformation
    def price_to_eur(self, row, index):
        """
        This method converts a field (row[index]) containing a price in cents
        to EUR currency.
        :param row: List
        :param index: Int
        """
        row[index] = cents_to_eur(row[index])


class TxtData(DataForm):
    """
    This class represents a form of data which source is a txt file.
    It inherits from DataForm and implements its abstract methods such as
    get_headers and get_data.
    """
    def __init__(self, path, na_form, encoding='utf-8', separator=';'):
        """
        Init method of the TxtData class.
        :param path: String. Path to the txt file where data is stored.
        :param na_form: See super class definition
        :param encoding: Encoding which shall be used to parse data in txt file
        :param separator: Character which indicates the separation between
        fields or columns.
        """
        super().__init__(na_form)
        self.path = path
        self.separator = separator
        self.encoding = encoding

    def open_txt(self):
        """
        This method opens a txt file, reads all its lines and returns a matrix
        with its data.
        :return: Matrix. List of lists containing the lines in the txt file.
        """
        if exists(self.path):
            txt_file = None
            try:
                with open(self.path, 'r', encoding=self.encoding) as txt_file:
                    stream = txt_file.readlines()
                    return stream
            except Exception as e:
                return e
            finally:
                if txt_file is not None:
                    txt_file.close()
        else:
            raise FileNotFoundError

    def get_headers(self, headers_row=None):
        """
        TxtData implementation of the get_headers method. This method search
        for headers (when possible) in a List matrix.
        :param headers_row: See super class definition.
        :return: Returns a List with all the headers.
        """
        if headers_row is not None:
            for i, line in enumerate(self.open_txt()):
                if i == headers_row:
                    return [text_cleaner(col) for col in
                            line.split(self.separator)]
        else:
            return None

    def get_data(self, headers_row=None):
        """
        TxtData implementation of the get_data method. This method returns the
        data from a matrix of Lists read from a txt file.
        :param headers_row: See super class definition.
        :return: a matrix containing all the data rows.
        """
        data = []
        for line in self.open_txt():
            clean_line = [text_cleaner(l) for l in line.split(self.separator)]
            data.append(clean_line)
        if headers_row is not None:
            return data[:headers_row] + data[headers_row + 1:]
        else:
            return data
