import random

scrambled = []
alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789!/;.:?,*$^)([]#~")
random.shuffle(alphabet)
shuffled = "".join(alphabet)

shift = random.randint(1, 100)

for char in alphabet:
    index = alphabet.index(char)
    char = alphabet[(index - shift) % len(alphabet)]
    scrambled.append(char)

print(shuffled, shift, sep='|')
