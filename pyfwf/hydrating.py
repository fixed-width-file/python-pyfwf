"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = "Kelson da Costa Medeiros <kelsoncm@gmail.com>"

__all__ = ["hydrate_object", "dehydrate_object", "Hydrator"]

import importlib
from typing import Dict, List

CLASS_NAME_MAPPING = {
    "io.github.kelsoncm.fwf.columns.CharColumn": "pyfwf.columns.CharColumn",
    "io.github.kelsoncm.fwf.columns.RightCharColumn": "pyfwf.columns.RightCharColumn",
    "io.github.kelsoncm.fwf.columns.PositiveIntegerColumn": "pyfwf.columns.PositiveIntegerColumn",
    "io.github.kelsoncm.fwf.columns.PositiveDecimalColumn": "pyfwf.columns.PositiveDecimalColumn",
    "io.github.kelsoncm.fwf.columns.DateTimeColumn": "pyfwf.columns.DateTimeColumn",
    "io.github.kelsoncm.fwf.columns.DateColumn": "pyfwf.columns.DateColumn",
    "io.github.kelsoncm.fwf.columns.TimeColumn": "pyfwf.columns.TimeColumn",
    "io.github.kelsoncm.fwf.descriptors.HeaderRowDescriptor": "pyfwf.descriptors.HeaderRowDescriptor",
    "io.github.kelsoncm.fwf.descriptors.DetailRowDescriptor": "pyfwf.descriptors.DetailRowDescriptor",
    "io.github.kelsoncm.fwf.descriptors.FooterRowDescriptor": "pyfwf.descriptors.FooterRowDescriptor",
    "io.github.kelsoncm.fwf.descriptors.FileDescriptor": "pyfwf.descriptors.FileDescriptor",
}


def get_full_class_name(instance_or_class):
    if isinstance(instance_or_class, type):
        return instance_or_class.__module__ + "." + instance_or_class.__qualname__
    else:
        return instance_or_class.__module__ + "." + instance_or_class.__class__.__qualname__


def create_class(full_class_name, *args, **kwargs):
    full_class_name = CLASS_NAME_MAPPING.get(full_class_name, full_class_name)
    module_name, class_name = full_class_name.rsplit(".", 1)
    MyClass = getattr(importlib.import_module(module_name), class_name)
    return MyClass(*args, **kwargs)


def assert_element_isinstance(name, lst, cls):
    if name in lst:
        if not isinstance(lst[name], cls):
            raise TypeError("%s has informed, but is not a %s" % (name, cls))


def assert_isinstance(name, value, cls):
    if not isinstance(value, cls):
        raise TypeError("%s is not a %s" % (name, cls))


def hydrate_object(representation: Dict):
    assert_isinstance("representation", representation, Dict)
    if "_hydrate_as" not in representation:
        raise ValueError("_hydrate_as is required")
    assert_element_isinstance("_hydrate_as", representation, str)
    assert_element_isinstance("args", representation, List)
    assert_element_isinstance("kwargs", representation, Dict)
    assert_element_isinstance("attributes", representation, Dict)

    def hydrate_if_hydratable(o):
        return hydrate_object(o) if isinstance(o, Dict) and "_hydrate_as" in o else o

    hydrate_as = representation["_hydrate_as"]
    args = [hydrate_if_hydratable(arg) for arg in (representation["args"] if "args" in representation else [])]
    kwargs = {
        k: hydrate_if_hydratable(v) for k, v in (representation["kwargs"] if "kwargs" in representation else {}).items()
    }
    attributes = representation["attributes"] if "attributes" in representation else {}

    instance = create_class(hydrate_as, *args, **kwargs)
    for attr_name in attributes.keys():
        setattr(instance, attr_name, attributes[attr_name])
    return instance


def dehydrate_object(obj):
    def dehydrate_if_hydratable(o):
        return dehydrate_object(o) if isinstance(o, Hydrator) else o

    result = {"_hydrate_as": get_full_class_name(obj)}
    if hasattr(obj, "hydrating_args"):
        result["args"] = [dehydrate_if_hydratable(getattr(obj, name)) for name in obj.hydrating_args]
    if hasattr(obj, "hydrating_kwargs"):
        result["kwargs"] = {name: dehydrate_if_hydratable(getattr(obj, name)) for name in obj.hydrating_kwargs}
    if hasattr(obj, "hydrating_attributes"):
        result["attributes"] = {name: dehydrate_if_hydratable(getattr(obj, name)) for name in obj.hydrating_attributes}
    return result


class Hydrator(object):
    def dehydrate(self):
        return dehydrate_object(self)

    @classmethod
    def hydrate(cls, representation: Dict):
        return hydrate_object(representation)
