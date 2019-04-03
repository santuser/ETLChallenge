class DifferentListLength(Exception):
    def __init__(self):
        super(DifferentListLength, self).__init__('Error: Lists have'
                                                  ' different length')
