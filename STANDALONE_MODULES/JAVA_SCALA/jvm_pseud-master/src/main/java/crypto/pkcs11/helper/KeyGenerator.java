package crypto.pkcs11.helper;

import iaik.pkcs.pkcs11.*;
import iaik.pkcs.pkcs11.Mechanism;
import iaik.pkcs.pkcs11.objects.*;
import iaik.pkcs.pkcs11.wrapper.PKCS11Constants;

public class KeyGenerator {
    //TAKEN FROM THIS TUTORIAL
    //https://medium.com/@mevan.karu/want-to-know-how-to-talk-to-a-hsm-at-code-level-69cb9ba7b392

    public static AESSecretKey generateAESKey(Session session, String keyLabel, String keyId) throws TokenException {
        // Create a template of the key that we are going to generate.
        AESSecretKey secretKeyTemplate = new AESSecretKey();
        // Set the token value true. This saves the key in the token.
        secretKeyTemplate.getToken().setBooleanValue(Boolean.TRUE);
        // Makes key to be used for encrypting operations.
        secretKeyTemplate.getEncrypt().setBooleanValue(Boolean.TRUE);
        // Makes key to be used for decrypting operations.
        secretKeyTemplate.getDecrypt().setBooleanValue(Boolean.TRUE);
        // Make key private. When a key is private only authorized user can access the key.
        secretKeyTemplate.getPrivate().setBooleanValue(Boolean.TRUE);
        // Makes the key sensitive.
        secretKeyTemplate.getSensitive().setBooleanValue(Boolean.TRUE);
        // Makes the key not extractable. So key can't be retrieved outside the HSM.
        secretKeyTemplate.getExtractable().setBooleanValue(Boolean.FALSE);
        // Set a label to the key. Label can be used to retrieve the key.
        if (keyLabel != null) {
            secretKeyTemplate.getLabel().setCharArrayValue(keyLabel.toCharArray());
        }
        // Set the length of the key.
        secretKeyTemplate.getValueLen().setLongValue(32L);
        // Key template configuration is complete.
        // Selects the key generation mechanism.
        Mechanism keyGenMechanism = Mechanism.get(PKCS11Constants.CKM_AES_KEY_GEN);
        // Generates the key using the initiated session.
        if (keyId != null) {
            secretKeyTemplate.getId().setValue(keyId.getBytes());
        }
        AESSecretKey secretKey = (AESSecretKey) session.generateKey(keyGenMechanism, secretKeyTemplate);

        return secretKey;
    }
}
