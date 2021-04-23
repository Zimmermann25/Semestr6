import struct, time, os

def userFilePathsInput():
	#część na wprowadzanie danych
	myFilePath = input("Podaj ścieżkę pliku / nazwę pliku w tym samym folderze. Wciśnij enter jeśli plik o domyślnej nazwie "
					   "example_new.ts jest w tym samym folderze co uruchamiany plik\n") or 'example_new.ts'
	tempPath = os.path.join(os.getcwd(), myFilePath) # jak podana będzie tylko nazwa.ts
	while not os.path.exists(os.path.dirname(myFilePath)) and (not os.path.exists(tempPath)  ) or (not myFilePath.endswith(".ts")) :
		myFilePath = input("Podaj poprawną ścieżkę pliku z rozszerzeniem .ts\n")
		tempPath = os.path.join(os.getcwd(), myFilePath) # jak podana będzie tylko nazwa.ts

	#podanie poprawnej ścieżki zapisu audio
	audioOutputPath = input("Podaj ścieżkę zapisu pliku audio / nazwę zapisywanego pliku audio w tym samym folderze z rozsze"
							"rzeniem .mp2 . Wciśnij enter jeśli chcesz domyślną nazwę PID136Output.mp2 \n") or 'PID136Output.mp2'
	if not audioOutputPath.endswith(".mp2"):audioOutputPath += ".mp2"
	tempPath = os.path.join(os.getcwd(), audioOutputPath) # jeśli podana będzie tylko nazwa, bez ścieżki
	while (not os.path.exists(os.path.dirname(audioOutputPath)) ) and ( not os.path.exists(os.path.dirname(tempPath)) ): # dopóki zła ścieżka zapisu
		audioOutputPath = input("Podaj poprawną ścieżkę zapisu pliku audio / nazwę zapisywanego pliku audio w tym samym folderze z rozszerzeniem .mp2 .\n")
		if not audioOutputPath.endswith(".mp2"):audioOutputPath += ".mp2"
		tempPath = os.path.join(os.getcwd(), audioOutputPath)


	#podanie poprawnej ścieżki zapisu video
	videoOutputPath = input("Podaj ścieżkę zapisu pliku video / nazwę zapisywanego pliku video w tym samym folderze z rozsze"
							"rzeniem .264 . Wciśnij enter jeśli chcesz domyślną nazwę PID174Output.264\n") or 'PID174Output.264'
	if not videoOutputPath.endswith(".264"):videoOutputPath += ".264"
	tempPath = os.path.join(os.getcwd(), videoOutputPath)
	while (not os.path.exists(os.path.dirname(audioOutputPath)) ) and ( not os.path.exists(os.path.dirname(tempPath)) ): # dopóki zła ścieżka zapisu
		videoOutputPath = input("Podaj poprawną ścieżkę zapisu pliku video / nazwę zapisywanego pliku video w tym samym folderze z rozszerzeniem .264 .\n")
		if not videoOutputPath.endswith(".264"):videoOutputPath += ".264"
		tempPath = os.path.join(os.getcwd(), videoOutputPath)

	#wybór poprawnej opcji
	choice = input(
"""Wybierz opcję:
1. Wypisanie danych o pakietach, zapis audio i video do plików.
2. Zapis danych o pakietach do pliku txt(bez wypisywania), zapis audio i video do plików.
3. Tylko zapis audio i video do plików, bez wypisywania i zapisywania danych o pakietach(domyślne)\n""") or '3'

	while (not choice.isdigit()) or (choice not in [ '1','2','3' ]):
		print("Nie ma takiej opcji.")
		choice = input(
"""Wybierz opcję:
1. Wypisanie danych o pakietach, zapis audio i video do plików.
2. Zapis danych o pakietach do pliku txt(bez wypisywania), zapis audio i video do plików.
3. Tylko zapis audio i video do plików, bez wypisywania i zapisywania danych o pakietach\n""")
	choice = int(choice)

	txtOutputPath = ""
	if choice==2:
		txtOutputPath = input("Podaj ścieżkę zapisu pliku z informacjami o pakietach z rozszerzeniem .txt (domyślnie PacketInfo.txt)\n") or "PacketInfo.txt"
		if not txtOutputPath.endswith(".txt"): txtOutputPath += ".txt"
		tempPath = os.path.join(os.getcwd(), txtOutputPath)
		while (not os.path.exists(os.path.dirname(txtOutputPath)) ) and ( not os.path.exists(os.path.dirname(tempPath))): # dopóki zła ścieżka zapisu
			txtOutputPath = input("Podaj poprawną ścieżkę zapisu pliku z informacjami o pakietach z rozszerzeniem .txt\n")
			if not txtOutputPath.endswith(".txt"): txtOutputPath += ".txt"
			tempPath = os.path.join(os.getcwd(), txtOutputPath)

	return myFilePath, audioOutputPath, videoOutputPath, txtOutputPath, choice


