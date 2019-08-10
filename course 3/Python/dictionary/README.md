## dictionary (3 points)

File `input.txt` is an English-Latin dictionary, that is, a list of words on
English and their translations into Latin (translations may be
several). It is necessary to create a Latin-English dictionary from it and save into `output.txt` file. Words must be arranged in alphabetical order! For this, you need to implement two functions correctly (see file `dictionary.py`). To run your program use 
```
$ python3 dictionary.py < input.txt > output.txt
```

**Input:**
```
apple - malum, pomum, popula
fruit - baca, bacca, popum
punishment - malum, multa
```
**Output:**
```
baca - fruit
bacca - fruit
malum - apple, punishment
multa - punishment
pomum - apple
popula - apple
popum - fruit
```
**Hints:** [`IO redirection in shell`](https://robots.thoughtbot.com/input-output-redirection-in-the-shell)
