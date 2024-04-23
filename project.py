
"""
This code is incomplete in terms of design (completely missing comments due to incompleteness), but in general it works.

In brief: To solve a problem, the code turns a chemical equation into a matrix 
where each line is a different chemical element and each column is how much substance is in the corresponding part of the equation
(here is a link to the source "https://digitalcommons.usf.edu/cgi/viewcontent.cgi?article=4910&context=ujmm"). 

After that you get a matrix and a vector (the vector consists of the rightmost element of the equation),
multiplying the inverse matrix by the vector you get a vector in which the coefficients are located from top to bottom. 

Actually most of the code is devoted to the creation of the inverse matrix. 

!!!! throughout this code, I will refer to a matrix as a two-dimensional list. !!!!

comments are written using " instead of a # because of the color palette in VS code where normal comments are gray text on a black background, and with " is blue.
"""


import chemparse
from math import gcd
from functools import reduce #This is a built-in python function used only to find the greatest common divisor.


"""
flips the matrix relative to the main diagonal.
"""
def adjusted_of_matrix(matrix_sample_aj):
    res = [[0 for _ in range(len(matrix_sample_aj))] for _ in range(len(matrix_sample_aj))]
    for i in range(len(matrix_sample_aj)):
        for j in range(len(matrix_sample_aj)):
            res[i][j] = matrix_sample_aj[j][i]
    
    return res


"""
multiplies each matrix element by some number
"""
def multiplication_matrix_on_coefficent(matrix_mult, coeff):
    for i in range(len(matrix_mult)):
        if type(matrix_mult[i]) is list:
            for j in range(len(matrix_mult)):
                matrix_mult[i][j] = coeff * matrix_mult[i][j]
        else:
            matrix_mult[i] = coeff * matrix_mult[i]
    
    return matrix_mult  


"""
multiplies a matrix by a vector according to the rules of matrix to matrix multiplication.
"""
def multiply_matrix_on_vector(matrx_mlt, vector):
    for i in range(len(vector)):
        for j in range(len(vector)):
            matrx_mlt[j][i] = matrx_mlt[j][i]*vector[i]
    return matrx_mlt


"""
summarizes all numbers in one row turning the matrix into a single column
"""
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



"""
When the upper left number in a 3 by 3 matrix (for example) is taken, 
it must be multiplied by the determinant of the 2 by 2 matrix in the lower right corner, 
this function returns the required 2 by 2 matrix.
"""
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


"""
separates the right row of the matrix , 
making the left part of matrix square and the right row becomes a vector
"""
def separate_matrix(non_sep_matrix):
    right_sep_matrix = []
    left_sep_matrix = []

    for matr_i in non_sep_matrix:
        right_sep_matrix.append(matr_i.pop(-1))
        left_sep_matrix.append(matr_i)
    return left_sep_matrix , right_sep_matrix


"""
recursive algorithm for finding the determinant of a matrix (the algorithm traverses only the top row)
"""
def determinant_of_matrix(matrix_sample):
    res = 0
    if len(matrix_sample) > 1:
        for i in range(len(matrix_sample)):
            res += matrix_sample[0][i]*(1-(2*(i%2)))*determinant_of_matrix(matrix_determinant_sep(matrix_sample,i, 0))
    else:
        res = matrix_sample[0][0]
    
    return int(res)



"""
Matrix minor finder 
"""
def matrix_minor_finder(matrix_smpl): 
    matr_res =[]

    for i in range(len(matrix_smpl)):
        part_matr_res =[]
        for j in range(len(matrix_smpl)):
            part_matr_res.append(determinant_of_matrix(matrix_determinant_sep(matrix_smpl,j,i))*(1-(2*((i+(j%2))%2))))
        matr_res.append(part_matr_res)
    return matr_res



"""
returns a list of chemical elements (H, O, Cl, etc.) that occur in the equation.
"""
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


