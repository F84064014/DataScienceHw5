import re

from functools import reduce

'''
this is my polynomial object
    
    mode -> display mode with [^*] or without [*^]
    terms -> dictionary {element: coefficient} e.g. x+2xy2={x:1, x^2y:2}
'''
class POLY():

    '''
    input polynomial string (or dictionary), turn to dictionary and save in self.terms
    '''
    def __init__(self, str_poly: str = '', dict_poly: dict = None, mode: int = 0) -> None:
        
        self.mode = mode

        if dict_poly:
            self.terms = dict_poly
            return

        # standardized the polynomial and split into terms
        terms = str_poly[1:-1].replace('-', '+-').split('+')
        terms = [term.replace('*', '').replace('^', '') for term in terms]
        terms = [term.replace('-', '-1') if re.search(r"[-][^0-9]+", term) else term for term in terms]
        terms = ['1'+term if term[0].isalpha() else term for term in terms]

        # \A: match only at the start of the string
        re_coeff = re.compile(r"\A-?[-0-9]+")
        re_elem = re.compile(r"[^-0-9]+.*")

        coeffs = [int(re_coeff.search(term).group()) if re_coeff.search(term) else 1 for term in terms]
        elems = [re_elem.search(term).group() for term in terms]

        self.terms = dict(zip(elems, coeffs))

    '''
    static method, multiply two element
    output e1 * e2 = e3
    e.g. e1 = XY2Z3; e2 = X2YZ5; output = X3Y3Z8
    '''
    def elem_mul(e1: str, e2: str) -> str:

        # spilt each variable and it's power in the term e.g. 'X2Y5Z' => {X:2, Y:5, Z:1}
        re_elem_sep = re.compile(r"[A-Za-z][-0-9]*")
        _e1 = dict([(re.search(r"[A-Za-z]", _var).group(), int(re.search(r"[0-9]+", _var).group() if re.search(r"[0-9]+", _var) else 1)) for _var in re_elem_sep.findall(e1)])
        _e2 = dict([(re.search(r"[A-Za-z]", _var).group(), int(re.search(r"[0-9]+", _var).group() if re.search(r"[0-9]+", _var) else 1)) for _var in re_elem_sep.findall(e2)])

        _e3 = dict()

        # for each variable sum the power and save in new dictionary
        for key in list(set(list(_e1.keys()) + list(_e2.keys()))):
            
            _e3[key] = (_e1.get(key) if _e1.get(key) else 0) + (_e2.get(key) if _e2.get(key) else 0)

        res = ''

        # sort the variable to make sure that all terms will be in same order like XYZ
        for key, val in sorted(_e3.items(), key=lambda x: x[0]):
            res += key + ('' if val==1 else str(val))
            
        return res

    '''
    set display mode
    set print mode (1: print '*' and '^', 0: None of above)
    ''' 
    def set_mode(self, mode: int) -> None:
        
        self.mode = mode if mode==1 or mode==-1 else 1 

    '''
    representation
    (this is what interpreter see when you mention the POLY object)
    '''    
    def __repr__(self) -> str:
        
        terms = []
        for e, p in self.terms.items():
            res = ''
            
            # add '^' and '*'
            if self.mode == 0:
                for s in re.findall(r"[a-zA-Z][0-9]", e):
                    e = e.replace(s, s[0] + '^' + s[1])
                e = (('' if p==1 or p==-1 else '*') + e)

            res += (('' if p==1 else '-' if p==-1 else str(p)) + e)
            terms.append(res)

        return '+'.join(terms).replace('+-', '-')

    '''
    static method
    reduce if there is same element in defferent term
    e.g. 2XY + 2XZ + 3XY => 5XY + 2XZ
    '''
    def terms_reduction(terms: list) -> dict:

        _terms = dict()

        for e, p in terms:
            if _terms.get(e):
                _terms[e] += p
            else:
                _terms[e] = p

        return _terms

    '''
    static method
    multiply two POLY object and retrun result POLY object (use 'POLY' for forward declaration)
    '''
    def poly_mul(poly1: 'POLY', poly2: 'POLY') -> 'POLY':

        # multipy two polynomial object and sum the terms with same element
        terms = POLY.terms_reduction([(POLY.elem_mul(e1, e2), p1*p2) for e1, p1 in poly1.terms.items() for e2, p2 in poly2.terms.items()])
        return POLY(dict_poly=terms)



if __name__=='__main__':

    # input polynomial string
    _str = input('input the polynomial: ')

    # switch to selected mode
    mode = 0 if '^' in _str or '*' in _str else 1

    # split and get each polynomial inside parenthesis
    polys = []
    for str_poly in re.findall(r'\([^()]*\)', _str):
        polys.append(POLY(str_poly=str_poly))

    # use reduce() with poly_mul(poly1, poly2) to multiply each polynomial
    poly_res = reduce(POLY.poly_mul, polys)
    poly_res.set_mode(mode)
    print(poly_res)
    

    
# sample input
# (X+2*Y)(2*X^2-Y^2+Z)
# (2*X+3*Y+4*Z)(XY^2+X^2Y+Z^2)
# (A+2*B^2)(B+3*C^3)(2*A+B+C)

# (X+2Y)(2X2-Y2+Z)
# (2X+3Y+4Z)(XY2+X2Y+Z2)
# (A+2B2)(B+3C3)(2A+B+C)