#deklaracja zmiennych i wartosc i poczatkowe
myFilePath, audioOutputPath, videoOutputPath, txtOutputPath, choice = userFilePathsInput()
#print("Podane ściezki: ", myFilePath, audioOutputPath, videoOutputPath, txtOutputPath, choice)
CHUNK = 188 # 188 bajtów = 1504 bity
TS_PacketId = 0
CCCheck136 = 0
CCCheck174 = 0
curPESSize = 0 # do kroku 3
PESHeaderDataLength = 0# do kroku 3 i 4
extensionLen = 0
headLen = 0
outputPESAudio = b""
outputPESVideo = b""
start = time.time() # całkowity czas po podaniu danych

print("Working...")
with open(audioOutputPath, 'ab+') as PID136Output, open(videoOutputPath, "ab+") as PID174Output:
	PID136Output.truncate(0) #usunięcie zawartości pliku optimOutput.mp2 jeśli taka zawartość już jest w tym pliku
	PID174Output.truncate(0) #usunięcie zawartości pliku PID174Output.264 jeśli taka zawartość już jest w tym pliku
	if choice==2: # musze zrobić standardowo bez with, i potem ręcznie zamknąć ze względu na ifa
		txtFile = open(txtOutputPath, "a")
		txtFile.truncate(0)
	with open(myFilePath, "rb") as inputFile:
		while True:
			outputLine = ""
			curPacket = inputFile.read(CHUNK)
			if curPacket ==b'':break # jak dojdzie do końca pliku, to break, by wyjść z pętli while
			data = list(struct.unpack(f'>{188}B', curPacket)) # 1 bajt unsigned char, > oznacza odczyt danych big endian(taki format pliku)
			#każdą szestastkową 8 bitową wartość nagłówka rzutuj na ciąg 0 i 1 typu string

			#data[:4] - tablica z pierwszymi 4 wartościami z tablicy data
			#format(x, 'b') - rzutuj wartość x(8bitową) na wartość binarną(zera i jedynki)
			#.zfill(8) oznacza dopełnienie zerami z lewej jeśli jest zbyt krótki ciąg, bo python obcina zera wiodące w repr. binarnej
			#przykład: wartość 15 normalnie na ośmiu bitach: 00001111, wartość 15 zapisana binarnie w pythonie: 1111
			#map(lambda x: format(x, 'b').zfill(8), data[:4])
			#map - dla każdej wartości x z podanej tablicy(data[:4]) wykonaj funkcje(lambda to funkcja "anonimowa"),
			#której zawartość to format(x, 'b').zfill(8), map zwraca generator object
			#"".join(someObject) - zawartość obiektu/generatora zapisz do zmiennej typu string, gdzie "" oznacza przerwę
			#pomiędzy kolejno dopisywanymi wartościami(a konkretniej w tym przypadku jej brak)
			binHeader = "".join(map(lambda x: format(x, 'b').zfill(8), data[:4])) # w tej linii *był największy nakład obliczeń
			SB = int(binHeader[0:8], 2)
			E = binHeader[8]
			S = int(binHeader[9], 2) #Start, pierwszy pakiet zawierajacy coś nowego
			P = binHeader[10]
			PID = int(binHeader[11:24], 2)
			TSC = int(binHeader[24:26], 2)
			AF = int(binHeader[26:28], 2)
			CC = int(binHeader[28:32], 2)
			if choice==1 or choice==2: # jeśli bez wypisywania/zapisywania danych o pakietach, to nie potrzebuje tego
				TSPacketLine = f"PacketId: {TS_PacketId:08} SB: {SB} E: {E} S: {S} P: {P} PID: {PID} TSC: {TSC} AF: {AF} CC: {CC}"
				if PID==136:
					if S==1:
						CC=0
						CCCheck136 = 0
						extensionLen = 0
						TSPacketLine+= " Started"
					elif CC==15 and CCCheck136==15:TSPacketLine += " Finished"
					elif S==0 and CC==CCCheck136:TSPacketLine += " Continue"
					elif S==0 and CC !=CCCheck136:
						TSPacketLine += " CC ERROR"
						CCCheck136 = CC
					CCCheck136 +=1

				elif PID==174:
					if S==1:
						CC=0
						CCCheck174 = 0
						extensionLen = 0
						TSPacketLine += " Started"
					elif CC==15 and CCCheck174==15:TSPacketLine += " Finished"
					elif S==0 and CC==CCCheck174:TSPacketLine += " Continue"
					elif S==0 and CC !=CCCheck174:
						TSPacketLine += " CC ERROR"
						CCCheck174=CC
					CCCheck174 +=1

			AFOffset = 0
			if AF > 1:  # 0<=AF<=3, dlatego AF> 1 albo AF=2 or AF=3
				#AF=2 - tylko pole AF, AF=3 - pole AF i jakies dodatkowe dane
				AFLData = "".join(map(lambda x: format(x, 'b').zfill(8), data[4:6]))  # 8 bitów
				AFLLength = int(AFLData[:8], 2)
				if AFLLength > 0:	#Dla bezpieczenstwa
					DC = AFLData[8]
					RA = int(AFLData[9],2)
					SP = AFLData[10]
					PR = int(AFLData[11], 2) # flaga PCR
					OR = int(AFLData[12], 2) # flaga OPCR
					SPFlag = AFLData[13]
					TP = AFLData[14]
					EX = AFLData[15]
					AFOffset = 1+ AFLLength
					StuffingLen = AFLLength-1

					# pola opcjonalne,  parsuje tylko pcr i opcr
					startByte = 6 # moze wystąpić jedno, albo oba
					PCRVal = OPCRVal = 0
					PCRLine = ""
					if PR:
						PCRData = "".join(map(lambda x: format(x, 'b').zfill(8), data[startByte:startByte+6]))
						PCRBase = int(PCRData[:33], 2)
						PCRReserved = int(PCRData[33:39], 2)
						PCRExtension = int(PCRData[39:48], 2)
						PCRVal = PCRBase * 300 + PCRExtension  # 300 -> xTS.BaseToExtendedClockMultiplier = 300
						if S==1 and (choice==1 or choice==2): PCRLine += f" PCR:{PCRVal}"
						startByte +=6
						StuffingLen -=6
					if OR:
						OPCRData = "".join(map(lambda x: format(x, 'b').zfill(8), data[startByte:startByte+6]))
						OPCRBase = int(OPCRData[:33], 2)
						OPCRReserved = int(OPCRData[33:39], 2)
						OPCRExtension = int(OPCRData[39:48], 2)
						OPCRVal = OPCRBase * 300 + OPCRExtension  # 300 -> xTS.BaseToExtendedClockMultiplier = 300
						if S==1 and (choice==1 or choice==2): PCRLine += f" OPCR:{OPCRVal}"
						StuffingLen -=6
						startByte +=6
					#dalszej części chyba nie potrzebuje aktualnie (str 41 w itu)
					if choice==1 or choice==2:
						AFLine = f' AF part-> L: {AFLLength} DC: {DC} RA: {RA} SP: {SP} PR: {PR} OR: {OR} SPFlag: {SPFlag} TP: {TP} EX: {EX} Stuffing: {StuffingLen}'

			PESpacket = b"" # dane z pakietu, które będą zapisane do pliku
			if PID==136 or PID==174:  #136 fonia, 174 wizja
				if AF==0 or AF==1:
					PESpacket += curPacket[4:] # brak AF, najprostrzy przypadek, wchodzi tylko payload
				else: # jest AF, trzeba znać jego długość, tutaj payloadu może nawet nie być
					PESpacket += curPacket[4 + AFOffset:] # było AFOffset

				PESHeaderStr = "".join(map(lambda x: format(x, 'b').zfill(8), PESpacket[:9]))
				if len(PESHeaderStr)< 72: pass # 8*9 # za mało danych, coś nie tak
				else:
					# nie potrzebuje ich wszystkich, ale niech już zostaną
					PSCP = int(PESHeaderStr[:24], 2) # packet start code prefix, powinno byc 0x000001
					StreamID = int(PESHeaderStr[24:32], 2)
					PES_packet_length = int(PESHeaderStr[32:48], 2) # bajt 4 i 5
					Byte6_7and6 = PESHeaderStr[48:50]
					PESScramblingControl = PESHeaderStr[50:52]
					PES_priority = PESHeaderStr[52]
					DataAlignIndicator = PESHeaderStr[53]
					Copyright = PESHeaderStr[54]
					OriginalOrCopy = PESHeaderStr[55]
					PTS_DTS = PESHeaderStr[56:58]
					ESCR = PESHeaderStr[58]
					ESRate = PESHeaderStr[59]
					DSMTrickMode = PESHeaderStr[60]
					AdditionalCopyInfo = PESHeaderStr[61]
					PES_CRC = PESHeaderStr[62]
					PESExtension = PESHeaderStr[63]
					PESHeaderDataLength = int(PESHeaderStr[64:72], 2)

					if choice==1 or choice==2: PESLine = f' PES part->  PSCP: {PSCP}, StreamID: {StreamID}, PES_packet_length: {PES_packet_length}'
					if PTS_DTS == '00':pass #print("brak PTS i DTS") # PTS tylko dla fonii, oba dla wizji
					elif PTS_DTS == '01':pass#print("Forbidden")
					elif PTS_DTS == '10': # 5 bajtów dodatkowo(jest tylko PTS, czyli fonia)
						'''README: markery w pakiecie 3(i pewnie innych też) nie są samymi 1, ale wartość PTS pokrywa się z tą na 
							slajdzie(32911615). Nie wiem dlaczego jest poprawnie od 5+PESHeaderDataLength. W mojej ocenie powinno być 
							6+PESHeaderDataLength, bo 6Bajtów zajmuje nagłówek PES(podstawowy), prawdopodobnie spowodowane
							jest to linią AFOffset = 1+AFLLength, albo PESHeaderDataLength dziwnie liczy
							W każdym razie coś powoduje przesunięcie o 1 bajt w stosunku do poprawnego PTS. Analogicznie dla PTS_DTS=11'''
						PTS_DTSData = "".join(map(lambda x: format(x, 'b').zfill(8), PESpacket[5+PESHeaderDataLength:10+PESHeaderDataLength]))
						if len(PTS_DTSData) < 40:pass#print(curLine) # za mało danych, czyli coś nie tak
						else:
							PTS0010 = PTS_DTSData[:4]
							PTS3230 = PTS_DTSData[4:7]
							marker1 = PTS_DTSData[7]
							PTS2915 = PTS_DTSData[8:23]
							marker2 = PTS_DTSData[23]
							PTS140 = PTS_DTSData[24:39]
							marker3 = PTS_DTSData[39]
							PTSTemp = PTS3230 + PTS2915 + PTS140
							PTSFull = int(PTSTemp, 2)
							#90000 = 90kHz zegara, .6f to dokładność do 6 miejsc po przecinku
							if choice==1 or choice==2:
								if PCRLine: PESLine+= PCRLine # pcr i opcr jesli występują
								PESLine += f" PTS: {PTSFull}, (Time={PTSFull/90000 :.6f}s)"
					elif PTS_DTS == '11':
						PTS_DTSData = "".join(map(lambda x: format(x, 'b').zfill(8), PESpacket[5+PESHeaderDataLength:15+PESHeaderDataLength]))
						if len(PTS_DTSData) < 80:pass #print(curLine) # za mała długość oznacza błąd
						else:
							PTS0011 = PTS_DTSData[:4]
							PTS3230 = PTS_DTSData[4:7]
							marker1 = PTS_DTSData[7]
							PTS2915 = PTS_DTSData[8:23]
							marker2 = PTS_DTSData[23]
							PTS140 = PTS_DTSData[24:39]
							marker3 = PTS_DTSData[39]

							DTS0001 = PTS_DTSData[40:44]
							DTS3230 = PTS_DTSData[44:47]
							marker4 = PTS_DTSData[47]
							DTS2915 = PTS_DTSData[48:63]
							marker5 = PTS_DTSData[63]
							DTS140 = PTS_DTSData[64:79]
							marker6 = PTS_DTSData[79]

							PTSTemp = PTS3230 + PTS2915 + PTS140 # postać binarna
							DTSTemp = DTS3230 + DTS2915 + DTS140
							PTSFull = int(PTSTemp, 2) # postać dziesiętna
							DTSFull = int(DTSTemp, 2)
							if choice==1 or choice==2:
								if PCRLine: PESLine+= PCRLine # pcr i opcr jesli występują
								PESLine += f" PTS: {PTSFull}, DTS: {DTSFull} (Time={PCRVal/27000000 :.6f}s)"
						#print("markers: ", marker1, marker2, marker3, marker4, marker5, marker6)

				#trzeba sprawdzić StreamID, dla 0xBD(189), 0xC0(192) - 0xDF(223), 0xE0(224) - 0xEF(255) jest 3bajtowe extension a w nim m.in PTS i DTS
				forbiddenStreamId = [188, 190, 191, 240, 241, 255, 242, 248]
				#if StreamID==189 or 192<=StreamID<=223 or 224<=StreamID<=255: # tu dać warunki z 6 minuty
				if StreamID not in forbiddenStreamId:
					extensionLen = 3 # dodatkowe bajty na PES, PTS, DTS itd

				if S == 1:
					if PSCP != 1: print("PSCP ERROR") # nie występuje ta sytuacja ani razu, ale niech zostanie
					#dane docelowe zaczynają się od header + extensionLen + int(PESpacket[63:71], 2)
					headLen = 6 + extensionLen + PESHeaderDataLength
					curPESSize = PES_packet_length
					PESHeaderDataLength = int(PESHeaderStr[64:72], 2) # ósmy bajt, o tyle można przeskoczyć do ładunku
					if PID==136:
						if outputPESAudio:# tutaj zapis jesli cos wcześniej było w buforze outputPES
							PID136Output.write(outputPESAudio[headLen:])#teraz gdy zapisuje CHUNKAMI, a nie jednym wielkim całym ciągiem, zaoszczędziłem 8 sekund
						if choice==1 or choice==2:
							outputLine = TSPacketLine + AFLine + PESLine
						outputPESAudio = b''

					elif PID==174:
						if PR:
							if choice==1 or choice==2:
								outputLine = TSPacketLine + AFLine + PESLine

						if outputPESVideo:
							PID174Output.write(outputPESVideo[headLen:])
						outputPESVideo = b''
				else:
					if PID==136:
						if CC == 15 and(choice==1 or choice==2):
							outputLine = TSPacketLine + AFLine + f' PES part-> PcktLen: {curPESSize + 6 } HeadLen: {headLen} DataLen: {curPESSize+6 - headLen}'

				if PID==136:outputPESAudio += PESpacket
				elif PID==174:outputPESVideo += PESpacket

			if choice==1 or choice==2:
				printLine=""
				if outputLine: printLine = outputLine
				else:
					if AF> 1:printLine = TSPacketLine + AFLine
					else:printLine = TSPacketLine

				if choice==1:print(printLine)
				else: txtFile.write(printLine+"\n")

			TS_PacketId +=1

		if choice==2:txtFile.close() # musze ręcznie zamknąć

