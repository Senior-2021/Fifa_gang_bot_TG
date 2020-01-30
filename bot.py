import telebot
import config
import os
import db_handler
import random
import sqlite3

bot = telebot.TeleBot(config.token)

transl = "0123456789ABCDEF"

# Перевод элемента строки в цифру
def code(a):
    for i in range(len(transl)):
        if a == transl[i]:
            return i
        
# Перевод из строки в число   
def r2n(x,r):
    res = 0
    for i in x:
        c = code(i)
        res = res * r + c
    return res

# Перевод строки в массив
def s_l(a):
	x = []
	b = a.split(',')

	for i in range(len(b)):
		x.append(int(b[i]))
	return x

# Перевод массива в строку 
def l_s(a):
	x = ''
	for i in a:
		x = x + str(i) + ','
	x = x[:-1]
	return x

keyboard_start = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_start.row('Трейды и инвестиции')
keyboard_start.row('Викторина FUT')


keyboard_trade = telebot.types.ReplyKeyboardMarkup(True)
keyboard_trade.row('НАЗАД')



keyboard_chek = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_chek.row('Проверить подписку')


statuss = ['creator', 'administrator', 'member']
list_of_wrong_answers = ['Неправильно! Попробуй еще раз', 'Ты ошибаешься! Думай лучше']
list_of_right_answers = ['А ты не плох)))', 'Молодец, показываешь хороший результат!']

@bot.message_handler(commands=['start'])
def start_message(message):
	res = 0
	for chri in statuss:
		if chri == bot.get_chat_member('@robtrade', message.from_user.id).status:
			res += 1
			bot.send_message(message.chat.id, 'Приветствую тебя, дорогой фифер!')
			bot.send_message(message.chat.id, 'Выбери интерсующий тебя раздел', reply_markup=keyboard_start)
			break
	if res == 0:
		bot.send_message(message.chat.id, 'Хей бро, для начала подпишись на наш канал @robtrade. ', reply_markup=keyboard_chek)

