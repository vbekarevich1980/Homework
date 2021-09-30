# Task 6.3
# Implement The Keyword encoding and decoding for latin alphabet.
# The Keyword Cipher uses a Keyword to rearrange the letters in the alphabet.
# Add the provided keyword at the beginning of the alphabet.
# A keyword is used as the key, and it determines the matching of the letter in the cipher alphabet to the plain
# alphabet.
# Repeats of letters in the word are removed, then the cipher alphabet is generated with the keyword matching
# to A, B, C etc. until the keyword is used up, whereupon the rest of the ciphertext letters are used in alphabetical
# order, excluding those already used in the key.
#
# <em> Encryption:
# Keyword is "Crypto"
#
# * A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
# * C R Y P T O A B D E F G H I J K L M N Q S U V W X Z
# </em>
#
# Example:
# ```python
# >>> cipher = Cipher("crypto")
# >>> cipher.encode("Hello world")
# "Btggj vjmgp"
#
# >>> cipher.decode("Fjedhc dn atidsn")
# "Kojima is genius"
# ```
from string import ascii_uppercase
from string import ascii_lowercase


class Cipher:

    def __init__(self, keyword):
        self.keyword = keyword.upper()
        self.__set_cipher(self.keyword)

    def __set_cipher(self, keyword):
        no_rptd_lttrs_kwrd = ''
        for lttr in keyword:
            if lttr not in no_rptd_lttrs_kwrd:
                no_rptd_lttrs_kwrd += lttr
        cipher = no_rptd_lttrs_kwrd + ''.join([lttr for lttr in ascii_uppercase if lttr not in no_rptd_lttrs_kwrd])
        self.__cipher = cipher

    def encode(self, text):
        encoded = ''
        for lttr in text:
            if lttr.isupper() and lttr in ascii_uppercase:
                encoded += self.__cipher[ascii_uppercase.find(lttr)]
            elif lttr.islower() and lttr in ascii_lowercase:
                encoded += self.__cipher[ascii_lowercase.find(lttr)].lower()
            else:
                encoded += lttr
        print(encoded)
        return encoded

    def decode(self, text):
        decoded = ''
        for lttr in text:
            if lttr.isupper() and lttr in ascii_uppercase:
                decoded += ascii_uppercase[self.__cipher.find(lttr)]
            elif lttr.islower() and lttr in ascii_lowercase:
                decoded += ascii_lowercase[self.__cipher.lower().find(lttr)]
            else:
                decoded += lttr
        print(decoded)
        return decoded


c = Cipher("crypto")
c.encode("Hello-world")
c.decode("Fjedhc dn atidsn")
