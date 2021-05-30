import math
import matplotlib.pyplot as plt
from scipy.stats import kstest, chisquare, chi2, chi2_contingency, norm, ks_2samp

nums = []
binaryLength = 32
with open("TRNGOutputsBin/SpeakToMicOutput.bin" , "rb") as file: # mój plik z liczbami losowymi
	CHUNK = binaryLength//8 # 4 bajtowe liczby odczytuje
	while True:
		data = file.read(CHUNK)
		if data==b'':break # jak już nic nie ma
		nums.append(int.from_bytes(data, "big") / ((2**32)-1) ) #big endain i konwersja zakresu z uint32 do <0, 1>
howMany = min(1000099, len(nums)) #aktualnie 100000 liczb 32 bitowych, potem 1mln
print("howMany: ", howMany)
no_obs = 10
no_sum = 100
no_num = 100
mean = 0.5 * no_num
rstd = math.sqrt(12)
x = [0.0 for ii in range(no_num)] #0.0, by nie podkreślalo jako warning
y = [0.0 for ii in range(no_num)]
p = [0.0 for ii in range(no_sum)]
pv = [0.0 for ii in range(no_obs)]
curIndex = 0#indeks z tablicy nums (są tam liczby od 0 do 1)
allPVals = []
for i in range(1, no_obs+1):
	for j in range(no_sum):
		suma = 0
		for k in range(no_num):
			y[k] = nums[curIndex]
			suma += y[k]
			curIndex +=1
			#curIndex %=howMany

		for k in range(1, no_num):
			temp = y[k-1]
			y[k-1] = (suma - mean) * rstd # *, czy /
			suma -= temp
			suma += nums[curIndex]
			curIndex +=1
			#curIndex %=howMany

		curIndex +=1 # by przejść do następnego przedziału o szerokości 200
		#curIndex %=howMany
		y[no_num-1] = (suma-mean)*rstd

		x[0] = y[0]/math.sqrt(no_num) # linia 50
		x[1] = -x[0]*(no_num-1)/math.sqrt((2*no_num)-1) + y[1]*math.sqrt(no_num/((2*no_num)-1))
		x[0] = norm.cdf(x[0])
		x[1] = norm.cdf(x[1])

		for k in range(2, no_num):
			a = 2*no_num + 1-k
			b = 2*a - 2# oby poniżej nie było problemów z nawiasami
			x[k] = y[0]/math.sqrt(a*b)  -  math.sqrt( (a-1)/(b+2) ) * y[k-1] + y[k] * math.sqrt(a/b)

		#print("x: ", x)
		p[j] = kstest(x, 'norm', N=no_num).pvalue #parametr N nie ma wpływu, ale niech będzie
	#print(p)
	allPVals.extend(p) # for test purposes only
	pv[i-1] = kstest(p, 'uniform', N=no_num).pvalue

print("pv:  ", pv)

plt.hist(allPVals, bins=10,alpha=1, color='red') # for test purposes only
plt.title("WSZYSTKIE wartości p na podstawie danych z tablicy x w odniesieniu do rozkładu normalnego")

plt.figure()
plt.hist(pv, bins=10,alpha=1, color='red')
plt.title("Wszystkie wartości pv na podstawie danych z tablicy p w odniesieniu do rozkładu jednostajnego")

tmp = kstest(pv, 'uniform', N=no_obs).pvalue
print("Ostateczna wartość tmp na podstawie danych z tablicy pv w odniesieniu do rozkladu jednostajnego: ", tmp) # wtf, pvalue = 0.86


plt.show()



