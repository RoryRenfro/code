import string 
def check_strength(pw): # defining the function pw
    score = 0 # default score
    if len(pw) >= 12: score += 1 # 12 or more characters it adds one point
    if any(c.islower() for c in pw ): score += 1 # if that character is a lowercase letter.
    if any(c.isupper() for c in pw ): score += 1 # checks for an uppercase letter.
    if any(c.isdigit() for c in pw ): score += 1  # checks for a number.
    if any(c in string.punctuation for c in pw): score += 1 # checks whether the character is a symbol.
    return score # This sends the final score, 0 to 5, back to whoever called the function.

print("password strength 0-5")
print(check_strength(input("password:   ")))
