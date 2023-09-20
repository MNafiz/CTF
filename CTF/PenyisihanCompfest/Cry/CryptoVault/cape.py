import ecdsa
import ecdsa.ellipticcurve as EC

curve = ecdsa.SECP256k1
G = curve.generator
n = G.order()
x 	= int('ce205d44c14517ba33f3ef313e404537854d494e28fcf71615e5f51c9a459f42', 16)
y = int('6080e22d9a44a5ce38741f8994ac3a14a6760f06dd1510b89b6907dfd5932868', 16)
Q = EC.Point(curve.curve, x, y)
print(ecdsa.VerifyingKey.from_public_point(Q, curve))