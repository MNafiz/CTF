# dimension
n = 64
# plaintext modulus
p = 257
# ciphertext modulus
q = 0x10001
# bound for error term
error_bound = int(floor((q/p)/2))
# message scaling factor
delta = int(round(q/p))


V = VectorSpace(GF(q), n)
S = V.random_element()
print("S = ", S, "\n")

m = ?

A = V.random_element()
error = randint(-error_bound, error_bound)
b = A * S + m * delta + error

print("A = ", A)
print("b = ", b)
