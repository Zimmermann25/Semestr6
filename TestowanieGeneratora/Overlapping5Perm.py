import math, random, sys
import scipy
import numpy as np
from scipy.stats import kstest, chisquare, chi2, chi2_contingency, norm, ks_2samp
import matplotlib.pyplot as plt

#opcje wypisywania na ekran, by nie obcinało danych z np.array przy jej wypisywaniu, oraz wypełniało cały wiersz
np.set_printoptions(threshold=sys.maxsize, linewidth=1800)

#ta funkcja wylicza ranking liczb podanych w tablicy(jednowymiarowej) wynik to liczba z zakresu 1- factorial(len(arr))
def calculateRank(nums):#tutaj powinno wchodzic 5 cyfr w tablicy, jesli chce zakres 1-120, testowane zarówno z, jak i bez powtórzeń i działa poprawnie
	outputRank = 0
	for i in range(len(nums)):
		curVal = nums[i]
		smallerCounter = 0 # ile liczb po prawej jest mniejszych od aktualnej
		dictArr = {}
		nom = math.factorial(len(nums)-1-i) # ilość liczb znajdujących się po prawej stronie, przykładowo 12137 dla i=0 -> 2137
		denom = 1 # zmienna dla permutacji z powtórzeniami
		for j in range(i, len(nums)): # znajdz mniejsze wartoścci po prawej(rzadko, ale mogą się powtarzać)
			if dictArr.get(nums[j]) is None:dictArr[nums[j]] = 1
			else:
				dictArr[nums[j]] += 1
				if dictArr[nums[j]]>=2:
					denom *= dictArr[nums[j]] # dla permutacji z powtórzeniami
			if nums[j] <curVal:smallerCounter +=1

		#(smallerCounter * nom), nom to aktualna podstawa, smallerCounter to ile liczb mniejszych jest po prawej stronie
		outputRank += (smallerCounter * nom)//denom
		#print(outputRank, "num: ", nom, "denom: ", denom, "app: ", (smallerCounter * nom)//denom)
	return outputRank+1 # +1, by nie liczyło od 0


nums = []
binaryLength = 32

with open("TRNGOutputsBin/SpeakToMicOutput.bin" , "rb") as file: # mój plik z liczbami losowymi
	CHUNK = binaryLength//8 # 4 bajtowe liczby odczytuje
	while True:
		data = file.read(CHUNK)
		if data==b'':break # jak już nic nie ma
		nums.append(int.from_bytes(data, "big")) #big endain
howMany = min(1000000, len(nums)) #aktualnie 100000 liczb 32 bitowych, potem 1mln
print("howMany: ", howMany, "expected average: ", howMany/120)

'''ranksArr1Dim = [ranksArr[i][0] for i in range(len(ranksArr))] #120 wierszy, 1 kolumna
ranksArr2Dim = [[0 for i in range(120)] for j in range(len(ranksArr))] # macierz 120x120, wyrazy w przekątnej głównej
for i in range(120):
	ranksArr2Dim[i][i] = ranksArr1Dim[i] # wpisanie ilości konkretnych rankingów do 2 wymiarowej tablicy(120x120)

print("Wystąpienia rankingów (1 wiersz 120 kolumn): ", ranksArr)
print("Wystąpienia rankingów (120 wierszy, 1 kolumna): ", ranksArr1Dim)
print("Wystąpienia rankingów (120 wierszy, 120 kolumn): ")'''


'''covMatrix = np.cov(ranksArr2Dim) # macierz kowariancji
print("covMatrix: ", covMatrix) # wszystko około -50, oprócz wartości na głównej przekątnej
invCovMatrix = np.linalg.inv(covMatrix)# odwrotność macierzy kowariancji, ma być zależność bliska 0
print("inverse: ", invCovMatrix) # praktycznie wszystko jest około -6 * 10^11, czyli duża ujemna liczba'''

no_trs=1000000
mean = 2 * no_trs / 120 # nie wiem, co to i po co, było w kodzie, to przepisałem
ratio=no_trs*200000

A = [[0 for ii in range(60)] for j in range(60)]
B = [[0 for ii in range(60)] for j in range(60)]
curIndex = 0
with open("TRNGOutputsBin/operm5.cov") as covFile:
	tempArr = covFile.read()
	tempArr = tempArr.split()
	for i in range(60):
		for j in range(i, 60):
			A[j][i] = int(tempArr[curIndex])
			curIndex +=1

	#analogicznie dla B
	for i in range(60):
		for j in range(i, 60):
			B[j][i] = int(tempArr[curIndex])
			curIndex +=1
#koniec odczytu danych

no_tests = 1
x = [0 for i in range(60)]
y = [0 for i in range(60)]
for nn in range(no_tests):#po co niby są 2 testy, jak wewnątrz wszstko się zeruje i wyniki się powtarzają?
	ranksArr = [ 0 for x in range(120)] # 1 wiersz, 120 kolumn, wypełnienie zerami najpierw
	'''for i in range(howMany-5+1): #howMany-5+1
		curRank = calculateRank(nums[i: 5+i]) # obliczanie rankingów i wstawianie do tablicy
		ranksArr[curRank-1] +=1 # -1 bo mam outputRank+1 w calculateRank'''

	for i in range(no_trs+1): #howMany-5+1
		curRank = calculateRank(nums[i: 5+i]) # obliczanie rankingów i wstawianie do tablicy
		ranksArr[curRank-1] +=1 # -1 bo mam outputRank+1 w calculateRank

	chsq = 0
	#print("ranksArr: ", ranksArr)
	for j in range(60):
		x[j] = ranksArr[j] + ranksArr[j+60] - mean #macierz f, to macierz rankingów( u mnie ranksArr)
		y[j] = ranksArr[j] - ranksArr[j+60] #jakie real i po co tu ma być? to są liczby rzeszywiste...

	for j in range(60):
		for k in range(60):
			#print("x[j]: ", x[j], "A[j][k]: ", A[j][k], "x[k]: ", x[k])
			chsq += (x[j] * A[j][k] * x[k]) + (y[j] * B[j][k]*y[k])

	chsq /= ratio

	#chsq:  128.49546854010555 pval:  0.024744222098273316
	print("chsq: ", chsq, "pval: ", 1 - chi2.cdf(chsq, 99)) #0.024, więc blisko 0

#print("x: ", x)

print("ranksArr: ", ranksArr)

plt.hist(ranksArr, bins=120)
plt.title("ilość wystąpien danego rankingu dla 1000000 liczb i 120 indeksów(5!)") #8073, 8635
print(max(ranksArr))
plt.show()



