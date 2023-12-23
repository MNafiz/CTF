from sage.all import *
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import *
import hashlib

p = 33184772290615481426295675425316668758122179640330548849957081783509
N = 6

u = [[28879155726567049983454622837721881713004421469649633653126003880251,22074946600328057026240224251921516029989227864483537878311928528684,11985344636547053777186855301874485401032363227366605932898421631165,11038047153398875511855062921770308445072978178537727544345865556069,17913589562779438181451311229483343663752773108623377725718452883819,6988548052196701160389870027180255419046432117124570998462066223760],
[12442646139394994295898159421691536460921770233410583384741128805851,26791343238957883953511341730456926026845067572390616134588257575715,20044295739622127408570744416765049400182932494144906328843165683951,3716946288972247122675229801442487271330697050902983897960257015353,28203806658422488413821254734838742146597120966298092240011671950418,4762041594051527320517864505450207655232589320366293231953595725863],
[30088717492536940712495821833412730937575223939046572858904284613916,27041904353687235206996420047457376344449825180129098056224307456338,24437749819141358658247648214143755332360241994475937257542642573583,7796437298901905297245658644368499053223939852560146715778064632640,15614447029063100426172954288407641313530323021423668136405899310194,8922479681646925758338291598256040373376681973788891756406422763139],
[19322178296033807354940969679463195308540921806504252678149867173138,33097125072731086770607131468725547500825910975790412321782115869838,12883750093703623804432147375290510155697961091062129358847651674123,24597869343287697641622709721671426915780058312255624403180234192713,26537027184297668426345397663386813121592656652583736980586291216445,11617206120365401967915791192731000879817682674901777733903856797733],
[16710090447056060108731601191705411717377136736726300253063986063308,13112164116392985346393033303671764991807289870465207976284880921022,31389068001989884948885767386697332939461030078718007394707803846255,29908327338977214304615826417150579857655888232250984362081852839023,22583975168456327742148140296560922679546031771450762766874213823663,20255781234412108781956807555843619052915858233204195711555194680279],
[8639975336305093270106069074993623126891247360031281653825740040741,13403900498226599196478196563037659383351290165716358605156795361654,19127443140313962513371049800518743806366324348931149667137542330176,1587790520831406950292877253889772565635165863077419349924612463554,28260643245678615796033409984375030239968039321917236595612922928109,27245620107342379746895845516019185969531890676595911744377909557532]]
v = [[14593469507593520336534893606693100073219081551387449023943771554442,2283021458111487923710380205365151066104282754263745192237326490551,13170584523093998223191696419879547969801075848834311698387381471505,19259980148204759114097202057965316584985415828667111050145931544542,29885290219184042616179535742918968947354026457415023160998318453828,15123772566136939254700272466681741447495954560621338927076401710465],
     [8217862512033149496876384094296269532452490863111766288591338421520,13729461020836068836298855334139849351346259147300854170266838049852,11104728330778098008854657250493837339864716593096275438194673593723,10798384644614928362418932155290042574495162355923347471159291144698,31877189181091302604647976237742181979760578672930582051196549136046,1918629350716436456009684853559872579413764560427000121836347921516],
     [17260689732862422635435505221480922746751317064535215923993790192886,15747877220363614821162725299191209258209710570887630567232690904197,8617228034985901541131740069450254422228498135170302566742947957775,14253933715820016671570267997896238444667901637428211288460788838246,16499164346493998999442730191394982099986918128009049722691512093014,13025912772710188038104092079604197742726564877681113284285303849554],
     [2573456644853874338239370492651477088261797251129609392543920453838,32896562598550390417662631073664427877599458467029721692315947839203,21609625125792777949315379171355985793236349536655762275501735276637,2064423690239912348059209794358643838603106021323566574579622769345,10416995935649914543433851087690149206442589809600595549054529630023,14743736977132006506906381861127077616280508458806441865058344748656],
     [4225662325959455234970599933733361974460852167061568484358345163405,10702969665926869787857799410201005975577054702738405546384443139142,1359255767431309667828876308576650892896838633542052871017414741807,31671777458706492709787940377250078973397972903701973598970849268174,24125683246160911728533816896560068159204522435801109506125539244342,6566591950072749090239378195580530026605442552103644998279546358496],
     [2340617144223968993993626239720251771746071020532956496851092249201,18464940637598472739277490361512029859881180718968424684424994902717,27460971987555371094455429952593747078655439217048574014441041685569,6667117338244005137290181664972559554258953283885089203943302963181,20312635823091168798778853401004417385080412291250382174823545520392,32296141232133239312731746201245526393343079356560448241095997297137]]

# print(u)

u = matrix(GF(p), u)
v = matrix(GF(p), v)
a = u.diagonalization()[0]
b = v.diagonalization()[0]

shared_secret = a + b
def decrypt(cipher, key):
    iv, enc = b64decode(cipher)[:16], b64decode(cipher)[16:]
    # i = 0
    # key = 0
    # for row in shared_secret:
    #     for item in row:
    #         key += item**i
    #         i += 1

    key = hashlib.sha256(long_to_bytes(int(key))).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)

    flag = cipher.decrypt(enc)
    return flag


ct1 = b"t22qVcUY/TYh9hwuASW/6PliQ03dLEWpOTqZHF82rQ/VqmqX7fj2l1YHzX7Cq0Sy"

ct2 = b"8t5wC5gsdXOG7vDvw+uStOT1P2ZhB2FGsr/lvNaBMX+FAZ9aVY4UMOk8neL3KcELjQ3F62aX/sxN4KexO/krK2mm/v10qYrKbLPXljdwvck="


# print(decrypt(ct1, shared_secret))

diagon_1 = list(a.diagonal())
diagon_2 = list(b.diagonal())
from itertools import permutations
permuts_1 = list(permutations(diagon_1))
permuts_2 = list(permutations(diagon_2))

k = 0
solved = False
for permut_1 in permuts_1:
    a = list(permut_1)
    for permut_2 in permuts_2:
        k += 1
        print(k)
        b = list(permut_2)
        ss = [i + j for i, j in zip(a, b)]
        pangkat = 0
        key = 0
        for s in ss:
            key += s**pangkat
            pangkat += 7
        result = decrypt(ct1, key % p)
        if b"flag" in result:
            print(result)
            print(unpad(decrypt(ct2, key % p), 16).decode())
            solved = True
            break
    if solved:
        break    
