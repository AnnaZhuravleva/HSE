### logger-mixin (3 points)

Implement mixin class `LoggerMixin` that adds methods-logging behaviour to base class.
Logging information (method call stack) should be aggregated in `__str__` method.
Do not log `__magic__` methods and any not callable attributes. For more details see docstring and 
`test_logger_mixin.py` file.

**Hints:** `mixin`, `__getattribute__`
