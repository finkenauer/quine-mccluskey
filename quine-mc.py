# dictionary of minterms
minterms = {
	"!A!B!C!D": "0000", "!A!B!CD": "0001", "!A!BC!D": "0010", "!A!BCD": "0011",
	"!AB!C!D": "0100", "!AB!CD": "0101", "!ABC!D": "0110", "!ABCD": "0111",
	"A!B!C!D": "1000", "A!B!CD": "1001", "A!BC!D": "1010", "A!BCD": "1011",
	"AB!C!D": "1100", "AB!CD": "1101", "ABC!D": "1110", "ABCD": "1111",
}

bin_dec = {
	0: "0000", 1: "0001", 2: "0010", 3: "0011",
	4: "0100", 5: "0101", 6: "0110", 7: "0111",
	8: "1000", 9: "1001", 10: "1010", 11: "1011",
	12: "1100", 13: "1101", 14: "1110", 15: "1111",
}

def get_minterms(eq, list_mint):
	""" List the minterms of the function and group them by # 1's.
	Args: equation in SOP format.
	Returns: groups of minterms divided by number of 1's.
	"""
	eq = eq.replace(" ", "").replace("*", "")
	eq = eq.upper()
	mint = eq.split('+')

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

def get_implicant_prime(groups):
	if(set.union(*groups) == set()):
		imp_prime = uncheck - check
		print(imp_prime)
		print_implicant_prime(imp_prime)
		return imp_prime

	else:
		c = [set() for i in range(len(groups) - 1)]
		
		for i in range(len(groups) - 1):
			for term1 in groups[i]:
				for term2 in groups[i+1]:
					comp = comp_minterms(term1, term2)
					if(comp!=False):
						c[i].add(comp)
						check.add(term1)
						check.add(term2)
					else:
						uncheck.add(term1)
						uncheck.add(term2)
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
	eq = open('input.txt', 'r').readline()
	
	# first stage
	groups = get_minterms(eq, list_mint)
	get_implicant_prime(groups)
	
	
if __name__== "__main__":
	main()

