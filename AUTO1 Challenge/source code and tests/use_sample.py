"""
This is an example of how to achieve all the necessary transformations
present in the development requirements.
"""
import csv
from EtlChallengeModule.etl_module_data_manipulation import TxtData


result = TxtData('challengeme.txt', "-")
result.load(0)
result.slice_data(['engine-location',
                   'num-of-cylinders',
                   'engine-size',
                   'weight',
                   'horsepower',
                   'aspiration',
                   'price',
                   'make'])

result.drop_na()
result.data_to_one_hot_encoding(['engine-location'])
result.data_to_bool(['aspiration'], ['turbo'])
result.str_col_to_number(['num-of-cylinders'])
result.price_to_eur(['price'])
result.data_to_float(['horsepower'])

with open('output.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(result.get_data_matrix())
writeFile.close()
