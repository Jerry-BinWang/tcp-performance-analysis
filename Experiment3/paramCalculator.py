import matplotlib.pyplot as plt
import os, sys, collections
import csv

droppedTCP = 0 # total size of dropped tcp packets
packetDropRate = 0 # 

cumulativeThroughputTCP = {} # cumulative tcp thruput over time
cumulativeThroughputCBR = {} # cumulative cbr thruput over time
intervalThroughputTCP = {} # thtoughput in intervals of 1 sec
intervalThroughputCBR = {} # thtoughput in intervals of 1 sec
bandwidthTCP = {}
bandwidthCBR = {}

latency = {} # end-t-end latency for each packet
rttTCP = {} # RTT for each packet
cwind = {} # congestion window size over time
packetDrop = {} # total packet drop over time

avgThroughput = {}
avgPacketdrop = {}
avgLatency = {}
avgRTT = {}
avgBandwidth = {}

def exportToCSV(fileName, dictionary):
	with open(fileName, 'wb') as csvfile:
		writer = csv.writer(csvfile)
		sorted_dict = collections.OrderedDict(sorted(dictionary.items()))
		for key, value in sorted_dict.iteritems():
			writer.writerow([key, value])

def plotDict(plotName, figName, xlabel, ylabel, dictionary1):
	list1 = sorted(dictionary1.items()) # sorted by key, return a list of tuples
	x,y = zip(*list1) # unpack a list of pairs into two tuples
	f = plt.figure(figsize=(5,4))
	plt.plot(x, y)
	plt.title(plotName)
	plt.xlabel(ylabel)
	plt.ylabel(xlabel)
	plt.legend(loc="upper left", prop={'size': 7})
	f.savefig(figName)

def plotDict2(plotName, figName, xlabel, ylabel, dictionary1, dictionary2, dict1, dict2):
	list1 = sorted(dictionary1.items()) # sorted by key, return a list of tuples
	list2 = sorted(dictionary2.items())
	
	x,y = zip(*list1) # unpack a list of pairs into two tuples
	x1,y1 = zip(*list2)
	f = plt.figure(figsize=(5,4))
	plt.plot(x, y, label=dict1)
	plt.plot(x1,y1, label=dict2)
	plt.title(plotName)
	plt.xlabel(ylabel)
	plt.ylabel(xlabel)
	plt.legend(loc="upper center", prop={'size': 7})
	f.savefig(figName)

def plotDict4(plotName, dictionary1, dictionary2, dictionary3, dictionary4):
	list1 = sorted(dictionary1.items()) # sorted by key, return a list of tuples
	list2 = sorted(dictionary2.items())
	list3 = sorted(dictionary3.items())
	list4 = sorted(dictionary4.items())

	x,y = zip(*list1) # unpack a list of pairs into two tuples
	x1,y1 = zip(*list2)
	x2,y2 = zip(*list3)
	x3,y3 = zip(*list4)
	plt.plot(x, y)
	plt.plot(x1,y1)
	plt.plot(x2,y2)
	plt.plot(x3,y3)
	plt.title(plotName)
	figName = plotName + '.png'
	plt.savefig(figName)

def calculate_throughput(traceFile):
	global cwind, droppedTCP
	global cumulativeThroughputTCP, cumulativeThroughputCBR, intervalThroughputTCP, intervalThroughputCBR
	global bandwidthTCP, bandwidthCBR
	with open(traceFile, "r") as f:
		dataReceivedTCP = 0
		dataReceivedCBR = 0
		tcp_limiter = 0
		cbr_limiter = 0
		for line in f:
			splitLine = line.split(" ")
			if(splitLine[0] == "r" and splitLine[3] == "3" and splitLine[4] == "tcp"):
				dataReceivedTCP += int(splitLine[5])
				if tcp_limiter%60 == 0:
					cumulativeThroughputTCP[float(splitLine[1])] = ((dataReceivedTCP/float(splitLine[1]))/1000)
					bandwidthTCP[float(splitLine[1])] = (((dataReceivedTCP + droppedTCP)/float(splitLine[1]))/1000)
				intervalThroughputTCP[int(float(splitLine[1]))] = dataReceivedTCP/1000
				tcp_limiter += 1

			elif(splitLine[0] == "r" and splitLine[3] == "5" and splitLine[4] == "cbr"):
				dataReceivedCBR += int(splitLine[5])
				if cbr_limiter%10 == 0:
					cumulativeThroughputCBR[float(splitLine[1])] = ((dataReceivedCBR/float(splitLine[1]))/1000)
					bandwidthCBR[float(splitLine[1])] = (((dataReceivedCBR)/float(splitLine[1]))/1000)
				intervalThroughputCBR[int(float(splitLine[1]))] = dataReceivedCBR/1000
				cbr_limiter += 1

			elif(splitLine[0] == "d" and splitLine[4] == "tcp"):
				droppedTCP += ((int(splitLine[5]))/1000)
				packetDrop[float(splitLine[1])] = droppedTCP/(float(splitLine[1]))
			
			elif("cwnd_" in splitLine):
				cwind[float(splitLine[0])] = float(splitLine[splitLine.index('cwnd_')+1])
	
