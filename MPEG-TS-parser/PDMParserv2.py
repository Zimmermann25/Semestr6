import struct, time
import numpy as np
'''MPEG-TS packet:
`        3                   2                   1                   0  `
`      1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0  `
`     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ `
`   0 |                             Header                            | `
`     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ `
`   4 |                  Adaptation field + Payload                   | `
`     |                                                               | `
` 184 |                                                               | `
`     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ `


MPEG-TS packet header:
`        3                   2                   1                   0  `
`      1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0  `
`     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ `
`   0 |       SB      |E|S|T|           PID           |TSC|AFC|   CC  | `
`     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ `

Sync byte                    (SB ) :  8 bits
Transport error indicator    (E  ) :  1 bit
Payload unit start indicator (S  ) :  1 bit
Transport priority           (T  ) :  1 bit
Packet Identifier            (PID) : 13 bits
Transport scrambling control (TSC) :  2 bits
Adaptation field control     (AFC) :  2 bits
Continuity counter           (CC ) :  4 bits


AFL: 8bitów
DC: 1
RA: 1
SP: 1
PR: 1
OR: 1
SPFlag: 1
TP: 1
EX: 1

'''
class xTS:
	TS_PacketLength = 188
	TS_HeaderLength = 4
	PES_HeaderLength = 6
	BaseClockFrequency_Hz = 90000 #Hz
	ExtendedClockFrequency_Hz = 27000000 #Hz
	BaseClockFrequency_kHz = 90 #kHz
	ExtendedClockFrequency_kHz = 27000 #kHz
	BaseToExtendedClockMultiplier = 300

class xTS_PacketHeader:

	PIDDict = {
		"PAT": "0x0000",
		'CAT' : '0x0001',
        'TSDT' : '0x0002',
        'IPMT' : '0x0003',
        'NIT' : '0x0010', #DVB specific PID
        'SDT' : '0x0011', #DVB specific PID
        'NULL' : '0x1FFF'
	}

	def Reset(self):pass
	def Parse(self, Input):pass
	def Print(self):pass
	def hasAdaptationField(self):pass
	def hasPayload(self):pass

myFilePath = 'example_new.ts'
CHUNK = 188 # 188 bajtów = 1504 bity
TS_PacketId = 0

#te zmienne będą musiały być resetowane(funkcja reset())
CCCheck = 0
curPESSize = 0 # do kroku 3
PESHeaderDataLength = 0# do kroku 3 i 4
extensionLen = 0
headLen = 0
outputPES = b""
currentSize = 0

start = time.time()

