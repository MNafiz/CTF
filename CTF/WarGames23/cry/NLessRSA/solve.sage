from sage.all import *
from Crypto.Util.number import *

phi=340577739943302989719266782993735388309601832841016828686908999285012058530245805484748627329704139660173847425945160209180457321640204169512394827638011632306948785371994403007162635069343890640834477848338513291328321869076466503121338131643337897699133626182018407919166459719722436289514139437666592605970785141028842985108396221727683676279586155612945405799488550847950427003696307451671161762595060053112199628695991211895821814191763549926078643283870094478487353620765318396817109504580775042655552744298269080426470735712833027091210437312338074255871034468366218998780550658136080613292844182216509397934480
e=65537
c=42363396533514892337794168740335890147978814270714150292304680028514711494019233652215720372759517148247019429253856607405178460072049996513931921948067945946086278782910016494966199807084840772350780861440737097778578207929043800432279437709296060384506082883401105820800844187947410153745248466533960754243807208804084908637481187348394987532434982032302570226378255458486161579167482667571132674473067323283939026297508548130085016660893371076973067425309491443342096329853486075971866389182944671697660246503465740169215121081002338163263904954365965203570590704089906222868145676419033148652705335290006075758484
p = 161858851126363750131252278443447168260852575582585451640814432234372639248575999813974282205976906890574920486285708765150639612195410229043083289561691094157966293503325568381598667787734900472194008968504777213838234481951932391653763314418452086665006225863274324640443184430553056738832834747049214763773
# phi=384311908785744245321358708225189221259009647913732006922216061052684579183795045340296093789847179853695837499175713502900631762148538450847942480446554534710419587457366481581551847156963660249754053760377199526625539515135186841126194946117088139842502462240071522249812962834235561263869865532565266413663004093821447736717407139675210985864241924063719832695843115110848563054560635889076173117439859526286554152992652788703209654326440234429232395571156945988045006562101452120168793536520995461322047354796481075693046515345347545042558026048601258826991795096218849780379215793958704302585840325809038713602188
# e=65537

q = (phi // (p - 1)) + 1
n = p * q

print(pow(3, phi, n))
d = inverse(e, phi)
m = pow(c, d, n)

print(long_to_bytes(int(m)))

# x = var("x", domain=ZZ)


# for i in range(-2000,2000):
#     print(i+1)
#     jml = 37*0xcafebabe + i 
#     print(jml)
#     rhs = phi - jml
#     sols = solve([x*(13*x - jml) - x - 13*x + 1 == rhs], x)
#     print(sols)
#     if sols:
#         break
    # sols = solve([(x-1)*(y-1)==phi, 13*x - y == jml], (x, y), solution_dict=True)
    # for sol in sols:
    #     p = int(sol[x])
    #     q = int(sol[y])
    #     if p > 0 and q > 0 and (p-1)*(q-1) == phi:
    #         print("Dapet")