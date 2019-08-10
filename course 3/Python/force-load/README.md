### force-load (6 points)

Implement function `force_load` that can load correct objects and blocks from *bad module*.
*Bad module* is module where some lines can't be imported and raise exceptions.
For example,
```python
#!/usr/bin/env python3           # OK
-*- coding: utf-8 -*-            # NOT OK

Delay normalno i budet normalno  # NOT OK

class Bar                        # NOT OK


def bar(n):                      # OK
    """
    :param n: int                # OK
    :return: str, n times "bar"  # OK
    """                          # OK
    assert isinstance(n, int)    # OK
    return "bar" * n             # OK


import math                      # OK
bar = math.sqrt("Mark")          # NOT OK
```
Well, you can import only `bar` and `math` objects from example listed above. For more details see `test_force_load.py` and `bad_*.py` modules. Your function should return dictionary with
imported objects.

**Hints:** `exec`, `globals()`, `try/except`, `traceback`

Also your implementation should have this line (or how to handle correct objects and blocks (lines) from *bad module* to dictionary):
```python
exec("".join(lines), globals(), returned_dict)
```
