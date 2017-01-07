from threading import Thread
import sys
import time


class Worker(object):
	"""docstring for """

	def __init__(self, name):
		self.name = str(name)
		self.test = ""

	def __str__(self):
		return self.name




def search(pattern, data, timeout=60):

	result = {
		elapsed: "",
		byte_cnt = "",
		status = ""
		}

	lenPattern = len(pattern)
	start_time = time.time()

	try:
		while True:
			if time.time() - start_time > timeout:
				return {}
				break
			pass







		for k in range(256):
	        skip.append(m)
	    for k in range(m-1):
	        skip[ord(pattern[k])] = m - k - 1
	    skip = tuple(skip)
	    k = m - 1
	    while k < n:
	        j = m - 1
	        i = k
	        while j >= 0 and text[i] == pattern[j]:
	            j -= 1
	            i -= 1
	        if j == -1:
	            offsets.append(i + 1)
	        k += skip[ord(text[k])]

	result[elapced] = time.time() - start_time

	return offsets






def generateWorkers(number):

	newWorkers = []
	for i in range(1, number + 1):
		tempWorker = Worker("worker" + str(i))
		newWorkers.append(tempWorker)
	return newWorkers




Andy = Worker("Andy")

text = "xSdg"
#newfile = open("worker.txt", "w")
# for i in range(1000000):
# 	newfile = open("worker.txt", "a")
# 	newfile.write(text)
# 	newfile.close()


start_time = time.time()
newfile = open("worker.txt", "r")
#newfile.read()
if text in newfile.read():
	elapsed = time.time() - start_time
	print elapsed
elapsed = time.time() - start_time
print elapsed




# workerCluster = generateWorkers(10)
# print workerCluster
# workerCluster[0].test = Search()
# workerCluster[0].test.searchString("xAd", "xAd")
#
#
# for worker in workerCluster:
# 	worker.test = Search()
# 	#worker.test.searchString("xAd", "xAd")
# 	Thread(target=worker.test.searchString, args = ("xAd", "xAd")).start()
#
# for worker in workerCluster:
# 	print worker.test.elapsed, worker.test.status
# syze = 0
# for i in newWorkers:
# 	syze += sys.getsizeof(i)
#
# print syze












# #from Queue import Queue
# from threading import Thread
# import time
# #q = Queue()
#
#
# def lessthan99():
# 	time.sleep(3)
# 	for i in range(99):
# 		print i
#
# def morethan99():
#     for i in range(99, 200):
# 			print i
#
# Thread(target=lessthan99).start()
# Thread(target=morethan99).start()
