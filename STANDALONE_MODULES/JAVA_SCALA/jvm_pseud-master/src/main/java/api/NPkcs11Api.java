package api;

import api.conf.NPkcs11ApiConf;
import crypto.pkcs11.helper.KeyGenerator;
import crypto.pkcs11.helper.KeyRetriever;
import crypto.pkcs11.helper.SessionHandler;
import crypto.utils.NCryptoAPI;
import iaik.pkcs.pkcs11.Session;
import iaik.pkcs.pkcs11.TokenException;
import iaik.pkcs.pkcs11.objects.AESSecretKey;
import iaik.pkcs.pkcs11.objects.Key;

import java.io.IOException;

public class NPkcs11Api implements NCryptoAPI<Session, AESSecretKey> {

    private final NPkcs11ApiConf conf;

    public NPkcs11Api(NPkcs11ApiConf conf) {
        this.conf = conf;
    }

    @Override
    public Session getLibraryInstance() {

        try {
            System.out.println("Linux");
            return SessionHandler.initSession(true, conf.getPin(), conf.getPathToLinuxModule() + "./" + conf.getLinuxModuleFileName());
        } catch (IOException e) {
            System.out.println("Windows");
            try {
                return SessionHandler.initSession(true, conf.getPin(),  "./" + conf.getWindowsModuleFileName());
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            } catch (TokenException ex) {
                throw new RuntimeException(ex);
            }
        } catch (TokenException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public AESSecretKey getKeyInstance(Session session) {
        return getAESKey(session, conf.getKeyLabel(), conf.getKeyId());
    }

    private static AESSecretKey getAESKey(Session session, String keyLabel, String keyId) {
        try {
            AESSecretKey secretKey = (AESSecretKey) NPkcs11Api.retrieveKey(session, keyLabel, keyId, new AESSecretKey());
            if (secretKey == null) {
                System.out.println("Generating AES Key");
                secretKey = KeyGenerator.generateAESKey(session, keyLabel, keyId);
            }
            return secretKey;
        } catch (TokenException e) {
            System.err.println(e);
        } catch (IOException e) {
            System.err.println(e);
        }
        return null;
    }

    private static Object retrieveKey(Session session, String keyLabel, String keyId, Key keyTemplate) throws TokenException, IOException {
        if (keyLabel != null) {
            keyTemplate.getLabel().setCharArrayValue(keyLabel.toCharArray());
        }
        if (keyId != null) {
            keyTemplate.getId().setValue(keyId.getBytes());
        }
        return KeyRetriever.retrieveKey(session, keyTemplate);
    }
}
