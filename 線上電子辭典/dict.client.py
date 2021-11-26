from socket import *
import sys
import getpass

#創見網路連接
def main():
	if len(sys.argv) <3:
		print("argv is error")
		return

	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	s = socket()
	try:
		s.connect((HOST,PORT))

	except Exception as e:
		print(e)
		return

	while True:
		print('''
			========welcome=========
			--1.註冊  2.登錄  3.退出--
			========================
			''')
		try:
			cmd = int(input("輸入選項>>"))
		except Exception as e:
			print("命令錯誤")
			continue
		if cmd not in [1,2,3]:
			print("請輸入正確選項")
			sys.stdin.flush()#清除標準輸入（緩衝區)
			#continue
		elif cmd == 1:
			r = do_register(s)#連接客戶端端口
			if r ==0:
				print("註冊成功")
				#進入二級界面
			elif r ==1:
				print("用戶存在")
			else:
				print("註冊失敗")
		elif cmd == 2:
			name = do_login(s)
			if name:
				print("登錄成功")#在這登錄二級界面
				login(s,name)
			else:
				print("用戶明或密碼不正確")

		elif cmd ==3:
			s.send(b"E")
			sys.exit("謝謝使用")



def login(s,name):
	while True:
		print('''
			=========查詢界面========
			1.查詞  2.歷史紀錄  3.退出)
			''')
		try:
			cmd = int(input("輸入選項>>"))
		except Exception as e:
			print("命令錯誤")
			continue
		if cmd not in [1,2,3]:
			print("請輸入正確選項")
			sys.stdin.flush()#清除標準輸入（緩衝區)
			continue
		elif cmd == 1:
			do_query(s,name)
		elif cmd == 2:
			do_hist(s,name)
		elif cmd ==3:
			return
def do_hist(s,name):
	msg= "H {}".fotmat(name)
	s.send(msg.encode())
	data =s.recv(128).decode()
	if data =='OK':
		while True:
			data =s.recv(1024).decode()
			if data =='##':
				break
	else:
		print("沒有歷史紀錄")

		
def do_query(s,name):
	while True:
		word = input("單詞：")
		if word =='##':
			break

		msg = "Q {} {}".format(name,word)
		s.send(msg.encode())
		data = s.recv(128).encode()
		if data =='OK':
			data = s.recv(2048).decode()
			print(data)
		else:
			print("沒有查到該單詞")
def fo_hist():
	pass



def do_register(s):
	while True:
		name =input("User:")
		passwd = getpass.getpass()
		passwd2 = getpass.getpass('Again:')

		if (' 'in name) or (' ' in passwd):
			print("用戶明和密碼不許空格")
			continue
		if passwd != passwd2:
			print("兩次密碼不一致")
			continue

		msg ='R {} {}'.format(name,passwd)
		#發送請求
		s.send(msg.encode())
		#等待回覆
		data =s.recv(128).decode()
		if data == "OK":
			return 0
		elif data =='EXISTS':
			return 1
		else:
			return 2

def do_login(s):
	name =input("User:")
	passwd =getpass.getpass()
	msg = "L {} {} ".format(name,passwd)
	s,send(msg.decode())
	data = s.recv(128).decode()

	if data =="OK":
		return name
	else:
		return null


if __name__ =="__main__":
	main()