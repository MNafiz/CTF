from Crypto.Util.number import *

e=65537
d=10131385304346570862363672172479519014930196271019995786636312761595202976450148525856815802701000395414648952879542541837910153242322423617197237081517011770343483507147954603379775340354032171550002536949191526202882949011106324041950510428758192313639209608707267332626133813390706665183988905212402750559145874995378245989993172259045667922846459311291985631230765966175223063139300905844320136274784624189163396906195799651998297869785519453265295374484060469164750248157894549952155452201133386235668857589261017670709438675856434770369359043902405695013655876701550558255085119222905499413506619974520521907153
c=1591593246724999157444008497106998368793471183592237428604918799806530662349233859065006645389458330558447172355985537799936194439156401544278647409770856710101582617356645426116505937153919976163702450941667082770458220441555095046766518858126075220141563492528380016928322963102674156419345333112293094730388377740324702591650228853638137319581108498792859951612428620592885066215059208092697600743756952698387228113163058022227163874269292207709655891394840983772918753408397511455228387949415206869066679326964693685361100609298892890851027616112242014286515289992546231083350031229884737787886851166815320868631
hint=310523594211028464213357784311804646819308563816530741249790561697832923934423149152314610812096556160037359144686312133689119420764809735121486289170354537676025380665378738340474105599200706354127431296226082340642147576764659209798017224957787825582300844224668937186911935689407316590283570029569032779924
kphi = e*d - 1

for k in range(1,100000):
    if kphi % k == 0:
        phi = kphi // k
        n = phi + hint - 1
        if pow(2, phi, n) == 1:
            m = pow(c, d, n)
            flag = long_to_bytes(m)
            print(flag, k)
            break