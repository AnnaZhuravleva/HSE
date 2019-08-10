### property-maker (3 points)

Implement metaclass `PropertyMaker` that makes visible attribute `<attr_name>` if class has
getter method `Class.get_<attr_name>()`, also if class has setter method `Class.set_<attr_name>(value)`
setattr procedure is real for `<attr_name>` attribute. For more details see docstring and `test_property.py` file.

**Hints:** `metaprogramming`, `__new__`
