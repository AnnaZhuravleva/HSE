В этом репозитории содержатся описания и шаблоны решений задач по Теории алгоритмов в Школе Лингвистики ВШЭ.

Оригинальный репозиторий: [hse-ling-algorithms/hap](https://bitbucket.org/hse-ling-algorithms/hap)

# Пререквизиты

Чтобы сдавать задачи, вам необходимо сделать закрытый форк оригинального репозитория в личном аккаунте на Bitbucket.

* Залогиньтесь на сайте [hse.mkuznets.com](https://hse.mkuznets.com) с помощью своего аккаунта на Bitbucket.
* Форк репозитория [hse-ling-algorithms/hap](https://bitbucket.org/hse-ling-algorithms/hap) создастся автоматически и будет показан на сайте.

Решения принимаются только из закрытых форков.

Дальнейшие действия предполагается делать именно с форком.

# Задачи

* Каждая задача находится в отдельной директории.
* В каждой из них есть шаблон решения и файл с тестами.
* Эти тесты — базовые, их прохождение не гарантирует корректность решения.

# Проверка задач

* Для отправки задачи на проверку:
    * удалите файл `remove-this-file-when-ready` из директории решённой задачи;
    * закоммитьте решение;
    * сделайте push.
* Статус и отчёт проверки вы увидите в списке коммитов в интерфейсе Bitbucket.
* При каждом push тестируются все задачи, найденные в репозитории. Если код задачи уже тестировался и с тех пор не менялся, тесты запущены не будут.
* Задачи с файлом `remove-this-file-when-ready` не тестируются.

## Ограничения

* Запуск каждого набора юнит-тестов ограничен 10 секундами, тестов производительности — 120 секундами.
* Потребляемая тестами память ограничена 512 Мб.

При превышении ограничений проверка задачи завершается неудачей.

# Обновления

* В оригинальный репозиторий со временем будут добавляться директории с новыми задачи.
* Для их решения, вам нужно будет продублировать их в форке.
* Не важно, как именно это будет сделано, главное чтобы структура файлов в оригинальном репозитории и форке не отличалась.
* Проще всего обновлять форк через интерфейс Bitbucket:
    * Repository details -> Sync
    * После этого надо сделать pull в локальной копии репозитория
    * Если у вас есть действующие ветки помимо master, их нужно будет слить с master вручную.