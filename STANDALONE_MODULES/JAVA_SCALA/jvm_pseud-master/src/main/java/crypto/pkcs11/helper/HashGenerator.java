package crypto.pkcs11.helper;

import iaik.pkcs.pkcs11.Mechanism;
import iaik.pkcs.pkcs11.Session;
import iaik.pkcs.pkcs11.TokenException;
import iaik.pkcs.pkcs11.objects.SecretKey;

import java.math.BigInteger;

public class HashGenerator {

    public static String hash(Session session, byte[] dataToBeHashed, long digestMechanism, SecretKey key) {
        String hashValue = null;
        Mechanism hashingMechanism = Mechanism.get(digestMechanism);
        if (hashingMechanism.isDigestMechanism()) {
            try {
                session.digestInit(hashingMechanism);
                session.digestKey(key);
                byte[] digestVal = session.digest(String.valueOf(dataToBeHashed).getBytes());
                hashValue = new BigInteger(1, digestVal).toString(16);
                System.out.println(hashValue);
            } catch (TokenException e) {
                System.out.println("Hash generation error : " + e.getMessage());
            }
        }
        return hashValue;
    }
}
