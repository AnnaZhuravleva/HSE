import sqlite3
conn = sqlite3.connect('Аня.sqlite')
c = conn.cursor()

c.execute('SELECT * FROM texts')

results = c.fetchall()
#print(results)

for row in results:
    print('id: {}\n'.format(row[0]))
    print('place: {}\n'.format(row[1]))
    print('text: {}\n'.format(row[2]))
    print('informant: {}\n'.format(row[3]))
    print('---- '*10)
print("Adding record:")
city = input("place:")
text = input('text:')
informant = input('informant: ')

c.execute('INSERT INTO texts(city, text, informant) VALUES (?, ?, ?)', [city,text,informant])
conn.commit()

