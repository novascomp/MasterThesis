package crypto.pkcs11;

import crypto.utils.Input;
import crypto.utils.NCommonUtils;
import crypto.utils.NCrypto;
import crypto.utils.NCryptoAPI;
import iaik.pkcs.pkcs11.Mechanism;
import iaik.pkcs.pkcs11.Session;
import iaik.pkcs.pkcs11.TokenException;
import iaik.pkcs.pkcs11.objects.AESSecretKey;
import iaik.pkcs.pkcs11.parameters.InitializationVectorParameters;
import iaik.pkcs.pkcs11.wrapper.PKCS11Constants;

import java.security.NoSuchAlgorithmException;

public class NCryptoPKCS11 extends NCrypto<Session, AESSecretKey> {

    private final Session session;
    private final AESSecretKey secretKey;

    private static long encryptionMode = PKCS11Constants.CKM_AES_CBC_PAD;

    public NCryptoPKCS11(NCryptoAPI cryptoAPI) {
        super(cryptoAPI);
        session = super.cryptoAPI.getLibraryInstance();
        secretKey = super.cryptoAPI.getKeyInstance(session);
    }

    @Override
    public String encrypt(String staticRandomText, String id, String colName, String plainText, boolean hsmIv) {
        try {
            byte[] iv = NCommonUtils.localIvComputation(NCommonUtils.getDataForIvToHash(staticRandomText, id, colName));
            byte[] encrypted_data = encryptText(session, secretKey, plainText.getBytes(), iv);
            return NCommonUtils.byteArrayToHex(encrypted_data);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        } catch (TokenException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public String decrypt(String staticRandomText, String id, String colName, String encrypted_text, boolean hsmIv) {
        try {
            byte[] iv = NCommonUtils.localIvComputation(NCommonUtils.getDataForIvToHash(staticRandomText, id, colName));
            byte[] decrypted_data = decryptText(session, secretKey, NCommonUtils.hexStringToByteArray(encrypted_text), iv);
            return new String(decrypted_data);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        } catch (TokenException e) {
            throw new RuntimeException(e);
        }
    }

    private static byte[] decryptText(Session session, AESSecretKey aesSecretKey, byte[] encryptedData, byte[] iv) throws TokenException {
        Mechanism decryptionMechanism = Mechanism.get(encryptionMode);
        InitializationVectorParameters encryptionIV = new InitializationVectorParameters(iv);
        decryptionMechanism.setParameters(encryptionIV);
        session.decryptInit(decryptionMechanism, aesSecretKey);
        return session.decrypt(encryptedData);
    }

    private static byte[] encryptText(Session session, AESSecretKey aesSecretKey, byte[] dataToBeEncrypted, byte[] iv) throws TokenException {
        Mechanism encryptionMechanism = Mechanism.get(encryptionMode);
        InitializationVectorParameters encryptionIV = new InitializationVectorParameters(iv);
        encryptionMechanism.setParameters(encryptionIV);
        session.encryptInit(encryptionMechanism, aesSecretKey);
        return session.encrypt(dataToBeEncrypted);
    }


}
