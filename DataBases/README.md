# Neo4j

- База данных содержит стимулы для нейролингвистического эксперимента.

### Устройство базы данных

- Participant 1
  - Stimul 1 
    - Alternative-force-choice test: Answer 1, Answer 2, Answer 3, Correct answer, Participent's answer, Reaction time
    - Recognition test: Answer 1, Correct answer, Participent's answer, Reaction time
    - Semantic decision test: Answer 1, Answer 2, Answer 3, Correct answer, Participent's answer, Reaction time
  - Stimul 2 
    - Alternative-force-choice test: Answer 1, Answer 2, Answer 3, Correct answer, Participent's answer, Reaction time
    - Recognition test: Answer 1, Correct answer, Participent's answer, Reaction time
    - Semantic decision test: Answer 1, Answer 2, Answer 3, Correct answer, Participent's answer, Reaction time
       
- Participant 2
  - Stimul 1 
    - Alternative-force-choice test: Answer 1, Answer 2, Answer 3, Correct answer, Participent's answer, Reaction time
    - Recognition test: Answer 1, Correct answer, Participent's answer, Reaction time
    - Semantic decision test: Answer 1, Answer 2, Answer 3, Correct answer, Participent's answer, Reaction time
  - Stimul 2 
    - Alternative-force-choice test: Answer 1, Answer 2, Answer 3, Correct answer, Participent's answer, Reaction time
    - Recognition test: Answer 1, Correct answer, Participent's answer, Reaction time
    - Semantic decision test: Answer 1, Answer 2, Answer 3, Correct answer, Participent's answer, Reaction time
       
 Для каждого участника есть два списка стимулов:
 
 1) Список псевдослов
 2) Список их переводов
 
 - Для чистоты эксперимента набор исходных слов идентичен для каждого участника, но пары псевдослово-перевод отличаются (например, abene для одного участника будет обозначать 'кошка', а для другого - 'собака')
 - Мы хотим определить, насколько эффективно участник запомнил каждое слово из списка, и поэтому для каждого слова собираем данные трех тестов
 - В тесте Alternative-forced-choice участник видит псевдослово и выбирает один вариант его перевода на русский из трех
 - В тесте recognition участник видит пару псевдослово-перевод и должен ответить, верна пара или нет
 - В тесте semantic decision участник видит псевдослово и три семантические категории, его задача - выбрать верную (например, abene - люди, животные или предметы?)
 
 
 Так как списки для тестов тоже различаются, то мы и храним для каждого участника набор из разных списков
 
 
 
      
       