@bot.message_handler(content_types=['text'])
def sbc(message):
	if message.text == 'Проверить подписку':
		res = 0
		for chri in statuss:
			if chri == bot.get_chat_member('@robtrade', message.from_user.id).status:
				res += 1
				bot.send_message(message.chat.id, 'Приветствую тебя, дорогой фифер!')
				bot.send_message(message.chat.id, 'Выбери интерсующий тебя раздел', reply_markup=keyboard_start)
				break
		if res == 0:
			bot.send_message(message.chat.id, 'Хей бро, для начала подпишись на наш канал @robtrade. ', reply_markup=keyboard_chek)

	keyboard_card = telebot.types.ReplyKeyboardMarkup(True, True)
	if message.text == 'Викторина FUT':
		l = [i for i in range(1,11)]
		random.shuffle(l)

		conn = sqlite3.connect('db_game.sqlite')
		c = conn.cursor()

		user_id = str(message.chat.username)
		file_index = 0
		lifes = 3 
		result = 0

		sql = '''INSERT INTO game (user_id, file_index, lifes, result, list) VALUES (''' + "'" + user_id + "'" + ',' + str(file_index) + ',' + str(lifes) + ',' + str(result) + ',' + "'" + l_s(l) + "'" + ')'

		c.execute(sql)
		conn.commit()


		sql1 = '''SELECT file_index FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql1)
		index = c.fetchone()

		c.close()
		conn.close()

		conn = sqlite3.connect('db.sqlite')
		c = conn.cursor()

		sql_keyboard_wrong = '''SELECT wrong_a FROM victorina WHERE id =''' + str(l[index[0]])
		c.execute(sql_keyboard_wrong)
		
		list_of_wrong = c.fetchone()[0]

		list_of_wrong = list_of_wrong.split(',')
		
		random.shuffle(list_of_wrong)

		c.close()
		conn.close()

		conn = sqlite3.connect('db.sqlite')
		c = conn.cursor()
		sql_keyboard_right = '''SELECT right_a FROM victorina WHERE id =''' + str(l[index[0]])
		c.execute(sql_keyboard_right)

		right_a = c.fetchone()[0]
		list_of_wrong.append(right_a)
		random.shuffle(list_of_wrong)

		c.close()
		conn.close()



		keyboard_first_card = telebot.types.ReplyKeyboardMarkup(True, True)
		keyboard_first_card.row(list_of_wrong[0], list_of_wrong[1])
		keyboard_first_card.row(list_of_wrong[2], list_of_wrong[3])
		keyboard_first_card.row('Закончить игру')

		keyboard_card = keyboard_first_card



		f = open('photo/victorina/' + str(l[index[0]]) + '.jpg', 'rb')

		bot.send_photo(message.chat.id, f, reply_markup=keyboard_card) 


	conn = sqlite3.connect('db_game.sqlite')
	c = conn.cursor()

	user_id = str(message.chat.username)

	sql_id = '''SELECT file_index FROM game WHERE user_id="''' + user_id + '"'
	c.execute(sql_id)
	file = c.fetchone()
	file_id = 0
	right = ''
	false = []
	sql_list = '''SELECT list FROM game WHERE user_id="''' + user_id + '"'
	c.execute(sql_list)
	L = c.fetchone()
	List = []
	List_of_wrong = []

	c.close()
	conn.close()

	if file != None:
		file_id = file[0]
		List = s_l(L[0])

		conn = sqlite3.connect('db.sqlite')
		c = conn.cursor()

		sql_for_r_a = '''SELECT right_a FROM victorina WHERE id =''' + str(List[file_id])
		c.execute(sql_for_r_a)
		right = c.fetchone()[0]

		sql_for_w_a = '''SELECT wrong_a FROM victorina WHERE id =''' + str(List[file_id])
		c.execute(sql_for_w_a)

		l_w = c.fetchone()[0]
		List_of_wrong = l_w.split(',')

		c.close()
		conn.close()

		

	for i in List_of_wrong:
		if message.text == i:
			user_id = str(message.chat.username)

			conn = sqlite3.connect('db_game.sqlite')
			c = conn.cursor()
			sql_life = '''SELECT lifes FROM game WHERE user_id="''' + user_id + '"' 
			c.execute(sql_life)
			lifes = c.fetchone()[0]
			lifes = lifes - 1

			sql_lifes1 = '''UPDATE game SET lifes="''' + str(lifes) + '"' + ' ' + '''WHERE user_id=''' + "'" + user_id + "'"
			c.execute(sql_lifes1)
			conn.commit()

			sql_res = '''SELECT result FROM game WHERE user_id="''' + user_id + '"'
			c.execute(sql_res)
			res = c.fetchone()[0]

			c.close()
			conn.close()


			if lifes <= 0:

				conn = sqlite3.connect('db_game.sqlite')
				c = conn.cursor()

				user_id = str(message.chat.username)

				sql = '''DELETE FROM game WHERE user_id="''' + user_id + '"'
				c.execute(sql)
				conn.commit()

				c.close()
				conn.close()

				bot.send_message(message.chat.id, 'У тебя закончились жизни(((', reply_markup=keyboard_start)

			if lifes > 0:
				bot.send_message(message.chat.id, list_of_wrong_answers[random.randint(0, len(list_of_wrong_answers)-1)], reply_markup=keyboard_card)
				bot.send_message(message.chat.id, 'Оставшиеся попытки:' + str(lifes))
				bot.send_message(message.chat.id, 'Ты угадал ' + str(res) + '/' + str(10))


	if message.text == right and file_id < 9:
		conn = sqlite3.connect('db_game.sqlite')
		c = conn.cursor()

		user_id = str(message.chat.username)

		sql = '''SELECT file_index FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql)
		index = c.fetchone()
		file_index = r2n(str(index[0]), 10) + 1

		sql1 = '''UPDATE game SET file_index=''' + str(file_index) + ' ' + '''WHERE user_id=''' + "'" + user_id + "'"
		c.execute(sql1)
		conn.commit()

		sql2 = '''SELECT list FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql2)
		l = c.fetchone()
		l = s_l(l[0])

		sql_lifes = '''SELECT lifes FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql_lifes)
		lifes = c.fetchone()[0]

		sql_res = '''SELECT result FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql_res)
		res = c.fetchone()[0]
		res = res + 1

		sql_res_up = '''UPDATE game SET result =''' + str(res) + ' ' + '''WHERE user_id=''' + "'" + user_id + "'"
		c.execute(sql_res_up)
		conn.commit()

		c.close()
		conn.close()

		f = open('photo/victorina/' + str(l[file_index]) + '.jpg', 'rb')

		conn = sqlite3.connect('db.sqlite')
		c = conn.cursor()

		sql_keyboard_wrong1 = '''SELECT wrong_a FROM victorina WHERE id =''' + str(l[file_index])
		c.execute(sql_keyboard_wrong1)
		
		list_of_wrong1 = c.fetchone()[0]

		list_of_wrong1 = list_of_wrong1.split(',')
		
		random.shuffle(list_of_wrong1)

		c.close()
		conn.close()

		conn = sqlite3.connect('db.sqlite')
		c = conn.cursor()
		sql_keyboard_right1 = '''SELECT right_a FROM victorina WHERE id =''' + str(l[file_index])
		c.execute(sql_keyboard_right1)

		right_a1 = c.fetchone()[0]
		list_of_wrong1.append(right_a1)
		random.shuffle(list_of_wrong1)

		c.close()
		conn.close()



		keyboard_first_card1 = telebot.types.ReplyKeyboardMarkup(True, True)
		keyboard_first_card1.row(list_of_wrong1[0], list_of_wrong1[1])
		keyboard_first_card1.row(list_of_wrong1[2], list_of_wrong1[3])
		keyboard_first_card1.row('Закончить игру')
		keyboard_card = keyboard_first_card1
		bot.send_message(message.chat.id, list_of_right_answers[random.randint(0, len(list_of_right_answers)-1)])
		bot.send_message(message.chat.id, 'Оставшиеся попытки:' + str(lifes))
		bot.send_message(message.chat.id, 'Ты угадал ' + str(res) + '/' + str(10))
		bot.send_photo(message.chat.id, f, reply_markup=keyboard_card)

	if message.text == right and file_id >= 9:

		conn = sqlite3.connect('db_game.sqlite')
		c = conn.cursor()

		user_id = str(message.chat.username)

		sql_res = '''SELECT result FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql_res)
		res = c.fetchone()[0]
		res = res + 1

		sql = '''DELETE FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql)
		conn.commit()


		c.close()
		conn.close()

		bot.send_message(message.chat.id, 'Молодец!')
		bot.send_message(message.chat.id, 'Ты угадал ' + str(res) + '/' + str(10), reply_markup=keyboard_start)


	if message.text.lower() == 'закончить игру':
		conn = sqlite3.connect('db_game.sqlite')
		c = conn.cursor()

		user_id = str(message.chat.username)

		sql_res = '''SELECT result FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql_res)
		res = c.fetchone()[0]

		sql = '''DELETE FROM game WHERE user_id="''' + user_id + '"'
		c.execute(sql)
		conn.commit()

		c.close()
		conn.close()

		bot.send_message(message.chat.id, 'Конец игры')
		bot.send_message(message.chat.id, 'Ты угадал ' + str(res) + '/' + '10', reply_markup=keyboard_start)
            


	if message.text == 'НАЗАД':
		bot.send_message(message.chat.id, 'Выбери интерсующий тебя раздел', reply_markup=keyboard_start)

	if message.text == 'Трейды и инвестиции':
		f = open(db_handler.trade1, 'rb')
		bot.send_photo(message.chat.id, f)
		bot.send_message(message.chat.id, db_handler.txt1, reply_markup=keyboard_trade)



if __name__ == '__main__':
	bot.polling(none_stop=True)






