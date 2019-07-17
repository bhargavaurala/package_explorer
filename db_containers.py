class_to_str = {
    int: 'int',
    float: 'float',
    bool: 'bool',
    str: 'str',
    dict: 'dict',
    list: 'list',
    tuple: 'tuple',
    iter: 'iter',
    callable: 'callable'
}

class Input(object):
    def __init__(self, 
        name,
        docstring, 
        param_type, 
        expected_shape=None,
        options=None,
        is_optional=False,
        default_value=None):
        self.name = name
        self.docstring = docstring
        self.param_type = param_type
        self.expected_shape = expected_shape
        self.is_optional = is_optional
        self.default_value = default_value
    
    def __str__(self):        
        attrs = vars(self)    
        return '\n'.join("%s: %s" % item for item in attrs.items())

    def to_serialized_dict(self):
        serialized_dict = {}
        for var, val in vars(self).items():
            serialized_dict[var] = class_to_str[val] if val in class_to_str else val
        return serialized_dict

class Output(object):
    def __init__(self, 
        name,       
        docstring, 
        param_type,
        returned=True):
        self.name = name
        self.docstring = docstring
        self.param_type = param_type
        self.returned = returned

    def __str__(self):        
        attrs = vars(self)    
        return '\n'.join("%s: %s" % item for item in attrs.items())

    def to_serialized_dict(self):
        serialized_dict = {}
        for var, val in vars(self).items():
            serialized_dict[var] = class_to_str[val] if val in class_to_str else val
        return serialized_dict

class NodeFunction(object):
    def __init__(self,
        name,
        docstring,      
        inputs,
        outputs):
        self.name = name
        self.docstring = docstring
        self.inputs = inputs
        self.outputs = outputs

    def __str__(self):        
        fn_str = '\n'.join(['name: {}\ndocstring: {}'.format(self.name, self.docstring)])
        fn_str += '\nInputs:\n'
        fn_str += '\n'.join(str(input_) for input_ in self.inputs)
        fn_str += '\nOutputs:\n'
        fn_str += '\n'.join(str(output_) for output_ in self.outputs)
        return fn_str

    def to_serialized_dict(self):
        serialized_dict = {}
        for var, val in vars(self).items():
            if isinstance(val, list):
                serialized_dict[var] = [v.to_serialized_dict() for v in val]
            else:
                serialized_dict[var] = str(val)
        return serialized_dict


class Node(object):
    def __init__(self,
        name,
        docstring,
        inputs,
        outputs,
        node_functions,
        nodes):
        self.name = name
        self.docstring = docstring
        self.inputs = inputs
        self.outputs = outputs
        self.node_functions = node_functions
        self.nodes = nodes

    def __str__(self):        
        cls_str = '\n'.join(['name: {}\ndocstring: {}'.format(self.name, self.docstring)])
        cls_str += '\nInputs:\n'
        cls_str += '\n'.join(str(input_) for input_ in self.inputs)
        cls_str += '\nOutputs:\n'
        cls_str += '\n'.join(str(output_) for output_ in self.outputs)
        cls_str += '\nFunctions:\n'
        cls_str += '\n'.join(str(fn) for fn in self.node_functions)
        cls_str += '\nClasses:\n'
        cls_str += '\n'.join(str(cls) for cls in self.nodes)
        return cls_str

    def to_serialized_dict(self):
        serialized_dict = {}
        for var, val in vars(self).items():
            if isinstance(val, list):
                serialized_dict[var] = [v.to_serialized_dict() for v in val]
            else:
                serialized_dict[var] = str(val)
        return serialized_dict