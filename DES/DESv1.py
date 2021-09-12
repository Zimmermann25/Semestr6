
INITIAL_DATA_PERMUTATION = [58, 50, 42, 34, 26, 18, 10, 2,
							60, 52, 44, 36, 28, 20, 12, 4,
							62, 54, 46, 38, 30, 22, 14, 6,
							64, 56, 48, 40, 32, 24, 16, 8,
							57, 49, 41, 33, 25, 17, 9, 1,
							59, 51, 43, 35, 27, 19, 11, 3,
							61, 53, 45, 37, 29, 21, 13, 5,
							63, 55, 47, 39, 31, 23, 15, 7,
							]

# list for key permutation
KEY_PERMUTATION = [57, 49, 41, 33, 25, 17, 9,
				   1, 58, 50, 42, 34, 26, 18,
				   10, 2, 59, 51, 43, 35, 27,
				   19, 11, 3, 60, 52, 44, 36,
				   63, 55, 47, 39, 31, 23, 15,
				   7, 62, 54, 46, 38, 30, 22,
				   14, 6, 61, 53, 45, 37, 29,
				   21, 13, 5, 28, 20, 12, 4,
				   ]

#compression table to reduce key from 56 to 48 bit
KEY_COMPRESSION_TABLE = [14, 17, 11, 24, 1, 5, 3, 28,
						 15, 6, 21, 10, 23, 19, 12, 4,
						 26, 8, 16, 7, 27, 20, 13, 2,
						 41, 52, 31, 37, 47, 55, 30, 40,
						 51, 45, 33, 48, 44, 49, 39, 56,
						 34, 53, 46, 42, 50, 36, 29, 32,
						 ]

# to get a 48bits matrix
EXPANSION_MATRIX = [32, 1, 2, 3, 4, 5,
					4, 5, 6, 7, 8, 9,
					8, 9, 10, 11, 12, 13,
					12, 13, 14, 15, 16, 17,
					16, 17, 18, 19, 20, 21,
					20, 21, 22, 23, 24, 25,
					24, 25, 26, 27, 28, 29,
					28, 29, 30, 31, 32, 1,
					]

