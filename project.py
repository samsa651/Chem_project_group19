import chemparse
import math


def create_list_of_elements(lft_half, rgt_half):
    a = set()
    
    for i in lft_half:
        lft_keys = list(i.keys())
        for j in lft_keys:
            a.add(j)
    
    for i in rgt_half:
        rgt_keys = list(i.keys())
        for j in rgt_keys:
            a.add(j)

    return list(a)


def sum_two_lists(first_half, second_half):
    for i in range(len(second_half)):
        first_half.append(second_half[i])
    
    return first_half



def create_matrix_equation(lft_half_dt, rgt_half_dt, elements,eqtion):

    lft_half_len = len(lft_half_dt)
    rght_half_len = len(rgt_half_dt)

    m =[[0 for _ in range(lft_half_len+rght_half_len-1)] for _ in range(len(elements))]

    for i in range(len(elements)):
        for j in range(lft_half_len+rght_half_len-1):
            if elements[i] in eqtion[j]:
                if j < lft_half_len:
                    m[i][j] = eqtion[j][elements[i]]
                else:
                    m[i][j] = -1*eqtion[j][elements[i]]

    return m



def remove_spaces(sentence):
    return ''.join(sentence.split(' '))



s = 'Fe + O2 = Fe2O3'
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

matr = create_matrix_equation(left_half_numb, right_half_numb, list_of_elem, whole_eq)
print(whole_eq)
print(matr)
print(list_of_elem)
