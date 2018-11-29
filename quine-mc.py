import sys

# dictionary of minterms
minterms = {
	"!A!B!C!D": "0000", "!A!B!CD": "0001", "!A!BC!D": "0010", "!A!BCD": "0011",
	"!AB!C!D": "0100", "!AB!CD": "0101", "!ABC!D": "0110", "!ABCD": "0111",
	"A!B!C!D": "1000", "A!B!CD": "1001", "A!BC!D": "1010", "A!BCD": "1011",
	"AB!C!D": "1100", "AB!CD": "1101", "ABC!D": "1110", "ABCD": "1111",
}

bin_dec = {
	"0000": 0, "0001": 1, "0010": 2, "0011": 3,
	"0100": 4, "0101": 5, "0110": 6, "0111":7,
	"1000": 8, "1001": 9, "1010": 10, "1011": 11,
	"1100": 12, "1101": 13, "1110": 14, "1111": 15,
}

def get_minterms(eq, list_mint):
	""" List the minterms of the function and group them by # 1's.
	Args: equation in SOP format.
	Returns: groups of minterms divided by number of 1's.
	"""
	eq = eq.replace(" ", "").replace("*", "").replace("(", "").replace(")", "")
	eq = eq.upper()
	mint = eq.split('+')
	mint[len(mint) - 1] = mint[len(mint) - 1].strip('\n')
	
	groups = [set() for i in range(0, 5)]

	for i in range(len(mint)):
		exp = minterms.get(mint[i]) 		# get minterms
		n1 = exp.count('1')					# count '1's
		groups[n1].add(exp)

		list_mint.append(exp)				# list of minterms

	return groups

def comp_minterms(mint1, mint2):
	""" Compares if there is a unique bit difference in the same position of two minterms
	Args: two minterms to be compared
	Returns: agroupment of two minterms with '-' in the bit changed
	"""
	count = 0
	pos = 0
	for i in range(len(mint1)):
		if(mint1[i] != mint2[i]):
			count += 1
			pos = i
			agroup = mint1[:pos] + "-" + mint1[pos+1:]
	if(count == 1):
		return agroup
	else:
		return False

check = set()
uncheck = set()
label = set()

def get_implicant_prime(groups):
	""" Compares minterms with each other, searching for implicant primes
	Args: groups to be compared
	Returns: implicant primes
	"""
	if(set.union(*groups) == set()):
		imp_prime = uncheck - check
		return imp_prime

	else:
		c = [set() for i in range(len(groups) - 1)]
		for i in range(len(groups) - 1):
			for term1 in groups[i]:
				if(len(groups[i]) == 1):
					uncheck.add(term1)
				#	try:
				#		label.append(bin_dec[term1])
				#	except:
				#		continue
				for term2 in groups[i+1]:
					comp = comp_minterms(term1, term2)
					if(comp!=False):
						c[i].add(comp)
						check.add(term1)
						check.add(term2)
					else:
						uncheck.add(term1)
						uncheck.add(term2)
						try:
							label.add(bin_dec[term2])
							label.add(bin_dec[term1])
						except:
							continue
		return get_implicant_prime(c)

def bin_lit(expression):
	""" Maps the functions in binary to literals
	Args: expression in binary format
	Returns: expression in literal format
	"""
	a, b, c, d = "", "", "", ""
	map_a = {'0': '!A', '1': 'A', '-': ''}
	map_b = {'0': '!B', '1': 'B', '-': ''}
	map_c = {'0': '!C', '1': 'C', '-': ''}
	map_d = {'0': '!D', '1': 'D', '-': ''}

	a = map_a.get(expression[0])
	b = map_b.get(expression[1])
	c = map_c.get(expression[2])
	d = map_d.get(expression[3])

	return (a+b+c+d)

def print_implicant_prime(list_imp):
	""" Print the implicant primes in format of minterms
	Args: list of implicant primes
	"""
	for i in list_imp:
		print(bin_lit(i))


def main():
	list_mint = []
	eq = open('ava.txt', 'r').readline()
	print(eq)
	# first stage
	groups = get_minterms(eq, list_mint)
	
	print(list_mint)

	implic_prime = get_implicant_prime(groups)
	print(implic_prime)
	print_implicant_prime(implic_prime)

if __name__== "__main__":
	main()
