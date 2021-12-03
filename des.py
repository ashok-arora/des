from __future__ import print_function, unicode_literals
from PyInquirer import prompt

from des_constants import initial_permutation, final_permutation
from des_constants import expansion_D_box, straight_D_box, compression_D_box
from des_constants import sbox, pc1_table, shift_table

from utilities import hex2bin, bin2hex, dec2bin, bin2dec
from utilities import xor, permute, shift_left


def sub_key_generation(key):
    print("--------------------------------\nGeneration of 16 subkeys")

    key = hex2bin(key)

    print(f"\nGiven key = {bin2hex(key)} = {key}")

    # PC-1 Table
    key = permute(key, pc1_table, 56)

    print(f"Given key after PC1 = {bin2hex(key)} = {key}\n")

    left = key[0:28]
    right = key[28:]

    print(f"Left half = {bin2hex(left)} = {left}")
    print(f"Right half = {bin2hex(right)} = {right}\n")

    round_key_binary = []

    number_of_rounds = 16

    for i in range(0, number_of_rounds):

        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])

        print(f"Key Generation Round {i+1} Left half = {bin2hex(left)} = {left}")
        print(f"Key Generation Round {i+1} Right half = {bin2hex(right)} = {right}")

        combined = left + right
        print(
            f"Key Generation Round {i+1} Combined key = {bin2hex(combined)} = {combined}"
        )
        round_key = permute(combined, compression_D_box, 48)
        print(
            f"Key Generation Round {i+1} Compressed key = {bin2hex(round_key)} = {round_key}\n"
        )
        round_key_binary.append(round_key)

    return round_key_binary


def encrypt(plaintext, round_key_bin, text="Plain"):
    binary_plaintext = hex2bin(plaintext)
    print("--------------------------------\n16 rounds of DES")
    print(f"{text} text = {bin2hex(binary_plaintext)} = {binary_plaintext}")

    initial_permutated = permute(binary_plaintext, initial_permutation, 64)
    print(
        f"{text} text after IP = {bin2hex(initial_permutated)} = {initial_permutated}\n"
    )

    left = initial_permutated[0:32]
    right = initial_permutated[32:]

    print(f"Left half = {bin2hex(left)} = {left}")
    print(f"Right half = {bin2hex(right)} = {right}\n")

    number_of_rounds = 16

    for i in range(0, number_of_rounds):
        print(f"Cipher Round {i+1} input to F = {bin2hex(right)} = {right}")

        right_expanded = permute(right, expansion_D_box, 48)
        print(
            f"Cipher Round {i+1} Right expanded = {bin2hex(right_expanded)} = {right_expanded}"
        )

        s_box_input = xor(right_expanded, round_key_bin[i])
        print(
            f"Cipher Round {i+1} S-box input = {bin2hex(s_box_input)} = {s_box_input}"
        )

        s_box_output = ""
        for j in range(0, 8):

            first_bit = s_box_input[j * 6]
            second_bit = s_box_input[j * 6 + 1]
            third_bit = s_box_input[j * 6 + 2]
            fourth_bit = s_box_input[j * 6 + 3]
            fifth_bit = s_box_input[j * 6 + 4]
            sixth_bit = s_box_input[j * 6 + 5]

            row = bin2dec(int(first_bit + sixth_bit))
            col = bin2dec(int(second_bit + third_bit + fourth_bit + fifth_bit))
            val = sbox[j][row][col]
            s_box_output = s_box_output + dec2bin(val)

        print(
            f"Cipher Round {i+1} S-box output = {bin2hex(s_box_output)} = {s_box_output}"
        )

        s_box_output = permute(s_box_output, straight_D_box, 32)
        left = xor(left, s_box_output)

        if i != 15:
            left, right = right, left

        print(f"Cipher Round {i+1} Output of F  = {bin2hex(right)} = {right}")
        print(f"Cipher Round {i+1} Left Half = {bin2hex(left)} = {left}")
        print(f"Cipher Round {i+1} Right Half  = {bin2hex(right)} = {right}")
        print(
            f"Cipher Round {i+1} Key = {bin2hex(round_key_bin[i])} = {round_key_bin[i]}\n"
        )

    combine = left + right
    print(f"Round 16 left and right combined = {bin2hex(combine)} = {combine}")

    cipher_text = permute(combine, final_permutation, 64)
    print(f"Combined after FP = {bin2hex(cipher_text)} = {cipher_text}")

    return cipher_text


print(
    """
Sample Input/Output: 
    cipher_text = "C0B7A8D05F3A829C"
    key = "AABB09182736CCDD"
    plain_text = "123456ABCD132536"
"""
)


def main():
    questions = [
        {
            "type": "list",
            "name": "cipher_type",
            "message": "[DES] What do you want to do?",
            "choices": ["Encryption", "Decryption"],
        },
    ]

    answers = prompt(questions)
    if answers["cipher_type"] == "Encryption":
        questions = [
            {
                "type": "input",
                "name": "plain_text",
                "message": "Enter the plain text (hex): ",
            },
            {
                "type": "input",
                "name": "key",
                "message": "Enter the key (hex): ",
            },
        ]
        answers = prompt(questions)
        cipher_text = answers["plain_text"]
        key = answers["key"]

        print(f"Encryption of \n\plain text = {cipher_text} \n\tusing key = {key}")

        sub_keys = sub_key_generation(key)
        print([bin2hex(x) for x in sub_keys])

        decrypted_text = bin2hex(encrypt(cipher_text, sub_keys))
        print("\nPlain Text = ", decrypted_text)
    else:
        questions = [
            {
                "type": "input",
                "name": "cipher_text",
                "message": "Enter the cipher text (hex): ",
            },
            {
                "type": "input",
                "name": "key",
                "message": "Enter the key (hex): ",
            },
        ]
        answers = prompt(questions)
        cipher_text = answers["cipher_text"]
        key = answers["key"]

        print(f"Encryption of \n\cipher text = {cipher_text} \n\tusing key = {key}")
        sub_keys = sub_key_generation(key)
        print([bin2hex(x) for x in sub_keys])

        reversed_sub_keys = sub_keys[::-1]
        print([bin2hex(x) for x in reversed_sub_keys])

        decrypted_text = bin2hex(encrypt(cipher_text, reversed_sub_keys, text="Cipher"))
        print("\nPlain Text = ", decrypted_text)


if __name__ == "__main__":
    main()