print("Całkowity czas działania programu: ", time.time() - start)
print("Ilosć pakietów: ", TS_PacketId)
input("Wciśnij dowolny klawisz by zakończyć") # dla odpalania przez konsole, by nie wyłączyła się od razu

#Notatki, obserwacje:
#89 sekund processingu dla samego dźwięku, bez wypisywania danych, tryb laptopa comfort
#86 w trybie turbo, zapis do pliku to 8 * 10-5 s, czyli zapisu nie musze optymalizować, ale inne rzeszy tak
#Edit : odkryłem, że linia binData = "".join(map(lambda x: format(x, 'b').zfill(8), data)) ma największy nakład obliczeń(65 sekund)
#potem uświadomiłem sobie, że nie musze zamieniać wszystkich danych byteHEX(np. b'xff') na binaryString("1010101...", wystarczy, że
# zamienie tylko dane nagłówkowe, a pozostałe dane dopisze do global output i zapisze
# dzięki temu zszedłem do 15.9 sekundy w trybie laptopa comfort
# a dzięki zapisywaniu małych chunków(danych PES z aktualnego pakietu) do pliku w trybie append, zamiast jednego wielkiego w trybie write
#zaoszczędziłem kolejne 8 sekund, teraz w trybie comfort program wykonuje się dla samego dźwięku w 7.3 sekundy(bez wypisywania)

'''Czasy działania(tryb comfort):
ze względu na dokładnośc do nanosekund i zapisywanie małymi fragmentami czasy poszczególnych zapisów nie były rzeczywiste,
oraz nie zawsze nawet poprawnie przybliżone, dlatego nie ma o nich szczegółowych informacji
Pycharm:
	- tylko zapis audio i video: 16.8s
	- zapis danych o pakietach do pliku txt i zapis audioi video: 20.3s
		- zapis do pliku txt: 2.25s
		- zapis audio i video do plików: 1.42s
		- parsowanie danych nagłówkowych: 15.75
	- wypisanie danych o pakietach i zapis audio/video: 281.9s
	
Konsola pythona(uruchomienie skryptu bezpośrednio z pliku .py poprzez podwójne kliknięcie)
	- tylko zapis audio i video: 15.3s
	- zapis danych o pakietach do pliku txt i zapis audio/video: 19.5s
	- wypisanie danych o pakietach i zapis audio ivideo: 70.9s
'''






