import math
import struct
import matplotlib.pyplot as plt
import pyaudio
import numpy as np
import time

# histogram i entropia bezpośrednio z próbek,
#po processingu wntropia powinna wzrosnąć i histogram się wyrównać

'''
Czas działania i generowania próbek:
Czas potrzebny na wygenerowanie liczb 8 bitowych tylko na podstawie próbek z mikrofonu jest zależne od ustawień
częstotliwości próbkowania mikrofonu i wynosi w moim przypadku 44100 liczb/sekundę
Czas potrzebny na wygenerowanie liczb 8 bitowych na podstawie kilku pierwszych próbek z mikrofonu i przetworzeniu ich
wg podejscia zaprezentowanego w pracy 'A True Random Number Generator Based onHyperchaos and Digital Sound'
wynosi na moim laptopie około 132000 liczb/sekundę
'''

def getAudio(numOfSamples):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100 # 44.1kHz

	p = pyaudio.PyAudio()
	stream = p.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		output=True,
		frames_per_buffer=CHUNK,
		input_device_index=2  # słuchawki usb, musze jawnie zmienic
	)

	counter = 0
	samples = []
	while counter < numOfSamples:
		data = stream.read(CHUNK)  # ::2, by nie było powrotu do zera, brany co drugi element
		data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] + 128
		for i in range(len(data_int)):
			samples.append(data_int[i])
			counter +=1

	return samples

def fT(x, a=1.999999):
	if 0<=x<=0.5:return a*x
	elif 0.5<=x<=1:return a * (1-x)
	return 1 # jak x ma złą wartość, ale taka sytuacji nigdy nie ma miejsca

def swap(string): # dziele stringa na pół i najpierw wchodzi druga połowa odwrócona, a potem pierwsza połowa normalna
	s = len(string)//2
	outputStr = string[:s-1:-1] + string[s-1::-1] # od: do: krok
	return outputStr

def xorStr(str1, str2):
	if len(str1) != len(str2):return False
	outStr = ""
	for d in range(len(str1)):
		if str1[d] == str2[d]: outStr+='0'
		else:outStr +='1'
	return outStr

def TRNG(inputSampleArr, howMany = 100000, startSample = 10000 ):
	N = 256  # wymagane bity TRNG na wyjściu
	L = 8  # CCML size
	A = inputSampleArr[startSample: startSample + L] # tablica z próbkami dźwięku, nie zaczynam od zerowej próbki
	y = L // 2  # wymagana ilość iteracji
	# wiersz oznacza czas t, tutaj poniżej są wartośći początkowe dla t=0
	xArr = [[0.141592, 0.653589, 0.793238, 0.462643, 0.383279, 0.502884, 0.197169, 0.399375]]
	for i in range(1, y + 1):
		xArr.append([0] * 8)  # wypełnienie zerami, by potem płynnie wstawiać i liczyć wartości
	n = (N * L) // ((L // 2) * 64)  # ilość próbek audio (N//32)
	eps = 0.05  # coupling constant
	r = []  # r ^ y - 3bitowa liczba z próbki dźwięku
	for i in range(L):  # tu było n
		mask = 1
		tempNum = 0
		for k in range(3):
			tempNum += A[i] & mask
			mask <<= 1
		r.append(tempNum)  # dodaj 3 bitową liczbę do tablicy r

	c = 0
	t = 0
	output = []

	with open("TRNG32BitNumbers.bin", 'ab') as binFile:
		binFile.truncate(0)  # usunięcie zawartości pliku TRNG32BitNumbers.bin jeśli taka zawartość już jest w tym pliku
		while len(output) < howMany:  # 10sek/100000 liczb
			for i in range(L): # tutaj t=0
				xArr[t][i] = ((0.071428571 * r[i]) + xArr[t][i]) * (2/3)
				c +=1
			for t in range(y): # y=4
				for i in range(L):
					#print("t: ", t, "i: ", i,  "xArr[i][t]: ", xArr[t][i])
					xArr[t+1][i] = ((1-eps) * fT(xArr[t][i])) + ( (eps/2) * ( fT(xArr[t][(i+1)%L] ) + fT(xArr[t][(i-1)%L])))

			zArr = [] # 8 razy 64 bitowe ciągi zer i jedynek trzymane w tej tablicy jako binary string
			binary = ""
			for i in range(L):
				packed = struct.pack('>d', xArr[y-1][i]) # endianess, musi być big endian (>)
				binary = "".join(map(lambda x: format(x, 'b').zfill(8), packed ) )
				zArr.append( binary ) # 2 ostatnie najmniej znaczące bity z reprezentacji floata wchodzą do zArr
				xArr[0][i] = xArr[y-1][i]

			for i in range(L//2 ):
				temp = swap(zArr[i + (L//2)])
				zArr[i] = xorStr(zArr[i], temp )

			for i in range(L//2): # wybierz pierwszą połowe z tablicy zArr po zmianie
				for k in range(8):#do histogramu wchodzą 8 bitowe liczb
					curNumber = zArr[i][k*8: k*8+8]
					output.append(int(curNumber, 2))
				# ale do pliku zapisuje 32 bitowe liczby
				out1 = bytearray(int(binary[x:x+8], 2) for x in range(0, len(binary)//2, 8))
				out2 = bytearray(int(binary[x:x + 8], 2) for x in range(len(binary)//2, len(binary), 8))
				binFile.write(out1) # pierwsze 32 bity liczby 64 bitowej
				binFile.write(out2) # kolejne 32 bity liczby 64 bitowej


	return output

def calcEntropy(arr):# w arr wchodzą liczby
	xxd = {}
	for i in range(len(arr)):
		if xxd.get(arr[i]) is not None:xxd[arr[i]] += 1
		else:xxd[arr[i]] = 1
	suma = 0
	probArr = []  # w probArr wchodzą prawdopodobieństwa
	for key in xxd:
		probArr.append(xxd[key] / len(arr))
	for p in probArr:
		suma +=  -(p * math.log2(p))
	return suma

numOf32BitSamples = 1000000
sourceOutput = getAudio(numOf32BitSamples)
start = time.time()
TRGNOutput = TRNG(sourceOutput, numOf32BitSamples)
print("Entropy only from source: ", calcEntropy(sourceOutput))
print("Entropy after processing: ", calcEntropy(TRGNOutput))
print("time: ", time.time() - start)

fig, (axis1, axis2) = plt.subplots(2)
fig.tight_layout(pad=5.0) # odstęp między wykresami

axis1.hist(sourceOutput, bins=256)
axis1.set_title("Before processing")
axis1.set_xlabel(f"Wartość 8 bitowa, entropia: {calcEntropy(sourceOutput)}")
axis1.set_ylabel("Ilość próbek")

axis2.hist(TRGNOutput, bins=256)
axis2.set_title("After processing")
axis2.set_xlabel(f"Wartość 8 bitowa, entropia: {calcEntropy(TRGNOutput)}")
axis2.set_ylabel("Ilość próbek")

plt.show()








