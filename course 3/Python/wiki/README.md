### wiki (5 + 3 points)

There is a comic "law of philosophy" for Wikipedia articles:
if you go to the first normal link in the article, then early or
late you will come to an article about philosophy.

This task is to check this theory. For this you need to write a program,
which receives a link to an article on Wikipedia, and then
through the first normal link and recursively repeats this
operation (until an article on philosophy is reached,
or links are not cycled). A normal reference will refer to
link, which is in the main content of the article, not in infoboxes and
not in the service blocks, written in blue (red corresponds to
non-existent article), not italicized, is not a footnote and does not find
in parentheses. Note that in order to check the normality,
be sure to disassemble style sheets and check the color, etc., sufficient
but to make the program work for the current layout of Wikipedia
(for example, you can use the `class` attribute of tags). For comfort
check that the sequence of transitions is displayed on the
screen. Locate your solution in the file `wiki.py`. True solution will get **5 points**,
and true solution that effectively used OOP will get **8 points**.

**Hints:** `bad_wiki.py`
