#!/usr/bin/python
# encoding: utf-8

import sys
import time
from hashlib import sha256
import concurrent.futures


NONCEBLOCK_SIZE = 1000000
SLEEPTIME = 1.5
MAX_WORKER = 2

class BitcoinMiner():
	run = True
	nonceblock_ini = 0
	
	def __init__(self,block_number, transactions, last_hash, number_zeros):
		self.params = {
			'block_number':str(block_number), 
			'transactions':transactions, 
			'last_hash':last_hash, 
			'number_zeros': number_zeros}


	def MiningUnit(self, unit_index, nonce_block):			
		for n in nonce_block:
			if self.run : 
				hash_gen = sha256((self.params['block_number']+self.params['transactions']+self.params['last_hash']+str(n)).encode('ascii')).hexdigest() 
				if hash_gen.startswith('0'*int(self.params['number_zeros'])):
					print('\n*** Hash Found!\n\tnonce: {}\n\thash: {}\n\n'.format(n,hash_gen))
					self.run = False
		nonce_block = None
			

	def StartMinering(self):
		with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as thread_executor:
			thread_index = 1
			nonceblock = []
			mining_units = []
			while self.run:
				nonceblock_end = self.nonceblock_ini + NONCEBLOCK_SIZE		
				nonceblock = list(range(self.nonceblock_ini,nonceblock_end))
				while len(mining_units) == MAX_WORKER:
					time.sleep(SLEEPTIME)
					for f in concurrent.futures.as_completed(mining_units):
						mining_units.remove(f)
				if not self.run: 
					thread_executor.shutdown(wait=False)
					break
				mining_units.append( thread_executor.submit(self.MiningUnit,thread_index,nonceblock) )	
				self.nonceblock_ini = nonceblock_end
				thread_index+=1	
								
		
if __name__ == "__main__":
	init = time.perf_counter()
	instance = BitcoinMiner(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	instance.StartMinering()
	print('Task execution time: {} seconds\n'.format(time.perf_counter() - init))
	sys.exit()
