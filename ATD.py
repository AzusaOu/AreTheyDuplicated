# 2017.02.02 ~ 1st LIVE!
# 2017.02.03 ~ Muti-folder support

# Refer:
# http://blog.csdn.net/u010412949/article/details/8967874

import hashlib
import sys
import os
import shutil
import random

def calculateFileHash(file):
	f = open(file, 'rb')
	content = f.read()
	m = hashlib.md5()
	m.update(content)
	s = m.hexdigest()
	del m
	f.close()
	return s

# [UPDATE] 2017.02.03 - Azuya: Now it can tackle several folders one time.
def sameSearch(folderList):
	print('[Info] Building the list...')
	fileList = {}
	sameList = {}
	strPath = ''
	strHash = ''
	lstPath = []
	for folder in folderList:
		for root, dirs, files in os.walk(folder):
			for file in files:
				try:
					strPath = os.path.join(root, file)
					strHash = calculateFileHash(strPath)
					if strHash in fileList.keys():
						fileList[strHash].append(strPath)
						print('[Find] %s' % strHash)
					else:
						fileList[strHash] = [strPath]
				except:
					print('[Error] Failed in <%s>.' % strPath)
					pass
	print('[Info] Preparing...')
	for key in fileList.keys():
		if len(fileList[key]) > 1:
			sameList[key] = fileList[key]
	# print(fileList)
	return sameList
	# {<hash>:[xxx, xxx, xxx]}

def what2Remove(sameList, cmd, value=''):
	# {<haash>:[xxx, xxx, xxx]}
	delPath = []
	if cmd in ['-l', '--longest']:
		# Baoliu longest path:
		for haash in sameList.keys():
			maxLen = len(sameList[haash][0])
			maxPath = sameList[haash][0]
			for path in sameList[haash]:
				nowLen = len(path)
				if nowLen > maxLen:
					delPath.append(maxPath)
					maxLen = nowLen
					maxPath = path
				elif nowLen < maxLen:
					delPath.append(path)
	elif cmd in ['-s', '--shortest']:
		# Baoliu shortest path:
		for haash in sameList.keys():
			minLen = len(sameList[haash][0])
			minPath = sameList[haash][0]
			for path in sameList[haash]:
				nowLen = len(path)
				if nowLen < minLen:
					delPath.append(minPath)
					minLen = nowLen
					minPath = path
				elif nowLen > minLen:
					delPath.append(path)
	elif cmd in ['-b', '--blacklist']:
		for haash in sameList.keys():
			for path in sameList[haash]:
				if value in path and value != '':
					delPath.append(path)
				elif value == '':
					print('[Warning] Blacklist require a parameter.')
					return []
	# elif cmd in ['-w', '--whitelist']:
	# 	sig = 0
	# 	for haash in sameList.keys():
	# 		for path in sameList[haash]:
	# 			if value in path:
	# 				break
	# 		else:
	# 			sig = 1
	# 		for path in sameList[haash]:
	# 			if (value in path == False) and (value != '') and (sig == 0):
	# 				delPath.append(path)
	# 			elif value == '':
	# 				print('[Warning] Whitelist require a parameter.')
	# 				return []

	for haash in sameList.keys():
		print('\n[%s]' % haash)
		for path in sameList[haash]:
			if path in delPath:
				print(' x- %s' % path)
			else:
				print(' |- %s' % path)
	return delPath

def fileRemove(pathList):
	strTrash = 'TRASH'
	if os.path.isdir(strTrash) == False:
		os.mkdir(strTrash)
	for delPath in pathList:
		try:
			print('[Info] Remove %s' % delPath)
			shutil.move(delPath, os.path.join(strTrash, os.path.basename(delPath)+str(random.randint(0,1000))))
			os.system('echo %s >> %s' % (delPath, os.path.join(strTrash, '###_LOG_###.txt')))
		except:
			print('[Error] Cannot find %s' % delPath)
			pass

def KYMUI2017(strTITLE, strWELCOME, lstSELECT):
	# v1.0: 2017.02.02
	strSplit = ''
	for i in range(len(strTITLE)+6):
		strSplit += '='
	print(strSplit)
	print('|| %s ||' % strTITLE)
	print(strSplit)
	print(strWELCOME)

	# ====== VARS ======
	sameLst = {}
	delLst = []
	# ==================
	while True:
		count = 0
		for i in lstSELECT:
			print('%d - %s' % (count, i))
			count += 1
		choice = int(raw_input('>> Select what to do: '))
		print(' ')

		# ====== Functions ======
# Build the hash list
		if choice == 0:
			folders = []
			strGet = '###'
			while True:
				strGet = raw_input('>> Path: ')
				if strGet == '':
					break
				folders.append(strGet)
			sameLst = sameSearch(folders)

# Filt what to remove
		elif choice == 1:
			par = raw_input('>> [-l| -s| -b| ~]: ')
			val = raw_input('>> Parameter(if have): ')
			delLst = what2Remove(sameLst, par, val)

# Execute remove			
		elif choice == 2:
			par = raw_input('>> Are you sure?(y/n) ')
			if par == 'y':
				fileRemove(delLst)
				# sameLst = {}
				delLst = []
		# ========================

	print(' ')


if __name__ == '__main__':
	functions = ['Build the hash list',
	'Filt what to remove',
	'Execute remove']
	KYMUI2017('Are They Duplicated', 'Azuya - 170203', functions)
