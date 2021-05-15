#!/usr/bin/python
# encoding: utf-8

import sys
import time
from hashlib import sha256
import threading
import concurrent.futures


DEBUG = False
NONCEBLOCK_SIZE = 1000000
SLEEPTIME = 0

class ThreadManager():
	run = True
	flag_noncelist = True
	params = {}
	nonceblock_ini = 0
	nonceblock_list = []
	
	
	def __init__(self,block_number, transactions, last_hash, number_zeros):
		self.params = {
			'block_number':str(block_number), 
			'transactions':transactions, 
			'last_hash':last_hash, 
			'number_zeros': number_zeros
		}


	def MiningUnit(self, unit_index):	
		if DEBUG: print('starting thread {}'.format(unit_index))
		params = self.params
		while self.run :		 
			nonce_block = None
			
			if DEBUG: print(' thread {} waiting nonce block'.format(unit_index))
			while not self.flag_noncelist:
				time.sleep(SLEEPTIME)
			
			nonce_block = self.GetNonceBlock()
			self.flag_noncelist = True
			
			for n in nonce_block:
				text = str(params['block_number']) + params['transactions'] + params['last_hash'] + str(n)
				hash_gen = sha256(text.encode('ascii')).hexdigest() 
				if hash_gen.startswith('0'*int(params['number_zeros'])):
					return n,hash_gen
			if DEBUG: print('nonce block {}:{} processed by thread {}'.format(self.nonce_block,self.nonce_block+NONCEBLOCK_SIZE,unit_index))

					
	def NonceFiller(self):
		while self.run :
			aux =[]
			if len(self.nonceblock_list) < 5:
				nonce_block_end = self.nonceblock_ini + NONCEBLOCK_SIZE
				
				for x in range(self.nonceblock_ini,nonce_block_end):
					aux.append(x)
			
				while not self.flag_noncelist:
					time.sleep(SLEEPTIME)
				
				self.flag_noncelist = False
				self.nonceblock_list.append(aux)
				self.nonceblock_ini = nonce_block_end	
				self.flag_noncelist = True
				

	def GetNonceBlock(self):
		while not self.flag_noncelist :
			time.sleep(SLEEPTIME)
		return self.nonceblock_list.pop(0)


	def StartMinering(self):
		aux = []
		for _ in range(6):
			nonce_block_end = self.nonceblock_ini + NONCEBLOCK_SIZE		
			for x in range(self.nonceblock_ini,nonce_block_end):
				aux.append(x)
			self.nonceblock_list.append(aux)
			self.nonceblock_ini = nonce_block_end
			
		nonce_filler = threading.Thread(target=self.NonceFiller)
		nonce_filler.start()
		with concurrent.futures.ThreadPoolExecutor(max_workers=3) as thread_executor:
			mining_units = [thread_executor.submit(self.MiningUnit,x) for x in range(3)]	
						
			for f in concurrent.futures.as_completed(mining_units):
				print('\n*** Hash Found!\n\tnonce: {}\n\thash: {}\n\n'.format(f.result()[0],f.result()[1]))
				self.run = False
				break
				
			thread_executor.shutdown(wait=False)
			#nonce_filler.stop()
		
		
if __name__ == "__main__":
	init = time.perf_counter()
	instance = ThreadManager(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	instance.StartMinering()
	print('Task execution time: {} seconds\n'.format(time.perf_counter() - init))
	sys.exit()
