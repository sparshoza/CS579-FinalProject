import secrets

def generate_shares(secret, threshold, total_shares):
    coefficients = [secret] + [secrets.randbelow(256) for _ in range(threshold - 1)]
    #This line generates threshold number of coefficients to be used in the polynomial that will be used to generate the shares. The first coefficient is set to the value of the secret,
    # and the remaining coefficients are generated using the secrets.randbelow(256) function, which generates a random integer between 0 and 255 (inclusive).
    shares = {}
     #This loop generates total_shares number of shares using the coefficients generated earlier. For each share, a random value of x is chosen, and the corresponding value of y is 
    # calculated using the polynomial defined by the coefficients. The share is then added to a dictionary called shares, which maps the x value to the tuple (x, y).

    for i in range(1, total_shares + 1):
        x = i
        y = sum([coefficients[j] * x ** j for j in range(threshold)])
        shares[x] = (x, y)
    return shares

def combine_shares(shares):
    x_values, y_values = zip(*shares.values())
    if len(set(x_values)) != len(x_values):
        raise ValueError("Cannot recover the secret from the given shares")
    secret = 0
    #This loop reconstructs the secret using the x and y values of the shares. For each x value, a numerator and denominator are calculated using the other x values in the shares. 
    # These values are used to compute a Lagrange coefficient, which is multiplied by the corresponding y value to obtain a partial sum of the secret. 
    for i in range(len(x_values)):
        numerator = denominator = 1
        for j in range(len(x_values)):
            if i == j:
                continue
            numerator *= -x_values[j]
            denominator *= x_values[i] - x_values[j]
        secret += y_values[i] * numerator // denominator
    return secret

#secret will be the input ( secret message being shared, only works with numbers)
#threshold is the max amounts of internal rebuilders
#total shares is the total amount of times the secret is shared
secret = 11929
threshold = 5
total_shares = 7
shares = generate_shares(secret, threshold, total_shares)
print("Shares:", shares)
recovered_secret = combine_shares(shares)
print("Recovered secret:", recovered_secret)
