import copy

class RegisterMachine(object):

	def __init__(self, seq = []):
		self.data = seq

	def display(self):
		print self.data

	def run(self, program):
		commands = program.data
		line = 0
		command = commands[line]
		while command[0] != 'END':
			if command[0] == 'Z':
				self.set(command[1], 0)
			elif command[0] == 'S':
				self.set(command[1], self.get(command[1]) + 1)
			elif command[0] == 'T':
				self.set(command[2], self.get(command[1]))
			elif command[0] == 'J':
				if self.get(command[1]) == self.get(command[2]):
					line = command[3] - 2
			line += 1
			command = commands[line]

	def get(self, index):
		index -= 1
		if index < len(self.data):
			return(self.data[index])
		return 0

	def set(self, index, value):
		index -= 1
		while index >= len(self.data):
			self.data.append(0)
		self.data[index] = value

class RegisterProgram(object):

	def __init__(self, commands):
		self.data = commands

	def isStandardForm(self):
		for command in self.data:
			if command[0] == 'J' and self.data[command[3] - 1][0] == 'END':
				return False
		return True

	def concat(self, program):
		assert self.isStandardForm()
		return self.unprotectedConcat(program)

	def unprotectedConcat(self, program):
		p1 = self.data
		p2 = program.data
		p = p1[:len(p1)-1]
		for cmd in p2:
			if cmd[0] == 'J':
				ncmd = cmd[:3]
				ncmd.append(len(p1) - 1 + cmd[3])
				p.append(ncmd)
			else:
				p.append(cmd)
		return RegisterProgram(p)

	def save(self, name):
		program = self.data
		filePath = name + '.urm'
		f = open(filePath, 'w')
		for cmd in program:
			l = str(cmd[0])
			for i in range(1, len(cmd)):
				if i == 1:
					l += '('
				else:
					l += ','
				l += str(cmd[i])
			if len(cmd) > 1:
				l += ')'
			l += '\n'
			f.write(l)
		f.close()
		return filePath

	def roh(self):
		r = 0
		for cmd in self.data:
			if len(cmd) > 1 and cmd[1] > r:
				r = cmd[1]
			if len(cmd) > 2 and cmd[2] > r:
				r = cmd[2]
		return r + 1

	def trans(self, indices, fin_index):
		p = []
		for i in range(0, len(indices)):
			p.append(['T', indices[i], i + 1])
		for i in range(len(indices) + 1, self.roh() + 1):
			p.append(['Z', i])
		p.append(['END'])
		prg = RegisterProgram(p)
		prg = prg.concat(self)
		fin_trans = RegisterProgram([['T', 1, fin_index], ['END']])
		prg = prg.concat(fin_trans)
		return prg



def primRec(F, G, n):
	m = max(n+2, F.roh(), G.roh())
	commands = []
	for i in range(1, n+2):
		commands.append(['T', i, m+i])
	commands.append('END')
	H1 = concat(RegisterProgram(commands), F.trans(range(1, n+1), m+n+3))
	q = len(H1.data)
	H2 = G.trans(range(m+1, m+n+1) + range(m+n+2, m+n+4), m+n+3)
	p = q + len(H2.data) + 2
	H1.data.insert(len(H1.data)-1, ['J', m+n+2, m+n+1, p])
	H = H1.unprotectedConcat(H2)
	H.data.insert(len(H.data)-1, ['S', m+n+2])
	H.data.insert(len(H.data)-1, ['J', 1, 1, q])
	H.data.insert(len(H.data)-1, ['T', m+n+3, 1])
	return H


def compile(filePath):
	f = open(filePath, 'r')
	commands = []
	for line in f:
		line = ''.join(line.split())
		line = line.replace('(', ',')
		line = line.replace(')', '')
		tokens = line.split(',')
		for i in range(0, len(tokens)):
			if tokens[i].isdigit():
				tokens[i] = int(tokens[i])
		commands.append(tokens)
	f.close()
	return RegisterProgram(commands)

def isStandardForm(program):
	return program.isStandardForm()

def concat(p1, p2):
	return p1.concat(p2)

def writeProgram(name):
	filePath = name + ".urm"
	f = open(filePath, 'w')
	line_num = 1
	l = ''
	while l != 'END':
		l = raw_input(str(line_num) + '> ').strip().upper()
		line_num += 1
		f.write(l + '\n')
	f.close()
	return filePath

def saveProgram(program, name):
	return program.save(name)