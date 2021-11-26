import pymysql
import re

f = open('engTextProcess.txt')

db = pymysql.connect('localhost','root','123456','dict')

cursor = db.cursor()

for line in f:
	l = re.split(r"\s+",line)
	word = l[0]
	interpret=' '.join(1[1:])
	sql = "insert into words (word,interpret) \
	values('%s','%s')"%(word,interpret)

	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
f.close()	