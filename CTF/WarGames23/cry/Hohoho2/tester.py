from Crypto.Util.number import *

m = 0xb00ce3d162f598b408e9a0f64b815b2f
a = 0xaaa87c7c30adc1dcd06573702b126d0d
c = 0xcaacf9ebce1cdf5649126bc06e69a5bb

nama = bytes_to_long(b"Santa Claus")

inv_amin1 = inverse(a-1, m)

for i in range(120, 1000, 8):
    kanan = nama << i
    hasil = (-(inv_amin1 * c + kanan)) % m
    print(hasil.bit_length(), i)
    print((inv_amin1 * c + bytes_to_long(long_to_bytes(kanan + hasil))) % m)
    print(long_to_bytes(kanan+hasil) , long_to_bytes(hasil))
