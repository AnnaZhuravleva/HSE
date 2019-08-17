# 6. в скольких папках встречается несколько файлов с одним и тем же расширением;
import os
number = 0
for roots, dirs, files in os.walk('.'):
    names = []
    for f in files:
        name = f[::-1].split('.')[0]
        if name not in names:
            names.append(name)
        else:
            number += 1
            break
print(number)
