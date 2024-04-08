import chemparse
import math


def remove_spaces(sentence):
    return ''.join(sentence.split(' '))



s = 'Fe + O2 = Fe2O3'
s = remove_spaces(s)
left_half_eq , right_half_eq = s.split('=')
left_half_chem = left_half_eq.split('+')
right_half_chem = right_half_eq.split('+')

left_half_numb =[]
right_half_numb =[]
for n in left_half_chem:
    left_half_numb.append(chemparse.parse_formula(n))
for n in right_half_chem:
    right_half_numb.append(chemparse.parse_formula(n))

print('hello world')

print(left_half_numb,right_half_numb)
