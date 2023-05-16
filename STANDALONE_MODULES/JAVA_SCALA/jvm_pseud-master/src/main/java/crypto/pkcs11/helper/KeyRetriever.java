package crypto.pkcs11.helper;

import iaik.pkcs.pkcs11.Session;
import iaik.pkcs.pkcs11.TokenException;
import iaik.pkcs.pkcs11.objects.Key;
import iaik.pkcs.pkcs11.objects.Object;

public class KeyRetriever {

    //https://github.com/mevan-karu/Crypto/blob/master/src/main/java/org/karu95/hsm/cryptoprovider/keyhandlers/KeyRetriever.java
    public static Object retrieveKey(Session session, Key keyTemplate) {
        Object key = null;
        try {
            session.findObjectsInit(keyTemplate);
            Object[] secretKeyArray = session.findObjects(1);
            System.out.println(secretKeyArray.length);
            if (secretKeyArray.length > 0) {
                key = secretKeyArray[0];
            }
        } catch (TokenException e) {
            System.out.println("Key retrieval error : " + e.getMessage());
        }
        return key;
    }
}