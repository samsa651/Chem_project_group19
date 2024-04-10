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


def create_matrix_equation(lft_half, rgt_half):
    pass



def remove_spaces(sentence):
    return ''.join(sentence.split(' '))



s = 'O2 + Fe = Fe2O3'
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


print(list_of_elem)
