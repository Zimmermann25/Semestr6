import random, math
import matplotlib.pyplot as plt
from scipy.stats import kstest, chisquare, chi2, chi2_contingency, norm
import numpy as np

def readNumbers(binaryLength =32):
	nums = []
	with open("TRNGOutputsBin/SpeakToMicOutput.bin" , "rb") as file:
		CHUNK = binaryLength//8 # 4 bajtowe liczby odczytuje
		while True:
			data = file.read(CHUNK)
			if data==b'':break # jak już nic nie ma
			nums.append(int.from_bytes(data, "big"))
	return nums

def parkLotTest(nums, binaryLength=32):
	maxVal = (2**binaryLength)-1
	counter = 0
	numOfTrials = 500 #indeksy są potem modulo, więc nie będzie wyjścia poza zakres
	print("lenNums: ", len(nums), "numOfTrials: ", numOfTrials)
	trial = 0
	kArrOutput = []
	while trial < numOfTrials:
		parked = []
		k = 0
		n = 0
		while n < 2*12000:
			curX = (nums[counter]/maxVal)*100 # 99, czy 100 oto jest pytanie
			curY = (nums[counter+1]/maxVal)*100
			isOK = True # czy moge tutaj zaparkować
			for i in range(len(parked)): # sprawdz każdy aktualnie poprawnie zaparkowany samochód
				if abs(parked[i][0] - curX)<=1 and abs(parked[i][1]-curY)<=1:
					isOK = False # nie moge zaparkować
					break

			if isOK: # moge zaparkować
				parked.append([curX, curY])
				k+=1

			n+=2
			#counter +=2
			counter = (counter+2) % len(nums)
		trial +=1
		kArrOutput.append(k)

	average = sum(kArrOutput)/len(kArrOutput) # wartość średnia
	sigma = math.sqrt( sum(map(lambda x: (x-average)**2, kArrOutput)) / len(kArrOutput) )
	print(kArrOutput)
	print("average: ", average)
	print("sigma: ", sigma) # otrzymane p dla 100 znormalizowanych k to KstestResult(statistic=0.15638250560605194, pvalue=0.013315828899908122)

	#wykres po normalizacji
	#normalizedData = [(x - average)/sigma for x in kArrOutput]
	normalizedData = [(x - 3523)/21.9 for x in kArrOutput]
	k0 = kstest( normalizedData, 'norm')
	print("KS: ", k0)
	weights = np.ones_like(kArrOutput) / (len(kArrOutput))
	#p[i-1]=1-Phi(z);

	plt.hist(normalizedData, bins=10,alpha=1, weights=weights)
	return kArrOutput

#readedNums = readNumbers(32)
#parkLotTest(readedNums)

#k = [3535, 3481, 3511, 3551, 3500, 3534, 3516, 3518, 3498, 3490, 3506, 3505, 3510, 3499, 3528, 3509, 3524, 3516, 3516, 3525, 3526, 3539, 3474, 3515, 3514, 3537, 3506, 3526, 3496, 3510, 3521, 3521, 3539, 3510, 3503, 3512, 3490, 3548, 3541, 3489, 3509, 3528, 3500, 3541, 3501, 3494, 3482, 3541, 3543, 3508, 3499, 3548, 3526, 3519, 3492, 3521, 3511, 3554, 3530, 3521, 3508, 3507, 3524, 3515, 3546, 3545, 3531, 3499, 3524, 3527, 3504, 3467, 3538, 3540, 3522, 3535, 3469, 3526, 3531, 3520, 3499, 3499, 3496, 3515, 3505, 3476, 3519, 3555, 3552, 3517, 3503, 3521, 3519, 3513, 3536, 3532, 3454, 3510, 3552, 3499]

