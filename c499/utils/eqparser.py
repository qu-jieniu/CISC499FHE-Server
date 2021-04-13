from lark import Lark,Transformer
from integers.models import Integer,IntegerSet,PersistentSession
from collections import OrderedDict

def parse_eq(equation):
    
    eq_parser = Lark("""
    
    ?start: sum

    ?sum: product 
    | sum "+" product -> add
    | sum "-" product -> sub

    ?product : atom
    | product "*" atom -> mul

    
    ?atom : ALPHA -> set_id
    | "-" atom -> neg
    | "(" sum ")" 
    
    ALPHA: /[a-zA-Z0-9_]+/

    %import common.ESCAPED_STRING
    %import common.CNAME -> NAME
    %import common.WS_INLINE

    %ignore WS_INLINE

    """,start = 'sum',parser='lalr',transformer=EqTransformer())
    
    return eq_parser.parse(equation)

class EqTransformer(Transformer):
    def __init__(self):
        self.vars = {}
        
    def add(self,set_list):
        # lark recursively descends tree
        first = set_list[0]
        second =set_list[1]
        diff = len(first)-len(second)

        if diff > 0:
            for i in range(diff):
                second[len(second)+i] = 0
        elif diff < 0: 
            for i in range(diff):
                first[len(first)+i] = 0

        sum_set = OrderedDict()
        
        # what do we do with q values?
        for i in range(len(first)):
            sum_set[str(i)] = first[i]+second[i] 

        return list(sum_set.values())
    
    def neg(self, atom):
        return [elem*-1 for elem in atom]

    def sub(self,set_list):
        first = set_list[0]
        second =set_list[1]
        diff = len(first)-len(second)

        if diff > 0:
            for i in range(diff):
                second[len(second)+i] = 0
        elif diff < 0: 
            for i in range(diff):
                first[len(first)+i] = 0

        diff_set = OrderedDict()
        
        # what do we do with q values?
        for i in range(len(first)):
            diff_set[str(i)] = first[i]-second[i] 

        return list(diff_set.values())

    def mul(self,set_list):
        first = set_list[0]
        second =set_list[1]
        diff = len(first)-len(second)

        if diff > 0:
            for i in range(diff):
                second[len(second)+i] = 0
        elif diff < 0: 
            for i in range(diff):
                first[len(first)+i] = 0

        prod_set = OrderedDict()
        
        # what do we do with q values?
        for i in range(len(first)):
            prod_set[str(i)] = first[i]*second[i] 

        return list(prod_set.values())

    def set_id(self,set_id):
        # remove list
        set_id = set_id[0]
        # get set and make list
        ints = Integer.objects.filter(set_id=set_id.value)

        set_list = OrderedDict()

        for i in ints:
            set_list[str(i.index)] = i.X

        return list(set_list.values())
