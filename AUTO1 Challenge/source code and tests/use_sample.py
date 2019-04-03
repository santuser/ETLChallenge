"""
This is an example of how to achieve all the necessary transformations
present in the development requirements.
"""
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

"Print the final data rows."
for r in result.get_data_matrix():
    print(r)
