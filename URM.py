import copy

class RegisterMachine(object):

	def __init__(self, seq = []):
		self.data = seq

	def display(self):
		print self.data

	def run(self, program):
		line = 0
		command = program[line]
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
			command = program[line]

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
	return commands

def isStandardForm(program):
	for command in program:
		if command[0] == 'J' and program[command[3] - 1][0] == 'END':
			return False
	return True

def concat(p1, p2):
	p = p1[:len(p1)-1]
	for cmd in p2:
		if cmd[0] == 'J':
			ncmd = cmd[:3]
			ncmd.append(len(p1) - 1 + cmd[3])
			p.append(ncmd)
		else:
			p.append(cmd)
	return p

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