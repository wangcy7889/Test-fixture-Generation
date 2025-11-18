import sys
import numpy as np
SEPARATOR = '->'

def get_serialized_binary_representation(self):
    if len(self.binary_vocabulary) == 0:
        self.create_binary_representation()
    string = ''
    if sys.version_info >= (3,):
        items = self.binary_vocabulary.items()
    else:
        items = self.binary_vocabulary.iteritems()
    for key, value in items:
        array_as_string = np.array2string(value, separator=',', max_line_width=self.size * self.size)
        string += '{}{}{}\n'.format(key, SEPARATOR, array_as_string[1:len(array_as_string) - 1])
    return string