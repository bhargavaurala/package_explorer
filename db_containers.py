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
        fn_str = '\n'.join(['name: {}\ndoc: {}'.format(self.name, self.docstring)])
        fn_str += '\nInputs:\n'
        fn_str += '\n'.join(str(input_) for input_ in self.inputs)
        fn_str += '\nOutputs:\n'
        fn_str += '\n'.join(str(output_) for output_ in self.outputs)
        return fn_str

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
        cls_str = '\n'.join(['name: {}\ndoc: {}'.format(self.name, self.docstring)])
        cls_str += '\nInputs:\n'
        cls_str += '\n'.join(str(input_) for input_ in self.inputs)
        cls_str += '\nOutputs:\n'
        cls_str += '\n'.join(str(output_) for output_ in self.outputs)
        cls_str += '\nFunctions:\n'
        cls_str += '\n'.join(str(fn) for fn in self.node_functions)
        cls_str += '\nClasses:\n'
        cls_str += '\n'.join(str(cls) for cls in self.nodes)
        return cls_str



