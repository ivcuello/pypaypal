import random
import inspect
from enum import Enum
from typing import Iterable
from secrets import token_hex

# Import target module
from pypaypal.entities import payouts

from pypaypal.entities.base import PayPalEntity

_IT_MAPPING = { 'List': list, 'Set': set, 'Dict': dict, 'Tuple': tuple }

class SampleHolder:
    def __init__(self, entity_type: type, json_sample: str):
        self.entity_type = type
        self.json_sample = json_sample

class ModuleProcessor:

    def __init__(self, module_ref, full_module_name: str):
        self.entities = dict()
        self.enumerations = dict()
        self.module_ref = module_ref
        self.full_module_name = full_module_name

    def load_samples(self):
        for k, v in self.module_ref.__dict__.items():
            if isinstance(v, type) and v.__module__ == self.full_module_name:
                if Enum in v.__bases__ and not k in self.enumerations.keys():
                    self.enumerations[k] = v
                elif PayPalEntity in v.__bases__ and not k in self.entities.keys():
                    sample = self._make_json_sample(v)
                    self.entities[k] = SampleHolder(v, sample.to_dict() if hasattr(sample, 'to_dict') else sample.__dict__)
    
    def _check_iterable(self, btype):
        # Checking for typing non instatiable types
        ntype = _IT_MAPPING.get(btype.__name__)
        return ntype if ntype else btype

    def _random_built_in_sample(self, btype, arg_name):
        t_name = btype.__name__        
        if t_name == 'str':
            # Special use cases
            if 'amount' in arg_name:
                return str(random.randint(1, 9999))
            if 'area_code' == arg_name:
                return str(random.randint(100, 999))
            if 'currency_code' == arg_name:
                return 'USD'
            return token_hex().upper()
        if t_name == 'int':
            return random.randint(1, 9999)
        if t_name == 'float':
            return float(random.randint(1, 9999))
        return None

    def _make_json_sample(self, clazz: type) -> dict:
        bt_set = { 'builtins', '__builtins__', 'typing' }
        inspection = inspect.getfullargspec(clazz.__init__)

        arg_samples = dict()
        valid = set(inspection.args[1:])
        ctor_args = { k : v for k,v in inspection.annotations.items() if k in valid }

        for k, v in ctor_args.items():
            ins = self._check_iterable(v)
            if ins.__module__ in bt_set and isinstance(ins(), Iterable) and not isinstance(ins(), str):
                # Collecions & Arrays
                inner_type = v.__args__[0] if v.__args__ else None
                if not inner_type:
                    arg_samples[k] = []
                else:
                    arg_samples[k] = [ self._random_built_in_sample(inner_type, k) ] if inner_type in bt_set else [ self._make_json_sample(inner_type) ]
            elif v.__module__ in bt_set:
                # Built in data types
                arg_samples[k] = self._random_built_in_sample(v, k)
            else:
                # Custom types
                arg_samples[k] = self._make_json_sample(v)        
        return clazz(**arg_samples)

template_1 = r"""
class {EntityName}Test(unittest.TestCase):
    '''Test class for {EntityName}'''

    def setUp(self):
        self.sample_dict = {SampleDict}

    def test_serialize_from_json(self):
        '''Testing json_response serialization factory method'''        
        e = {module_name}.{EntityName}.serialize_from_json(self.sample_dict)        
        self.assertEqual(e.json_data, self.sample_dict)

    def test_instance_from_dict(self):
        '''Testing instance from dict factory method'''
        e = {module_name}.{EntityName}.instance_from_dict(self.sample_dict)
        self.assertEqual(e.json_data, self.sample_dict)
""".replace("'''", '"""')

# Imported target module
target_module = payouts
module_namespace = target_module.__package__
module_name = target_module.__name__.split('.').pop()

# test files path
FILE_PATH = r'/pypaypal/test/entities/{module_name}.py'\
    .replace('{module_name}', module_name)

p = ModuleProcessor(target_module, target_module.__name__)
p.load_samples()

with open(FILE_PATH, 'r') as read_file:
    content = read_file.read()

test_templates = [''] * 2
test_templates[0] = 'from {} import {}'.format(module_namespace, module_name)

for k,v in p.entities.items():
    tmp = template_1.replace('{module_name}', module_name)\
        .replace('{EntityName}', k)\
        .replace('{SampleDict}', str(v.json_sample))

    test_templates.append(tmp)

content = content.replace('# TODO: Write tests here', '\n'.join(test_templates))

with open(FILE_PATH, 'w') as write_file:
    write_file.write(content.replace('# TODO: Write tests here', '\n'.join(test_templates)))