#wygenerowane i zapisane wartości k(500), by nie musieć czekać kilku/kilkunastu minut na obliczenia dla dużego zbioru
k500 = [3535, 3481, 3511, 3551, 3500, 3534, 3516, 3518, 3498, 3490, 3506, 3505, 3510, 3499, 3528, 3509, 3524, 3516, 3516, 3525, 3526, 3539, 3474, 3515, 3514, 3537, 3506, 3526, 3496, 3510, 3521, 3521, 3539, 3510, 3503, 3512, 3490, 3548, 3541, 3489, 3509, 3528, 3500, 3541, 3501, 3494, 3482, 3541, 3543, 3508, 3499, 3548, 3526, 3519, 3492, 3521, 3511, 3554, 3530, 3521, 3508, 3507, 3524, 3515, 3546, 3545, 3531, 3499, 3524, 3527, 3504, 3467, 3538, 3540, 3522, 3535, 3469, 3526, 3531, 3520, 3499, 3499, 3496, 3515, 3505, 3476, 3519, 3555, 3552, 3517, 3503, 3521, 3519, 3513, 3536, 3532, 3454, 3510, 3552, 3499, 3574, 3449, 3549, 3537, 3553, 3502, 3502, 3520, 3544, 3515, 3527, 3529, 3585, 3555, 3501, 3494, 3516, 3521, 3521, 3497, 3539, 3530, 3511, 3532, 3527, 3502, 3531, 3511, 3501, 3505, 3518, 3517, 3501, 3499, 3509, 3482, 3555, 3504, 3520, 3534, 3516, 3580, 3530, 3506, 3514, 3539, 3530, 3518, 3503, 3512, 3543, 3520, 3537, 3498, 3505, 3514, 3527, 3534, 3518, 3560, 3525, 3502, 3475, 3483, 3534, 3521, 3509, 3539, 3565, 3525, 3477, 3496, 3525, 3528, 3516, 3535, 3521, 3509, 3501, 3518, 3490, 3483, 3542, 3497, 3501, 3504, 3489, 3510, 3490, 3509, 3527, 3518, 3507, 3493, 3518, 3471, 3534, 3526, 3503, 3535, 3502, 3513, 3543, 3532, 3517, 3512, 3530, 3503, 3534, 3530, 3498, 3540, 3539, 3521, 3493, 3538, 3519, 3541, 3525, 3511, 3490, 3512, 3499, 3519, 3534, 3516, 3535, 3513, 3505, 3532, 3465, 3531, 3538, 3541, 3566, 3496, 3502, 3521, 3503, 3500, 3540, 3496, 3515, 3514, 3526, 3534, 3526, 3530, 3558, 3525, 3555, 3512, 3516, 3534, 3483, 3569, 3494, 3523, 3519, 3498, 3529, 3485, 3536, 3540, 3527, 3509, 3516, 3557, 3533, 3485, 3543, 3522, 3510, 3479, 3504, 3544, 3528, 3522, 3551, 3514, 3495, 3522, 3529, 3514, 3522, 3508, 3507, 3512, 3524, 3532, 3472, 3512, 3530, 3536, 3525, 3506, 3497, 3517, 3452, 3529, 3515, 3503, 3524, 3518, 3516, 3551, 3539, 3502, 3477, 3517, 3525, 3540, 3509, 3518, 3540, 3538, 3521, 3517, 3541, 3519, 3490, 3555, 3547, 3479, 3519, 3515, 3540, 3535, 3536, 3542, 3529, 3571, 3510, 3488, 3495, 3482, 3521, 3534, 3513, 3503, 3502, 3544, 3516, 3549, 3535, 3504, 3511, 3511, 3456, 3511, 3502, 3549, 3498, 3574, 3533, 3546, 3502, 3529, 3507, 3544, 3544, 3516, 3486, 3474, 3530, 3513, 3536, 3531, 3468, 3508, 3525, 3529, 3540, 3503, 3526, 3556, 3523, 3539, 3496, 3496, 3532, 3523, 3516, 3512, 3546, 3539, 3513, 3488, 3513, 3511, 3521, 3476, 3525, 3490, 3508, 3527, 3540, 3531, 3525, 3518, 3519, 3528, 3516, 3521, 3526, 3480, 3492, 3514, 3478, 3519, 3487, 3496, 3497, 3514, 3522, 3542, 3484, 3519, 3514, 3542, 3515, 3545, 3524, 3510, 3527, 3499, 3479, 3524, 3499, 3503, 3548, 3496, 3523, 3525, 3545, 3529, 3512, 3528, 3519, 3498, 3514, 3522, 3522, 3509, 3517, 3511, 3484, 3510, 3504, 3504, 3465, 3542, 3505, 3512, 3502, 3514, 3535, 3496, 3542, 3506, 3547, 3518, 3526, 3533, 3519, 3526, 3481, 3547, 3544, 3512, 3486, 3503, 3517, 3531, 3549, 3533, 3502, 3506, 3529, 3511, 3582, 3516, 3526, 3503, 3547, 3538, 3512, 3523, 3531, 3534, 3500, 3472, 3467, 3501, 3529, 3525, 3540, 3529, 3554, 3547]

'''average:  3517.804
sigma:  21.352601340351946'''
average = sum(k500)/len(k500) # wartość średnia
sigma = math.sqrt( sum(map(lambda x: (x-average)**2, k500)) / len(k500) )
print("average: ", average, "sigma: ", sigma)
weights = np.ones_like(k500) / (len(k500))
normalizedData = [(x - average)/sigma for x in k500]
plt.hist(normalizedData, bins=10,alpha=1, weights=weights)
plt.xlabel("Wartość xi(znormalizowane)")
plt.ylabel("Prawdopodobieństwo wystąpienia")
plt.title("Znormalizowany rozkład prób bezkolizyjnych")
#print("for 100: ", kstest(k, 'norm'))

pvalues = []
for i in range(len(k500)):
	z = (k500[i] - average)/sigma
	pvalues.append(1 - norm.cdf(z)) # dystrybuanta rozkładu normalnego

plt.figure()
weightsKS = np.ones_like(pvalues) / (len(pvalues))
finalPval = kstest(pvalues, 'uniform') # tutaj powinien być rozkład jednostajny, zamiast normalnego
plt.hist(pvalues, bins=10,alpha=1, weights=weightsKS)
plt.title("Empiryczny rozkład wartości p")
plt.xlabel("Wartość p ")
plt.ylabel("Prawdopodobieństwo wystąpienia")

print("finalPvalue: ", finalPval)
plt.show()








