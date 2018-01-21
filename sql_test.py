import sqlite3

conn = sqlite3.connect(weacher.db)
c = conn.cursor()
sql = """
	CREATE TABLE weather(
	id INTEGER NOT NULL,
 	city VARCHAR(80),
	text_day VARCHAR(80),
	text_night VARCHAR(80),
	low VARCHAR(80),
	high VARCHAR(80)
	)
"""
c.execute(sql)
c.commit()
c.execute("INSERT INTO weather VALUES(1,'深圳','多云','多云','10','12')")
c.commit()
print("success.")
c.close()
