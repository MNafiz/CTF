from sage.all import *
from Crypto.Util.number import *


enc = 29004754752602891845701088578222561842513874918199800431567395933687795651470110377063745715224303592560274634075790412592313062222984678812372502446455553874025887805048706501835504141010199497560376154063288969798733730977056261626071788261554096303337042690996275614463889111101331868052859671922570628337639260391486134758084403718297925958046876883450312203509912864798807966117003174457393430905875449096266440351779141369905085213013783089319684239294684146737340793537160633379849038762741682795276911283424980467314859075820283929128473248792350786471543057922435616411342493331051424182347254472208007118691
n = 29353585191166156442189968012744774060523695365304588409452746298446966090446842013875144703842901644120084459742264199601712574341648935494662522676662195240580196375882847987434122422257670543787177894139225539012913211123707515022561081594248680970805167931112717636527712860774929806451263605673800306509371173663128670975257217464868471515902953618301217178231352288283127976806763613672091333537163342358371199303987661809368689697952949595308131881547519088258353529773216590952608452869230534334146785053625093426887703186355237207342461913924093535411997384080910520555094397726389504592515273009631000424191
e = 65537
leaked_p =[45076, 36169, 27950, 3563, 58188, 12614, 34400, 51608, 49317, 7186, 29518, 8535, 56393, 40272, 39843, 23648, 26140, 28698, 15925, 38759, 40734, 63262, 38472, 32529, 47175, 21167, 7210, 186, 18613, 17886, 16089, 4581, 28636, 51482, 52145, 4195, 44626, 58924, 1648, 16919, 40502, 35057, 34613, 64918, 11281, 41851, 14937, 53613, 7916, 58724, 35363, 19206, 46857, 10047, 18314, 31238, 15372, 64765, 14671, 16685, 16685, 16698, 34390, 41472]
key = 16685
p_partial = [bin(l^^key)[2:].zfill(16) for l in leaked_p]
p_partial = int("".join(p_partial),2)

a = p_partial

X = 2^81
M = matrix([[X^2, 2*X*a, a^2], [0, X, a], [0, 0, n]])
B = M.LLL()

Q = B[0][0]*x^2/X^2+B[0][1]*x/X+B[0][2]
p = p_partial + Q.roots(ring=ZZ)[0][0]
q = n//p

phi = (p-1)*(q-1)
d = inverse(e,phi)
m = pow(enc,d,n)

print(bytes.fromhex(hex(m)[2:]))