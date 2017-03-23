import numpy as np

def take_subarray(array, selection):
    # test the dimensions
    arr_shape = array.shape
    if len(selection) != len(arr_shape):
        print "Array and selection dimensions do not fit."
        return -1

    selection_tuple = []
    for dim in range(len(selection)):
        if len(selection[dim]) == 1:
            if selection[dim][0] < 0 or selection[dim][0] >= arr_shape[dim]:
                print "Dimension " + str(dim) + " of the selection is out of bounds."
                return -1
            selection_tuple.append(slice(selection[dim][0],selection[dim][0]+1))
        else:
            if selection[dim][0] < 0 or selection[dim][0] >= arr_shape[dim]:
                print "Element 1 of dimension " + str(dim) + " of the selection is out of bounds."
                return -1
            if selection[dim][1] < 0 or selection[dim][1] >= arr_shape[dim]:
                print "Element 1 of dimension " + str(dim) + " of the selection is out of bounds."
                return -1
            if selection[dim][0] >= selection[dim][1]:
                print "Element 1 is >= element 2 of dimension " + str(dim) + "."
                return -1

            if len(selection[dim]) == 2:
                selection_tuple.append(slice(selection[dim][0], selection[dim][1]+1))
            elif len(selection[dim]) == 3:
                selection_tuple.append(slice(selection[dim][0], selection[dim][1]+1, selection[dim][2]))


    selection_tuple = tuple(selection_tuple)
    return array[selection_tuple]

def n_transpose(array, order):
    arr_shape = array.shape
    if len(order) != len(arr_shape):
        print "Array and selection dimensions do not fit."
        return -1

    return array.transpose(tuple(order))