PESTime = 0
with open("optimizedOutputPID136.mp2", 'ab+') as optimized:
	optimized.truncate(0) #usunięcie zawartości pliku optimOutput.mp2 jeśli taka zawartość już jest w tym pliku
	with open(myFilePath, "rb") as file:
		while True: #TS_PacketId < 200000
			curPacket = file.read(CHUNK)
			if curPacket ==b'':break
			data = list(struct.unpack(f'>{188}B', curPacket)) # 1 bajt unsigned char, > oznacza odczyt danych big endian(taki format pliku)
			#każdą szestastkową 8 bitową wartość nagłówka rzutuj na ciąg 0 i 1 typu string
			binHeader = "".join(map(lambda x: format(x, 'b').zfill(8), data[:4])) # w tej linii *był największy nakład obliczeń

			# teraz zauważyłem, że nie musze wszystkiego zamieniać na postać binarną z hex i trzymać w binData
			SB = binHeader[0:8]
			E = binHeader[8]
			S = int(binHeader[9], 2)
			P = binHeader[10]
			PID = int(binHeader[11:24], 2)
			TSC = int(binHeader[24:26], 2)
			AF = int(binHeader[26:28], 2)
			CC = int(binHeader[28:32], 2)
			curLine = f"PacketId: {TS_PacketId} SB: {int(SB, 2)} E: {E} S: {S} P: {P} PID: {PID} TSC: {TSC} AF: {AF} CC: {CC}"
			#krok 3 i jeszcze zapamiętanie długości PES gdy CC=0 i S=1
			if S==1:
				CCCheck = 0
				extensionLen = 0
				#curLine += " Started"
			elif CC==15 and CCCheck==15:
				curLine += " Finished"
			elif S==0 and CC==CCCheck:
				curLine += " Continue"
			elif S==0 and CC !=CCCheck:
				curLine += " CC ERROR"
				#print("Error: ", TS_PacketId)
			CCCheck +=1

			AFOffset = 0
			if AF > 1:  # 0<=AF<=3, dlatego AF> 1 albo AF=2 or AF=3
				#AF=2 - tylko pole AF, AF=3 - pole AF i jakies dodatkowe dane
				AFLData = "".join(map(lambda x: format(x, 'b').zfill(8), data[4:6]))  # 8 bitów
				AFLLength = int(AFLData[:8], 2)
				DC = AFLData[8]
				RA = AFLData[9]
				SP = AFLData[10]
				PR = AFLData[11]
				OR = AFLData[12]
				SPFlag = AFLData[13]
				TP = AFLData[14]
				EX = AFLData[15]
				curLine += f' AF: L= {AFLLength} DC:{DC} RA:{RA} SP:{SP} PR:{PR} OR:{OR} SPFlag:{SPFlag} TP:{TP} EX:{EX} Stuffing: {AFLLength-1}'
				AFOffset = 1+ AFLLength
			# wyliczenie stuffing bytes, trzeba sprawdzic pola PR i OR i pozostałe dodatki w polu AF

			#krok 3 - składanie, dla PID =136(fonia), nagłówek PES >=6bajtów, jak dodatkowe flagi to 9 bajtów łącznie
			PESpacket = b""
			if PID==136:
				if AF==0 or AF==1:
					PESpacket += curPacket[4:] # brak AF, najprostrzy przypadek, wchodzi tylko payload
				else: # jest AF, trzeba znać jego długość, tutaj payloadu może nawet nie być
					PESpacket += curPacket[4 + AFOffset:]

				PESHeaderStr = "".join(map(lambda x: format(x, 'b').zfill(8), PESpacket[:9]))

				#print("PESHeaderStr: ", PESHeaderStr)
				PSCP = int(PESHeaderStr[:24], 2) # packet start code prefix, powinno byc 0x000001
				#print("PSCP: ", PSCP)
				StreamID = int(PESHeaderStr[24:32], 2)
				PES_packet_length = int(PESHeaderStr[32:48], 2)
				tempLine = f' PSCP: {PSCP}, StreamID: {StreamID}, PES_packet_length: {PES_packet_length}'
				#print(tempLine)
				#trzeba sprawdzić StreamID, dla 0xBD(189), 0xC0(192) - 0xDF(223), 0xE0(224) - 0xEF(255) jest 3bajtowe extension a w nim m.in PTS i DTS
				forbiddenStreamId = [188, 190, 191, 240, 241, 255, 242, 248]

				if StreamID==189 or 192<=StreamID<=223 or 224<=StreamID<=255: # tu dać warunki z 6 minuty
					extensionLen = 3
				if CC==15:
					# trzeba dodać 6-9, bo to rozmiar nagłówka PES
					curLine += f' PES: Len={curPESSize + 6 } HeadLen = {headLen} DataLen: {curPESSize - extensionLen - PESHeaderDataLength}'
				t = time.time_ns()
				if S == 1: # ta część zajmuje 8.2 sekundy łącznie
					# tutaj zapis jesli cos wcześniej było w buforze outputPES
					if outputPES:
						#globalOutputPES += outputPES # kolejne miejsce z dużym nakładem obliczeń(8 sekund)
						#teraz gdy zapisuje CHUNKAMI, a nie jednym wielkim całym ciągiem, zaoszczędziłem 8 sekund
						optimized.write(outputPES)

					outputPES = b''
					if PSCP != 1: print("PSCP ERROR")

					headLen = 6 + extensionLen + PESHeaderDataLength
					#curLine += tempLine
					curPESSize = PES_packet_length
					PESHeaderDataLength = int(PESHeaderStr[64:72], 2) # ósmy bajt, o tyle można przeskoczyć do ładunku
					#print("iff")

				# dane docelowe zaczynają się od header + extensionLen + int(PESpacket[63:71], 2)
				packSize = len(PESpacket) * 8
				#print("packSize: ", packSize, "headLen: ", headLen)

				outputPES += PESpacket # 0.07 sekundy
				PESTime += (time.time_ns() - t)


			#print(curLine)
			#print(binData)
			TS_PacketId +=1


print(time.time() - start)
#print("PESTime: ", PESTime/(10 ** 9) )
print("numOfPackets: ", TS_PacketId)

#89 sekund processingu, bez wypisywania danych, tryb laptopa comfort
#86 w trybie turbo, zapis do pliku to 8 * 10-5 s, czyli zapisu nie musze optymalizować, ale inne rzeszy tak
#Edit : odkryłem, że linia binData = "".join(map(lambda x: format(x, 'b').zfill(8), data)) ma największy nakład obliczeń(65 sekund)
#potem uświadomiłem sobie, że nie musze zamieniać wszystkich danych byteHEX na binaryString, wystarczy, że
# zamienie tylko dane nagłówkowe, a pozostałe dane dopisze do global output i zapisze
# dzięki temu zszedłem do 15.9 sekundy w trybie laptopa comfort
# a dzięki zapisywaniu małych chunków do pliku w trybie append, zamiast jednego wielkiego w trybie write
#zaoszczędziłem kolejne 8 sekund, teraz w trybie comfort program wykonuje się w 7.3 sekundy

'''if PESpacket[48:50] == '00':
	print("brak PTS i DTS")
elif PESpacket[48:50] == '01':
	print("Forbidden")
elif PESpacket[48:50] == '10': # 5 bajtów dodatkowo(jest tylko PTS, czyli fonia)
	print("PTS ")
	#extensionLen += 5
elif PESpacket[48:50] == '11': #PTS i DTS, 10 + 6(escr) + 3(ES rate) +
	print("PTS i DTS")'''








