### decoder (15 + 25 points)

You need to implement class `Decoder` that solves a substitution cipher
problem, for example,
```buildoutcfg
abcdefghijklmnopqrstuvwxyz  # alphabet
zklyqpnifjdcutvwsxmagoebhr  # encryption key
txlkwiuyhjbcsgvfezqnmoprd   # decryption key

# plaintext
THE MAN WHO DOES NOT READ BOOKS HAS NO ADVANTAGE
OVER THE MAN THAT CAN NOT READ THEM. --MARK TWAIN

# ciphertext
AIQ UZT EIV YVQM TVA XQZY KVVDM IZM TV ZYOZTAZNQ
VOQX AIQ UZT AIZA LZT TVA XQZY AIQU. --UZXD AEZFT
```
the essence of the task is to restore the initial text (`plaintext`) from the
 coded text (`ciphertext`), as well as the permutation of the letters of the alphabet (`encryption` and `decryption` keys)
 with which the coded text (`ciphertext`) was obtained.
 
 Example of usage:
 ```python
from decoder import Decoder, Scorer

scorer = Scorer("english_quadgrams.txt")        # or another frequency dict
decoder = Decoder(score_func=scorer, **kwargs)  # some useful kwargs

decoder = decoder.fit(ciphertext, **kwargs)     # some useful kwargs

assert decoder.transform(ciphertext) == plaintext
assert decoder.encryption_ == encryption
assert decoder.decryption_ == decryption
assert decider.inverse_transform(plaintext) == ciphertext
```
To test your implementation use `first.txt` and `second.txt` files. Place decoded plaintexts in files `first_decoded.txt` and `second_decoded.txt`.
For true **parallel implementation** you will get **25 more points**!

**Hints:** [`substitution ciphers`](https://people.csail.mit.edu/hasinoff/pubs/hasinoff-quipster-2003.pdf), [`quadgrams`](http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/)