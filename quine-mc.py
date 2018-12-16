import sys
import itertools	
import numpy as np

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
		n1 = exp.count('1')			# count '1's
		groups[n1].add(exp)
		list_mint.append(exp)			# list of minterms

	return groups

def label_minterm(list_mint):
	""" Return the labels of the minterms
	Args: list of minterms
	"""
	label = []
	for i in range(len(list_mint)):
		lab = bin_dec.get(list_mint[i])
		label.append(lab)

	return label


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
				if(len(groups[i+1]) == 0):
					uncheck.add(term1)
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
	print("Primos Implicantes: "),

	for i in list_imp:
		if(i == list(list_imp)[len(list_imp) - 1]):
			print(bin_lit(i))#,
		else:
			print(bin_lit(i) + ' +'),

def implicant_label(mint):
	""" Return the label of a given minterm
	Args: minterm (ex.: 1101)
	Returns: label (ex.: 13)
	"""
	sum_one = 0
	sum_dc = 0

	dc = []
	imp_label = set()

	for i in range(len(mint)):
		if(mint[i] == '-'):
			dc.append(pow(2,len(mint) - i - 1))
			sum_dc += pow(2,len(mint) - i - 1)
		else:
			sum_one += int(mint[i]) * pow(2,len(mint) - i - 1)

	for i in range(len(dc)):
		imp_label.add(sum_one + dc[i])

	imp_label.add(sum_one)
	imp_label.add(sum_one + sum_dc)

	return imp_label

def list_label_imp(implic_prime):
	""" Return a list of labels from implicant primes
	Args: list of implicant primes
	"""
	list_lab = []
	
	for i in range(len(implic_prime)):
		aux = list(implic_prime)[i]
		list_lab.append(implicant_label(aux))

	return list_lab


def essential_prime(chart):
	""" Find the essential primes in a chart, searching for the columns with an unique '1'
	Args: Chart of implicant primes * minterms
	Returns: list of essential primes
	"""
	prime = set()
	for col in range(len(chart[0])):
		count = 0
		pos = 0
		for row in range(len(chart)):
			if(chart[row][col] == 1):
				count += 1
				pos = row
		if(count == 1):
			prime.add(pos)

	return prime

def print_essential_prime(prime, list_imp):
	""" Print the essential primes in format of minterms
	Args: list of implicant primes and labels of essential primes
	"""
	essential = list(prime)
	count = -1

	aux = []

	for i in (list_imp):
		count += 1
		if(count in essential):
			if(count == list(essential)[len(essential) - 1]):
				print(bin_lit(i) + '\n\t'),
			else:
				print(bin_lit(i) + ' +'),


def petrick_method(chart):
	""" Find the rows with '1' and selects the row containing the biggest quantity of '1's
	Args: Chart of implicant primes * minterms
	Returns: list of indexs from the chart that contains '1' and the row found with the most number of '1's
	"""
	biggest = 0
	aux = 0
	choosen = 0

	P = []
	for row in range(len(chart)):
		p_i = []
		for col in range(len(chart[0])):
			if(chart[row][col] == 1):
				aux = aux +1 
				p_i.append(row)
			if(aux >= biggest):
				biggest = aux
				choosen = row
		aux = 0
		P.append(p_i)


	return P, choosen


def verify_solution(chart):
	""" Verify if the solution was found, i.e., the chart is all empty
	Args: chart
	"""
	count = 0

	for col in range(len(chart[0])):
		for row in range(len(chart)):
			if(chart[row][col] == 1):
				count += 1
				return False

	if(count == 0):
		return True

def delete_covered(chart, delete):
	""" Delete the rows and columns that the are covered by the row passed as argument
	Args: Chart of implicant primes * minterms, and row to be deleted
	"""

	for col in range(len(chart[0])):
		if (chart[delete][col] == 1):
			for row in range(len(chart)):
				chart[row][col] = 0

	return chart


def heuristic(chart, final):
	""" Recursive heuristic to search for the final solution. While the chart is not empty, it searches for the row with the most '1's
	and deletes the rows and columns covered by that row.s
	Args: chart, list of minterms
	Returns: the minterms that are in the final solution

	"""
	if(verify_solution(chart)):
		return final
	
	else:
		P, delete = petrick_method(chart)
		final.add(delete)
		new_chart = delete_covered(chart, delete)
		return heuristic(new_chart, final)

def count_literal(final, implic_prime):
	""" Count the number of literals in the final solution"""

	index = -1
	literals = 0

	for i in (implic_prime):
		index += 1
		if(index in final):
			for j in list(implic_prime)[index]:
				if(j != '-'):
					literals += 1
	
	return literals
	

def main():
	list_mint = []

	eq = open('e.txt', 'r').readline()
	print('Equacao a ser minimizada: ' + eq)

	# first stage
	groups = get_minterms(eq, list_mint)
	

	implic_prime = get_implicant_prime(groups) # implicant primes
	print_implicant_prime(implic_prime)

	lab_mint = label_minterm(list_mint) 	# list of labels of the minterms
	lab_imp = list_label_imp(implic_prime)	# list of labels of implicant primes

	# second stage
   	# make the prime implicant chart
	chart = np.array([[0 for i in range(len(lab_mint))] for i in range(len(implic_prime))])

	linha = -1
	for row in list(lab_imp):
		linha += 1
		for j in range(len(row)):
			for k in range(len(lab_mint)):
				if(list(row)[j] == lab_mint[k]):
					chart[linha][k] = 1

	es_prime = essential_prime(chart)
	final = es_prime 	# list of labels of the essential primes

	# 'remove' (replace 1 -> 0) the rows and columns covered by the essential primes
	for i in range(len(es_prime)):
		for col in range(len(chart[0])):
			if (chart[list(es_prime)[i]][col] == 1):
				for row in range(len(chart)):
					chart[row][col] = 0

	
	print('----------------------------------------')
	print('Solucao Final: \n\t'),
	if(verify_solution(chart)):
		print_essential_prime(final, implic_prime)
	else:
		final = heuristic(chart, final)
		print_essential_prime(final, implic_prime)

	print('Numero de Literais: ' + str(count_literal(final, implic_prime)))

					
if __name__== "__main__":
	main()
