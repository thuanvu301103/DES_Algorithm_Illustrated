from help_function import * 
from initial_data import *


K_bin = bin(int(K_hex, 16))[2:].zfill(len(K_hex) * 4)  # Change K from hex to binary
print('K (hex) = ', K_hex, '\nK (bin) = ', K_bin)
M_bin = bin(int(M_hex, 16))[2:].zfill(len(M_hex) * 4)  # Change M from hex to binary
print('M (hex) = ', M_hex, '\nM (bin) = ', M_bin)

## Step 1: Create 16 subkeys, each of which is 48-bits long.
print ("----- Step 1: Create 16 subkeys, each of which is 48-bits long.")
print ('PC_1 table: \n', PC_1)
PC_1_array = PC_table_to_array(PC_1)

### Generate permuted key K+
K_plus = applyPermutation(PC_1_array, K_bin)
print ('Generate permuted key: K+ = ', K_plus)

### split this key into left and right halves, C0 and D0, where each half has 28 bits.
C = []
D = []
C += [K_plus[:28]]
D += [K_plus[28:]]
print ('Split K+ into left and right halves: \n   C_0 = ', C[0], '\n   D_0 = ', D[0])

### Create sixteen blocks Cn and Dn with !<=n<=16
print ('Left shifts array', left_shifts)
print ('Create sixteen blocks Cn and Dn with !<=n<=16: ')
for i in range(16):
    C += [left_shift_string(C[i], left_shifts[i])]
    D += [left_shift_string(D[i], left_shifts[i])]
    print (f'  C_{i+1} = {C[i+1]}\n  D_{i+1} = {D[i+1]}\n C_{i+1}D_{i+1} = {C[i+1]}{D[i+1]}\n -----')

### Form keys K_n
print ('PC_2 table: \n', PC_2)
PC_2_array = PC_table_to_array(PC_2)
### Generate permuted key Kn
K = [K_bin]
for i in range(16):
    CD_block = C[i+1] + D[i+1]
    K += [applyPermutation (PC_2_array, CD_block)]
    print (f'Generate permuted key: K_{i+1} = ', K[i+1])

## Step 2: Encode each 64-bit block of data.
print ("----- Step 2: Encode each 64-bit block of data.")
print ('IP table: \n', IP_table)
IP_array = PC_table_to_array(IP_table)

### Generate permuted key IP from M
IP = applyPermutation(IP_array, M_bin)
print ('Generate permuted key from M: IP = ', IP)

### Divide the permuted block IP into a left half L0 of 32 bits, and a right half R0 of 32 bits
L = []
R = []
L += [IP[:32]]
R += [IP[32:]]
print ('Split IP into left and right halves: \n   L_0 = ', L[0], '\n   R_0 = ', R[0])

### E-bit selection table
print ('E-bit selection table: \n', E_bit_selection_table)
E_bit_selection_array = PC_table_to_array(E_bit_selection_table)

### S-boxes
print ('S-boxes:')
S_box = []
for i in range(len(S)):
    S_box += [S_box_to_matrix(S[i])]
for i in range(len(S_box)):
    print (f'   S{i+1} table: \n', S_box[i])

### P permutation
print ('P permatutation table: \n', P)
P_array = PC_table_to_array(P)

for i in range(16):
    n = i+1
    print(f'----- Round {n}: -----')
    ### Calculate E[R_(n-1)] from R_(n-1)
    E = applyPermutation(E_bit_selection_array, R[n-1])
    print(f'Calculate: E[R{n-1}] = {E}')
    ### Calculate A = Kn (+) E[R_(n-1)]
    A = xor_binary_strings(K[n], E)
    print(f'Calculate: A = K{n} (+) E[R{n-1}] = {A}')
    ### Calculate S-box output
    A_split_array = [A[i:i+6] for i in range(0, len(A), 6)]    # Split A into equal 6-bít block
    S_output = ''
    for i in range(len(A_split_array)):
        S_output += S_box_transform(S_box[i], A_split_array[i])
    print ('S-box tranform output: ', S_output)
    ### Generate permuted P from S_output
    P_output = applyPermutation(P_array, S_output)
    print ('Generate permuted P from S_output: P = ', P_output)
    ### Calculate Rn = L_(n-1) (+) R_(n-1)
    R += [xor_binary_strings(L[n-1], P_output)]
    print(f'Calculate: R{n} = L{n-1} (+) P(B) = {R[n]}')
    ### Calculate Ln = R_(n-1)
    L += [R[n-1]]
    print(f'Calculate: L{n} = R{n-1} = {L[n]}')

### Reverse R16L16
R_16_L_16 = R[16] + L[16]
print ('=============================\nReverse R16L16 = ', R_16_L_16)
### apply the final permutation
print ('Reverse IP = ', reverse_IP)
reverse_IP_array = PC_table_to_array(reverse_IP)
print ('Apply final permutation: final cipertext C = ', applyPermutation(reverse_IP_array, R_16_L_16))