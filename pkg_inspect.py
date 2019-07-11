import pkgutil
import sys
import os
import inspect
import pickle

from numpydoc_parser import numpy_fn_parser, numpy_cls_parser
from db_containers import NodeFunction, Node

def explore_package(module_name):
    try:
        loader = pkgutil.get_loader(module_name)
    except ImportError as e:
        print('no __path__ found')
        return None
    filepaths = [os.sep.join(loader.get_filename().split(os.sep)[:-1])]
    for sub_module in pkgutil.walk_packages(filepaths):
        print(sub_module)
        _, sub_module_name, _ = sub_module
        qname = module_name + "." + sub_module_name
        print(qname)
        explore_package(qname)

# explore_package(sys.argv[1])

def describe_builtin(obj):
    """ Describe a builtin function """
    # Built-in functions cannot be inspected by
    # inspect.getargspec. We have to try and parse
    # the __doc__ attribute of the function.
    docstr = obj.__doc__
    args = ''
    if docstr:
        items = docstr.split('\n')
        if items:
            func_descr = items[0]
            s = func_descr.replace(obj.__name__, '')
            idx1 = s.find('(')
            idx2 = s.find(')', idx1)
            if idx1 != -1 and idx2 != -1 and (idx2 > idx1 + 1):
                args = s[idx1 + 1:idx2]
    return args

def explore_module(mymodule, package_name, node=None):
    if node is None:
        node = Node(package_name,
                '',
                inputs=[],
                outputs=[],
                node_functions=[],
                nodes=[])
    print('exploring', mymodule)
    for element_name in dir(mymodule):
        # ignore private and inbuilt members, functions
        if (element_name.startswith('__') or element_name.endswith('__')) and 'init' not in element_name:
            continue
        element = getattr(mymodule, element_name)
        if inspect.isclass(element):
            print("class %s" % element_name)
            # call numpy_cls_parser here
            inputs, outputs = numpy_cls_parser(cls=element)            
            node_ = Node(element_name,
                element.__doc__,
                inputs,
                outputs,
                node_functions=[],
                nodes=[])                                    
            explore_module(element, '', node_) # recurse into subclasses
            node.nodes += [node_] # update parent node with recursive child node information
        elif inspect.ismodule(element):
            # explore_module(element)
            pass
        elif hasattr(element, '__call__'):
            if inspect.isbuiltin(element):
                sys.stdout.write("builtin_function %s" % element_name)
                data = describe_builtin(element)
                data = data.replace("[", " [")
                data = data.replace("  [", " [")
                data = data.replace(" [, ", " [")
                sys.stdout.write(data.replace(", ", " "))
                print("")
            else:
                try:
                    # data = inspect.getargspec(element)
                    print('function', element_name)                    
                    inputs, outputs = numpy_fn_parser(fn=element)
                    node_fn = NodeFunction(element_name,
                        element.__doc__,
                        inputs,
                        outputs)
                    node.node_functions += [node_fn]                    
                except:
                    pass
        else:
            print("value %s" % element_name)       

if len(sys.argv) > 1:
    package_name = sys.argv[1].strip()
else:
    package_name = 'sklearn.decomposition'
mymodule = __import__(package_name, fromlist=['foo'])
node = Node(package_name,
                '',
                inputs=[],
                outputs=[],
                node_functions=[],
                nodes=[])
explore_module(mymodule, package_name, node)
print(node)
outfile_name = '{}.db.pkl'.format(package_name)
with open(outfile_name, 'wb') as f:
    pickle.dump(node, f)