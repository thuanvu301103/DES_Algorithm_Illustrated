'''
    * Left shift a string
    * @Param
    ** input_string: str: string that needs to be leeft shifted
    ** shift: int: number of shift that needs take place
    * @Return
    ** shifted_string: str: ...
'''
def left_shift_string(input_string, shift):
    # Calculate the effective shift value (in case shift is greater than the length of the string)
    shift %= len(input_string)
    
    # Perform the left shift with adding
    shifted_string = input_string[shift:] + input_string[:shift]
    
    return shifted_string

'''
    * PC table string to array
    * @Param: 
    ** input_string: str: PC table string
    * @Return:
    ** PC_array: array(int): An array which each array item is a PC table cell from left to right, from top to bottom
'''
def PC_table_to_array (input_string):
    PC_rows = input_string.split('\n')
    PC_array = []
    for row in PC_rows:
        PC_array += [int(num) for num in row.split()]
    return PC_array

'''
    * S-box string to matrix
    * @Param: 
    ** input_string: str: S-box string
    * @Return:
    ** matrix: array(array(int)): ...
'''
def S_box_to_matrix (input_string):
    rows = input_string.split('\n')
    matrix = []
    for row in rows:
        lst = []
        for num in row.split():
            lst += [int(num)]
        matrix += [lst]
    return matrix


'''
    * Apply permutation
    * @Param:
    ** permutation_arr: array(int): array of peermutation table
    ** original_string: str: ...
    * @Return:
    ** permuted_string: str: ...
'''
def applyPermutation (permutation_arr, original_string):
    permuted_string = ''
    for num in permutation_arr:
        permuted_string += original_string[num-1]
    return permuted_string

'''
    * XOR two binary string
    * @Param:
    ** bin_str1: str: ...
    ** bin_str2: str: ...
    * @Return: ...: str: ...
'''
def xor_binary_strings(bin_str1, bin_str2):
    # Convert binary strings to integers
    int_val1 = int(bin_str1, 2)
    int_val2 = int(bin_str2, 2)
    
    # Perform XOR operation
    result = int_val1 ^ int_val2
    
    # Convert result back to binary string
    result_str = bin(result)[2:]
    
    return result_str.zfill(max(len(bin_str1), len(bin_str2)))  # Zero-fill to match the length of the longest input string

'''
    * Give 6-bit binary string, using S-box and return 4-bit string
    * @Param:
    * @Return:
'''
def S_box_transform (S_box_matrix, input_string):
    row = int('' + input_string[0] + input_string[-1], 2)
    col = int(input_string[1:5], 2)
    return format(S_box_matrix[row][col], '04b')