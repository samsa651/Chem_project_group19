import chemparse
import math


def adjusted_of_matrix(matrix_sample_aj):
    res = [[0 for _ in range(len(matrix_sample_aj))] for _ in range(len(matrix_sample_aj))]
    for i in range(len(matrix_sample_aj)):
        for j in range(len(matrix_sample_aj)):
            res[i][j] = matrix_sample_aj[j][i]
    
    return res


def multiplication_matrix_on_coefficent(matrix_mult, coeff):
    for i in range(len(matrix_mult)):
        if type(matrix_mult[i]) is list:
            for j in range(len(matrix_mult)):
                matrix_mult[i][j] = coeff * matrix_mult[i][j]
        else:
            matrix_mult[i] = coeff * matrix_mult[i]
    
    return matrix_mult  


def multiply_matrix_on_vector(matrx_mlt, vector):
    for i in range(len(vector)):
        for j in range(len(vector)):
            matrx_mlt[j][i] = matrx_mlt[j][i]*vector[i]
    return matrx_mlt


def sum_up_matrix_rows(matr_sum):
    res =[0]*(len(matr_sum))
    for i in range(len(matr_sum)):
        row_sum = 0
        for j in range(len(matr_sum)):
            row_sum += matr_sum[i][j]
        res[i] = row_sum
    return res


def full_multiplication_matrix_on_vector(matrx_mlt, vector):
    return sum_up_matrix_rows(multiply_matrix_on_vector(matrx_mlt, vector))


def matrix_determinant_sep(matrix_plot, num_of_colum, num_of_row):
    res=[]
    
    for i in range(len(matrix_plot)):
        part_res =[]
        for j in range(len(matrix_plot)):
            if i != num_of_row and j != num_of_colum:
                part_res.append(matrix_plot[i][j])
        if i != num_of_row:
            res.append(part_res)
    return res



def separate_matrix(non_sep_matrix):
    right_sep_matrix = []
    left_sep_matrix = []

    for matr_i in non_sep_matrix:
        right_sep_matrix.append(matr_i.pop(-1))
        left_sep_matrix.append(matr_i)
    return left_sep_matrix , right_sep_matrix



def determinant_of_matrix(matrix_sample):
    res = 0
    if len(matrix_sample) > 1:
        for i in range(len(matrix_sample)):
            res += matrix_sample[0][i]*(1-(2*(i%2)))*determinant_of_matrix(matrix_determinant_sep(matrix_sample,i, 0))
    else:
        res = matrix_sample[0][0]
    
    return int(res)


def matrix_minor_finder(matrix_smpl):
    matr_res =[]

    for i in range(len(matrix_smpl)):
        part_matr_res =[]
        for j in range(len(matrix_smpl)):
            part_matr_res.append(determinant_of_matrix(matrix_determinant_sep(matrix_smpl,j,i))*(1-(2*((i+(j%2))%2))))
        matr_res.append(part_matr_res)
    return matr_res


def create_list_of_elements(lft_half, rgt_half):
    a = []
    
    for i in lft_half:
        lft_keys = list(i.keys())
        for j in lft_keys:
            if not(j in a):
                a.append(j)
    
    for i in rgt_half:
        rgt_keys = list(i.keys())
        for j in rgt_keys:
            if not(j in a):
                a.append(j)
    return a


def sum_two_lists(first_half, second_half):
    res = []
    for i in range(len(first_half)):
        res.append(first_half[i])
    for i in range(len(second_half)):
        res.append(second_half[i])
    
    return res



def create_matrix_equation(lft_half_dt, rgt_half_dt, elements,eqtion):

    lft_half_len = len(lft_half_dt)
    rght_half_len = len(rgt_half_dt)

    whole_len = len(eqtion)
    print(whole_len)
    m =[[0 for _ in range(whole_len)] for _ in range(len(elements))]
    for i in range(len(elements)):
        for j in range(whole_len):
            if elements[i] in eqtion[j]:
                if j < lft_half_len or j == whole_len-1:
                    m[i][j] = eqtion[j][elements[i]]
                else:
                    m[i][j] = -1*eqtion[j][elements[i]]

    return m



def remove_spaces(sentence):
    return ''.join(sentence.split(' '))


def find_iverted_matrix(matrix_inv):
    return multiplication_matrix_on_coefficent(adjusted_of_matrix(matrix_minor_finder(matrix_inv)), 1/(determinant_of_matrix(matrix_inv)))




s = 'Fe2SiO4 + Mg2SiO4 + H2O + CO2 = Mg6Si4O18H8 + Fe2O3 + CH4'
s = remove_spaces(s)
left_half_eq, right_half_eq = s.split('=')
left_half_chem = left_half_eq.split('+')
right_half_chem = right_half_eq.split('+')

left_half_numb =[]
right_half_numb =[]

for i in left_half_chem:
    left_half_numb.append(chemparse.parse_formula(i))

for i in right_half_chem:
    right_half_numb.append(chemparse.parse_formula(i))

print(left_half_numb, right_half_numb)

list_of_elem = create_list_of_elements(left_half_numb, right_half_numb)


whole_eq = sum_two_lists(left_half_numb, right_half_numb)
"""
matrix_test = [[1, 2, -4], [-3, 5, 3], [2, 1, 1]]
vector_test = [2, 1, 3]
print(matrix_minor_finder(matrix_test))
print(determinant_of_matrix(matrix_test), adjusted_of_matrix(matrix_minor_finder(matrix_test)))
print(find_iverted_matrix(matrix_test))
print(full_multiplication_matrix_on_vector(matrix_test, vector_test))

"""


matr = create_matrix_equation(left_half_numb, right_half_numb, list_of_elem, whole_eq)
print(whole_eq)
print(matr)
print(list_of_elem)
listed_matrix = separate_matrix(matr)
print(listed_matrix)
part_matr = full_multiplication_matrix_on_vector(find_iverted_matrix(listed_matrix[0]),listed_matrix[1])
print(part_matr, determinant_of_matrix(listed_matrix[0]))
det = determinant_of_matrix(listed_matrix[0])
res= multiplication_matrix_on_coefficent(part_matr, det)
if determinant_of_matrix(listed_matrix[0]) < 0:
    res= multiplication_matrix_on_coefficent(res, -1)
    det = det * -1

print(*res, float(det))