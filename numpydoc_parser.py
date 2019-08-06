from numpydoc.docscrape import FunctionDoc, ClassDoc
from db_containers import Input, Output

from sklearn.ensemble import AdaBoostClassifier


def parameter_type_parser(param_type):
    parsed_param_type = {}
    parsed_param_type['numpydocparsestring'] = param_type
    parsed_param_type['param_type'] = []
    # print(param_type)
    # it is a list of valid inputs
    parsed_param_type['options'] = None
    parsed_param_type['default_value'] = None
    parsed_param_type['expected_shape'] = None
    if '{' in param_type:
        param_type = param_type.strip('{').strip('}')
        if ',' in param_type:
            options = [option.strip('\'') for option in param_type.split(',')]        
        else:
            options = [option.strip('\'') for option in param_type.split(' ')]
        parsed_param_type['param_type'] += ['LIST_VALID_OPTIONS']
        parsed_param_type['options'] = options
    elif '|' in param_type:
        options = [option.strip('\'') for option in param_type.split('|')]
        parsed_param_type['param_type'] += ['LIST_VALID_OPTIONS']
        parsed_param_type['options'] = options
    # elif ' or ' in param_type:
    #     options = [option.strip('\'').strip() for option in param_type.split('or')]
    #     parsed_param_type['param_type'] += ['LIST_VALID_OPTIONS']
    #     parsed_param_type['options'] = options
    else:
        pass
    # array of some shape, is None if no shape specified
    if 'array' in param_type:
        parsed_param_type['param_type'] += ['array']
        parsed_param_type['expected_shape'] = None
        shape_indicators = ['shape = ', 'shape =', 'shape= ', 'shape=', 'shape ', 'shape']
        for shape_indicator in shape_indicators:
            if shape_indicator in param_type:
                parsed_param_type['expected_shape'] = param_type[
                                                      param_type.find(shape_indicator) + len(shape_indicator):].strip()
    if 'dataframe' in param_type:
        parsed_param_type['param_type'] += ['dataframe']
        parsed_param_type['expected_shape'] = None
    # handling fundamental datatypes integer, float, string, boolean
    if 'object' in param_type:
        parsed_param_type['param_type'] += [object]
    if 'int' in param_type or 'integer' in param_type:
        parsed_param_type['param_type'] += [int]
    if 'float' in param_type:
        parsed_param_type['param_type'] += [float]
    if 'double' in param_type:
        parsed_param_type['param_type'] += [float]
    if 'bool' in param_type:
        parsed_param_type['param_type'] += [bool]
    if 'str' in param_type:
        parsed_param_type['param_type'] += [str]
    if 'dict' in param_type:
        parsed_param_type['param_type'] += [dict]
    if 'list' in param_type:
        parsed_param_type['param_type'] += [list]
    if 'tuple' in param_type:
        parsed_param_type['param_type'] += [tuple]
    if 'iterable' in param_type:
        parsed_param_type['param_type'] += [iter]
    if 'callable' in param_type:
        parsed_param_type['param_type'] += [callable]
    if 'None' in param_type:
        parsed_param_type['param_type'] += [None]
    parsed_param_type['is_optional'] = False
    if 'default' in param_type:
        parsed_param_type['is_optional'] = True
        default_str = param_type.split(',')[-1]
        default_indicators = ['by default', 'default:', 'default =', 'default=', 'default', 'default is']
        try:
            for default_indicator in default_indicators:
                parsed_param_type['default_value'] = default_str.lower()[default_str.find(default_indicator) + len(
                    default_indicator):].strip()
        except Exception as e:
            print('unable to parse parameter default value')
            parsed_param_type['default_value'] = None
    if 'optional' in param_type:
        parsed_param_type['is_optional'] = True
        parsed_param_type['default_value'] = None
    if len(parsed_param_type['param_type']) == 0:
        print('unable to parse parameter type')
        parsed_param_type['param_type'] += [None]
    return parsed_param_type


def numpy_doc_parser(data):
    inputs = []
    outputs = []
    for param in data['Parameters']:
        param_name, param_type, param_desc = param
        if param_name == 'self':
            continue
        param_desc = ' '.join(param_desc).strip()
        param_type = parameter_type_parser(param_type)
        # print(param_type)
        # Store into Input
        input_ = Input(param_name,
            param_desc,
            param_type['param_type'],
            param_type['expected_shape'],
            param_type['options'],
            param_type['is_optional'],
            param_type['default_value'])
        inputs += [input_]
    for param in data['Returns']:
        param_name, param_type, param_desc = param
        if param_name == 'self':
            continue
        param_desc = ' '.join(param_desc).strip()
        param_type = parameter_type_parser(param_type)
        # Store into Output with returned True
        output_ = Output(param_name,
            param_desc,
            param_type['param_type'],
            returned=True)
        outputs += [output_]        
    for param in data['Yields']:
        param_name, param_type, param_desc = param
        if param_name == 'self':
            continue
        param_desc = ' '.join(param_desc).strip()
        param_type = parameter_type_parser(param_type)
        # Store into Output with returned False
        output_ = Output(param_name,
            param_desc,
            param_type['param_type'],
            returned=False)
        outputs += [output_]
    for param in data['Attributes']:
        param_name, param_type, param_desc = param
        if param_name == 'self':
            continue
        param_desc = ' '.join(param_desc).strip()
        param_type = parameter_type_parser(param_type)
        output_ = Output(param_name,
                         param_desc,
                         param_type['param_type'],
                         returned=False)
        outputs += [output_]
    # print(param_type)
    return inputs, outputs


def numpy_fn_parser(fn):
    data = FunctionDoc(fn)
    # print(data)
    return numpy_doc_parser(data)


def numpy_cls_parser(cls):
    data = ClassDoc(cls)
    # print(data)
    return numpy_doc_parser(data)   


fn = AdaBoostClassifier.fit
inputs, outputs = numpy_fn_parser(fn=fn)
for input_ in inputs:
    print(input_)
for output in outputs:
    print(output)