def calculate_latency(traceFile):
	latencyData = {}
	with open(traceFile, "r") as f:
		for line in f:
			splitLine = line.split(" ")
			if (splitLine[4] == "tcp"):
				if(splitLine[2] == "0" and splitLine[0] == "+"):
					# packet sent from n0
					latencyData[int(splitLine[10])]=float(splitLine[1])
				elif(splitLine[3] == "3" and splitLine[0] == "r"):
					# packet received at n3
					if(latencyData.has_key(int(splitLine[10]))):
						latency[int(splitLine[10])]=(float(splitLine[1])-latencyData[int(splitLine[10])])
						del latencyData[int(splitLine[10])]

def calculate_rtt(traceFile):
	global rttTCP
	rtt_dict = {}
	delAck = 0
	with open(traceFile, "r") as f:
		for line in f:
			line = line.strip()
			tokens = line.split(' ')
			if tokens[0] == "+":
				if tokens[2] == "0" and tokens[4] == "tcp":
					rtt_dict[int(tokens[10])] = {"tcp": float(tokens[1])}
			if tokens[0] == "r":
				if tokens[3] == "0" and tokens[4] == "ack":
					if int(tokens[10]) in rtt_dict.keys():
						rtt_dict[int(tokens[10])]["ack"] = float(tokens[1])
					else:
						rtt_dict[int(tokens[10])] = {"ack": float(tokens[1])}
	rtttcp = collections.OrderedDict(sorted(rtt_dict.items()))
	for i in range(len(rtttcp)):
		if rtttcp[i].get('ack') == None:
			delAck += 1
			continue
		else:
			for j in range(delAck+1):
				rtttcp[i-delAck+j]= (rtttcp[i].get('ack') - rtttcp[i-delAck+j].get('tcp'))
			delAck = 0
	rttTCP = rtttcp

def calculateAvg(queueDisciplines):
	global rttTCP, cumulativeThroughputTCP, latency, intervalThroughputTCP, intervalThroughputCBR
	global packetDrop, cwind
	temp = {}
	for queueDiscipline in queueDisciplines:
		path = "exp3/"+queueDiscipline
		for file in os.listdir(path):
			cwind = {}
			rttTCP = {} 
			cumulativeThroughputTCP = {} 
			latency = {}
			intervalThroughputTCP = {}
			intervalThroughputCBR = {}
			if file.endswith(".tr"):
				filepath = path + '/' + file
				totalLatency = 0
				totalRTT = 0
				tcpVariant = file.split('-')[1]
				
				calculate_throughput(filepath)
				calculate_latency(filepath)
				calculate_rtt(filepath)
				
				avgThr = (cumulativeThroughputTCP[cumulativeThroughputTCP.keys()[-1]])
				avgThroughput[tcpVariant] = {queueDiscipline: avgThr}
				
				for i in range(len(latency)):
					totalLatency += latency[i]
				avgLat = (totalLatency/latency.keys()[-1])
				avgLatency[tcpVariant] = {queueDiscipline: avgLat}

				for key, value in rttTCP.iteritems():
					totalRTT += value
				avgrtt = (totalRTT/rttTCP.keys()[-1])
				avgRTT[tcpVariant] = {queueDiscipline: avgrtt}

				avg_packetdrop = packetDrop[packetDrop.keys()[-1]]
				avgPacketdrop[tcpVariant] = {queueDiscipline: avg_packetdrop}

			# PLOTS
				plotName = "tcp_cbr_cumul_"+tcpVariant+'_'+queueDiscipline
				figName = "tcp_cbr_cumul_3mb_"+tcpVariant+'_'+queueDiscipline+'.pdf'
				plotDict2(plotName, figName, "Throughput(kbps)", "Time(seconds)",cumulativeThroughputTCP, cumulativeThroughputCBR, "TCP", "CBR")
				# plotName = "tcp_latency_"+tcpVariant+'_'+queueDiscipline
				# plotDict(plotName, "", "Sequence Number", packetDrop)
				# plotName = "Packetdrop "+tcpVariant+'_'+queueDiscipline
				# figName = "tcp_packetdrop_"+tcpVariant+'_'+queueDiscipline+'.pdf'
				# plotDict(plotName, figName, "Packetdrop Rate (kbps)", "Time (seconds)", packetDrop)
				# plotName = "tcp_cwind_"+tcpVariant+'_'+queueDiscipline
				# figName = 'tcp_cwind_'+tcpVariant+'_'+queueDiscipline+'.pdf'
				# plotDict(plotName, figName, "Congestion Window", "Time (seconds)", cwind)
				# plotName = "tcp_cbr_bandwidth_"+tcpVariant+'_'+queueDiscipline
				# plotDict2(plotName, "Bandwidth Consumption/Time Window", "Time (seconds)", intervalThroughputTCP, intervalThroughputCBR)
				if not temp:
					temp = latency
		plotName = queueDiscipline+" cumulative throughput TCP"
		figName = queueDiscipline+"_cumul_thrpt.pdf"
		plotDict2(plotName, figName, "Throughput(kbps)", "Time (seconds)", latency, temp, "Sack", "Reno")
		# print "Average round trip time: ", avgRTT
		# print "Average latency per packet: ", avgLatency
		# print "Average throughput over full expertiment(kbps): ", avgThroughput
		# print "Average packet drop rate is: ", avgPacketdrop

