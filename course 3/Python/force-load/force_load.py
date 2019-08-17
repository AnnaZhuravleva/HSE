#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def force_load(module_name: str)-> dict:
    """
    >>> isinstance(force_load("bad_foo"), dict)
    True
    >>> len(force_load("bad_foo"))
    1
    >>> force_load("bad_foo")["foo"]("foo")
    'foo foo'
    """
    filename = module_name + '.py'
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    max = len(lines)
    returned_dict = {}
    i = 1
    k = 0
    while i <= max:
        tmpdict = {}
        testlines = lines[k:i + 1]
        try:
            exec(''.join(testlines), globals(), tmpdict)
            for key in tmpdict:
                returned_dict[key] = tmpdict[key]
            k += 1
        except:
            tmp = k
            while tmp < i:
                tmpdict = {}
                try:
                    exec(''.join(lines[tmp:i + 1]), globals(), tmpdict)
                    for key in tmpdict:
                        returned_dict[key] = tmpdict[key]
                    k = tmp
                    break
                except:
                    tmp += 1
            pass
        i += 1
    return returned_dict


if __name__ == "__main__":
    import doctest
    doctest.testmod()
