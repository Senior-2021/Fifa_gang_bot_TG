import sqlite3 

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

# c.execute('''CREATE TABLE trade (id INTEGER, name TEXT, file_id TEXT, txt TEXT )''')
# c.execute('''INSERT INTO trade (id, name, file_id, txt) VALUES (1, 'trade1', 'trades_photo/-ya8SaLmVj4.jpg', 'FLIP Инвестиции из уходящей TOTW✅

# Не самые лучшие цены на игроков сейчас, но заработать на них ещё как получится!

# Покупку осуществляйте сегодня до 20:00
# Советую брать по ставке - так проще будет урвать дешевле⚠

# Продажу осуществляем на следующей неделе во время пика цен перед WL. Мои прогнозы на стоимость карт:
# 1)Mahrez IF - 150.000+
# 2)Havertz IF - 220.000+
# 3)Ndindi IF - 80.000+')''')
# conn.commit()
# c.execute('''CREATE TABLE sbc_live (id INTEGER, name TEXT, file_id TEXT, txt TEXT)''')
# c.execute('''INSERT INTO sbc_live (id, name, file_id, txt) VALUES (1, 'PISZCZEK FLASHBACK', 'None', 'None')''')
# conn.commit()
# c.execute('''CREATE TABLE sbc_prod (id INTEGER, name TEXT, file_id TEXT, txt TEXT)''')
# c.execute('''CREATE TABLE sbc_osn (id INTEGER, name TEXT, file_id TEXT, txt TEXT)''')
# c.execute('''CREATE TABLE sbc_osn (id INTEGER, name TEXT, file_id TEXT, txt TEXT)''')
# c.execute('''CREATE TABLE teams_100K (id INTEGER, file_id TEXT, txt TEXT)''')
# c.execute('''CREATE TABLE teams_300K (id INTEGER, file_id TEXT, txt TEXT)''')
# c.execute('''CREATE TABLE teams_500K (id INTEGER, file_id TEXT, txt TEXT)''')
# c.execute('''CREATE TABLE teams_1KK (id INTEGER, file_id TEXT, txt TEXT)''')
# c.execute('''CREATE TABLE victorina (id integer, file_id TEXT, right_a TEXT, wrong_a TEXT)''')
c.close()
conn.close()

#TRADE
conn = sqlite3.connect('db.sqlite')
c = conn.cursor()
c.execute('''SELECT file_id FROM trade''')
row_of_file_id_of_trade = c.fetchone()
c.close()
conn.close()

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()
c.execute('''SELECT txt FROM trade''')
row_of_txt_of_trade = c.fetchall()
c.close()
conn.close()
#END TRADE