def plotForTCPvariant(tcpVariant, queueDisciplines):
	global rttTCP, cumulativeThroughputTCP, latency, intervalThroughputTCP, intervalThroughputCBR
	global packetDrop, cwind
	temp = {}
	for queueDiscipline in queueDisciplines:
		path = "exp3/"+queueDiscipline
		for file in os.listdir(path):
			if tcpVariant in file:
				filepath = path + '/' + file
				calculate_throughput(filepath)
				calculate_latency(filepath)
				calculate_rtt(filepath)
				if not temp:
					temp = rttTCP
					rttTCP = {}
	plotName = tcpVariant+" RTT"
	figName = tcpVariant+"_rtt.pdf"
	plotDict2(plotName, figName, "RTT(sec)", "Sequence Number", rttTCP, temp, "DropTail", "RED")

def calculateAvgOverQueue(queueDisciplines):
	global rttTCP, cumulativeThroughputTCP, latency, intervalThroughputTCP, intervalThroughputCBR
	global packetDrop, cwind
	temp = {}
	for queueDiscipline in queueDisciplines:
		path = "exp3/"+queueDiscipline
		for file in os.listdir(path):
			cwind = {}
			rttTCP = {} 
			cumulativeThroughputTCP = {} 
			latency = {}
			intervalThroughputTCP = {}
			intervalThroughputCBR = {}
			if file.endswith(".tr"):
				pass

queueDisciplines = ["RED", "DropTail"]
tcpVariants = ["reno", "sack"]
calculateAvg(queueDisciplines)
# plotForTCPvariant("reno", queueDisciplines)

# fileName_tcp_cumul_thru = str(queueDiscipline)+"_"+str(tcpVariant)+"_tcp_cumul_throughput.csv"

# fileName_tcp_latency = str(queueDiscipline)+"_"+str(tcpVariant)+"_tcp_latency.csv"
# fileName_tcp_rtt = str(queueDiscipline)+"_"+str(tcpVariant)+"_tcp_rtt.csv"
# fileName_tcp_intervals = str(queueDiscipline)+"_"+str(tcpVariant)+"_tcp_throughput_intervals.csv"

# fileName_cbr_cumul_throughput = str(queueDiscipline)+"_"+str(tcpVariant)+"_cbr_cumul_throughput.csv"
# fileName_cbr_intervals = str(queueDiscipline)+"_"+str(tcpVariant)+"_cbr_throughput_intervals.csv"

# fileName_cwind = str(queueDiscipline)+"_"+str(tcpVariant)+"_tcp_congestion_window.csv"
# fileName_packetDrop = str(queueDiscipline)+"_"+str(tcpVariant)+"_tcp_packetdrop.csv"

# exportToCSV(fileName_tcp_cumul_thru, cumulativeThroughputTCP)
# exportToCSV(fileName_cbr_cumul_throughput, cumulativeThroughputCBR)
# exportToCSV(fileName_tcp_latency, latency)
# exportToCSV(fileName_tcp_rtt, rttTCP)
# exportToCSV(fileName_tcp_intervals, intervalThroughputTCP)
# exportToCSV(fileName_cbr_intervals, intervalThroughputCBR)
# exportToCSV(fileName_cwind, cwind)
# exportToCSV(fileName_packetDrop, packetDrop)