S_BOXES = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		 [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		 [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],

		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]],

		[ [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		  [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		  [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		  [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]],

		[ [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		  [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		  [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		  [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14] ],

		[ [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		  [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		  [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		  [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]],

		[ [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		  [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		  [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		  [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13] ],

		[ [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		  [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		  [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		  [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12] ],

		[ [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		  [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		  [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		  [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] ] ]

#this list is used to permutate after pass through all sboxes
PERMUTATION_AFTER_SBOXES = [16, 7, 20, 21, 29, 12, 28, 17,
							1, 15, 23, 26, 5, 18, 31, 10,
							2, 8, 24, 14, 32, 27, 3, 9,
							19, 13, 30, 6, 22, 11, 4, 25,
							]

#Final permut for datas after the 16 rounds
FINAL_PERMUTATION = [40, 8, 48, 16, 56, 24, 64, 32,
					 39, 7, 47, 15, 55, 23, 63, 31,
					 38, 6, 46, 14, 54, 22, 62, 30,
					 37, 5, 45, 13, 53, 21, 61, 29,
					 36, 4, 44, 12, 52, 20, 60, 28,
					 35, 3, 43, 11, 51, 19, 59, 27,
					 34, 2, 42, 10, 50, 18, 58, 26,
					 33, 1, 41, 9, 49, 17, 57, 25
					 ]


SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] # how many shifts to do during for every round

#this function is not used aanymore in my implementation, but it would be used if decided to allow user input plain ascii text
def plain_key_to_64_bits(key): # use ascii values, key will have 8 chars
	key = key[:8] if len(key) >8 else key.zfill(8) # add zeros at beginning of key
	output = ""
	for letter in key:
		output += format(ord(letter), "b").zfill(8)
	return output

def hex_key_to_64_bits(key):
	key = key[:16] if len(key) >16 else key.zfill(16) # add zeros at beginning of key
	output = ""
	for hex_value in key:
		output += bin(int(hex_value, 16))[2:].zfill(4)
	return output

def convert_hex_to_binary(hex_value):
	return bin(int(hex_value, 16))[2:].zfill(64) #[2:] is it trim 0x

def convert_binary_to_hex(bin_value):
	return hex(int(bin_value, 2))[2:]

def permutate_key(key, permutate_list, bit_length):
	permutation = ""
	for i in range(bit_length):
		permutation += key[permutate_list[i] - 1]
	return permutation

def shift_left(k, how_many): #how many can be 1 or 2, depend on shift table
	output = k[how_many:] + k[:how_many]
	return output

def xor_of_binary_strings(str1, str2):
	y = int(str1, 2)^int(str2,2)
	return bin(y)[2:].zfill(len(str2))


def create_rounded_key_binary_list_from_hex_key(my_key="AABB09182736CCDD"):
	my_key = "AABB09182736CCDD" # key need to be 8 bytes long(64 bits
	my_key = hex_key_to_64_bits(my_key)
	permutated_key = permutate_key(my_key, KEY_PERMUTATION, 56)

	left_part_of_key = permutated_key[:28]
	right_part_of_key = permutated_key[28:56]
	round_key_binary = []# local variable

	for i in range(16): # here use list SHIFT
		left_part_of_key = shift_left(left_part_of_key, SHIFT[i])
		right_part_of_key = shift_left(right_part_of_key, SHIFT[i])
		round_key_binary.append(permutate_key(left_part_of_key + right_part_of_key, KEY_COMPRESSION_TABLE, 48))

	return round_key_binary

def encryption(message, round_key_binary_list):
	print("message input: ", message)
	message = convert_hex_to_binary(message) # just to make sure
	print("message after hex2bin: ", message)
	message = permutate_key(message, INITIAL_DATA_PERMUTATION, 64)
	print("After initial permutation", convert_binary_to_hex(message))
	left_part = message[0:32]
	right = message[32:64]

	for i in range(16):
		right_part_expansion = permutate_key(right, EXPANSION_MATRIX, 48)
		xor_expanded = xor_of_binary_strings(right_part_expansion, round_key_binary_list[i])

		s_boxes_output = ""
		for j in range(8):
			row = int( (xor_expanded[j * 6] + xor_expanded[j * 6 + 5]), 2)
			col = int( (xor_expanded[j * 6 + 1] + xor_expanded[j * 6 + 2] + xor_expanded[j * 6 + 3] + xor_expanded[j * 6 + 4]), 2)
			#print("i: ", i, "j: ", j,"row: ", row, "col: ", col)
			val = S_BOXES[j][row][col] # in sboxes we have 4 bit values
			s_boxes_output += format(val, "b").zfill(4)

		final_s_boxes_output = permutate_key(s_boxes_output, PERMUTATION_AFTER_SBOXES, 32)
		left_part = xor_of_binary_strings(left_part, final_s_boxes_output)

		if i < 15:#swap only if it isnt last of 16 rounds
			left_part, right = right, left_part

	encrypted_output = permutate_key(left_part + right, FINAL_PERMUTATION, 64) # dont care about warning
	print(convert_binary_to_hex(encrypted_output))
	return encrypted_output


key = "2137AAAABBBBCCCC" # key need to be 8 bytes long(64 bits
message = "987654AAA3"
round_key_binary = create_rounded_key_binary_list_from_hex_key(key)
encrypted_text = encryption(message, round_key_binary) 
encrypted_text_hex = convert_binary_to_hex((encrypted_text))

print("encrypted text: ", encrypted_text)
print("Decryption")
rkb_rev = round_key_binary[::-1]
text = convert_binary_to_hex(encryption(encrypted_text_hex, rkb_rev[:]))
print("Plain Text : ",text)




