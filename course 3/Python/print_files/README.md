## print-files (3 points)

Write a program that writes a list of files in this
directory and sorts them according to their size. The program should
get the path to the directory as a command-line argument and print
on the screen names of all files in it and their sizes, and the first
go files with the largest size, and in the case of the same size files
sorted alphabetically. File name and file size could be tab-separated.
To run your program use
```
$ python3 print_files.py <path_to_dir>
```
To test your program use
```
$ python3 test_print_files.py
```

**Input:**
```
$ python3 print_files.py ../dictionary
```
**Output:**
```
dictionary.py    1988
output.txt    115
input.txt    82
README.md    18
```
**Hints:**
`sys`, `os.listdir()`, `os.stat()`, `os.path.isfile()`, `os.path.join()`
