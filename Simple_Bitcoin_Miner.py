#!/usr/bin/python
#encoding: utf-8

import sys
from hashlib import sha256

def apply_sha256(text):
	return sha256(text.encode('ascii')).hexdigest() 

def hash_researcher(block_number, transactions, last_hash, number_zeros):
	nonce=0
	while True:
		text = str(block_number)+transactions + last_hash + str(nonce)
		hash_gen = apply_sha256(text)
		if hash_gen.startswith('0'*int(number_zeros)):
			print('\n*** Hash Found: ')
			print('\tnonce: {}'.format(str(nonce)))
			print('\thash: {}\n'.format(hash_gen))
			return nonce,hash_gen
		print('Nonce tested: {}'.format(nonce))
		nonce += 1
		
if __name__ == '__main__':
	try:
		if sys.argv[0] == '-h' or sys.argv[0] == '-help':
			raise Exception	
		
		block_number = sys.argv[1]
		transactions = sys.argv[2]
		last_hash = sys.argv[3]
		number_zeros = sys.argv[4]
		hash_researcher(block_number,transactions,last_hash,number_zeros)
		
	except Exception as e:
		print(e)
		filename = sys.argv[0]
		print(''' 
Simple Bitcoin Miner
			
	usage: python Simple_Bitcoin_Miner.py block_number transactions last_hash number_zeros

	-h, -help: Call this help instruction;

	block_number: \t Number of block that you will miner;
	transaction: \t Reference to transactions already computed; 
	last_hash: \t Hash of the last block in the chain
	number_zeros: \t Number of zeros that currently starts
''')
