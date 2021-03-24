from lark import Lark,Transformer

def parse_eq(equation):
    eq_parser = Lark("""
    
    
    
    ?sum: product 
    | sum "+" product -> add
    | sum "-" product -> sub

    ?product : atom
    | product "*" atom -> mul

    
    ?atom : set_id -> set
    | "-" atom -> neg
    | "(" sum ")" -> bracket

    set_id : NAME
    
    %import common.ESCAPED_STRING
    %import common.CNAME -> NAME
    %import common.WS_INLINE

    %ignore WS_INLINE

    """,start = 'sum')

    eq_transformer = Transformer
    return equation_parser.parse(equation)

class EqTransformer(Transformer):
    def __init__(self,user_id,session_id):
        self.user_id = user_id
        self.session_id = session_id

    def sum(self,first, second):
    
        diff = length(first)-length(second)
        
        if diff > 0:
            for i in range(diff)
                second[length(second)+i] = 0
        elif diff < 0: 
            for i in range(diff)
                first[length(first)+i] = 0

        sum_set = []
        
        # what do we do with q values?
        for i in range(length(first)):
            sum_set[i] = first[i][0]+second[i][0] 

        return sum_set
        

    def sub(self,first,second):
    
        diff = length(first)-length(second)
        
        if diff > 0:
            for i in range(diff)
                second[length(second)+i] = 0
        elif diff < 0: 
            for i in range(diff)
                first[length(first)+i] = 0

        diff_set = []
        
        # what do we do with q values?
        for i in range(length(first)):
            diff_set[i] = first[i][0]+second[i][0] 

        return diff_set

    def mul(self,first,second):
        diff = length(first)-length(second)
        
        if diff > 0:
            for i in range(diff)
                second[length(second)+i] = 1
        elif diff < 0: 
            for i in range(diff)
                first[length(first)+i] = 1

        product_set = []
        
        # what do we do with q values?
        for i in range(length(first)):
            product_set[i] = first[i][0]*second[i][0] 

        return product_set

    def set_id(self,id):
        # get set and make list
        ints = models.Integer.objects.filter(user_id = self.user_id, session_id=self.session_id,set_id=id)

        set_list = []

        for i in ints:
            set_list[i.index] = (i.X,i.q))
        return set_list
