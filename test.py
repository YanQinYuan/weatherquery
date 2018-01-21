import sqlite3 as ite

conn = ite.connect("weather.db")
with conn:
	cur = conn.cursor()
	cur.execute("select * from users where username='admin'")
	c = cur.fetchone()
	# dic.update({
	# 	"user_id":c[0],
	# 	"username":c[1]
	# 	})
	print(c)