"""
glues 2 lists together one after the other
"""
def sum_two_lists(first_half, second_half):
    res = []
    for i in range(len(first_half)):
        res.append(first_half[i])
    for i in range(len(second_half)):
        res.append(second_half[i])
    
    return res



"""
turns dictionaries with chemical elements that we got from chemparse into a matrix 
"""
def create_matrix_equation(lft_half_dt, rgt_half_dt, elements,eqtion): 

    lft_half_len = len(lft_half_dt)
    rght_half_len = len(rgt_half_dt)

    whole_len = len(eqtion)

    m =[[0 for _ in range(whole_len)] for _ in range(len(elements))]
    for i in range(len(elements)):
        for j in range(whole_len):
            if elements[i] in eqtion[j]:
                if j < lft_half_len or j == whole_len-1:
                    m[i][j] = eqtion[j][elements[i]]
                else:
                    m[i][j] = -1*eqtion[j][elements[i]]

    return m



def remove_spaces(sentence): #remove spaces in string
    return ''.join(sentence.split(' '))


"""
Just calls functions to find the inverse matrix 
in particular the multiplication of the minor matrix by 1/determinant matrix (i.e. made only for ease of use in code)
"""
def find_iverted_matrix(matrix_inv):
    return multiplication_matrix_on_coefficent(adjusted_of_matrix(matrix_minor_finder(matrix_inv)), 1/(determinant_of_matrix(matrix_inv)))


"""
finds the greatest common multiple and divides the whole array of coefficients by this number
"""
def simplify(listed_numbers):
    x = reduce(gcd , listed_numbers)
    for i in range(len(listed_numbers)):
        listed_numbers[i] = int(listed_numbers[i]/x)
    
    return listed_numbers







"""
This is the place to enter the chemical equation.
                ||
                ||
                \/

"""
s = 'Fe2SiO4 + Mg2SiO4 + H2O + CO2 = Mg6Si4O18H8 + Fe2O3 + CH4' # This is input line



"""
Following is the scary code for turning a string with an equation into a matrix, vector, and a list of chem elements.
"""
print(s)
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

#print(left_half_numb, right_half_numb)

list_of_elem = create_list_of_elements(left_half_numb, right_half_numb)


whole_eq = sum_two_lists(left_half_numb, right_half_numb)
"""
matrix_test = [[1, 2, -4], [-3, 5, 3], [2, 1, 1]]
vector_test = [2, 1, 3]
print(matrix_minor_finder(matrix_test))
print(determinant_of_matrix(matrix_test), adjusted_of_matrix(matrix_minor_finder(matrix_test)))
print(find_iverted_matrix(matrix_test))
print(full_multiplication_matrix_on_vector(matrix_test, vector_test))


just some tests 
"""


matr = create_matrix_equation(left_half_numb, right_half_numb, list_of_elem, whole_eq)
#print(whole_eq)
#print(matr)
#print(list_of_elem)
listed_matrix = separate_matrix(matr)
"""
    /\
    ||
on the zero element is a square matrix , on the first element is a vector
"""
#print(listed_matrix)
part_matr = full_multiplication_matrix_on_vector(find_iverted_matrix(listed_matrix[0]),listed_matrix[1])
#print(part_matr, determinant_of_matrix(listed_matrix[0]))
"""
the whole matrix is multiplied by the determinant to get rid of fractions, then multiplied by -1 if all elements in it are negative 
"""
det = determinant_of_matrix(listed_matrix[0])
res= multiplication_matrix_on_coefficent(part_matr, det)
if determinant_of_matrix(listed_matrix[0]) < 0:
    res= multiplication_matrix_on_coefficent(res, -1)
    det = det * -1
res.append(float(det))

for i in range(len(res)):
    res[i] = int(res[i])


"""
the resulting matrix with coefficients is simplified
"""
res = simplify(res)
print(*res)

"""
the answer is not in the most convenient form, 
each element of the answer from left to right is coefficients 
that must be substituted before each element of the equation from left to right.

Perhaps the code will not work for all equations, but in theory it should.
"""