package crypto.jce;

import api.helper.NJceProvider;
import crypto.utils.NCommonUtils;
import crypto.utils.NCrypto;
import crypto.utils.NCryptoAPI;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.nio.charset.StandardCharsets;
import java.security.*;

public class NCryptoJCE extends NCrypto<NJceProvider, Key> {

    private final String MODE = "AES/CBC/PKCS5PADDING";

    private final NJceProvider provider;

    private final Key secretKey;

    private final boolean withoutHSM;

    public static final String LOCAL_KEY_NAME = "local_aes_key_256";

    public NCryptoJCE(NCryptoAPI<NJceProvider, Key> cryptoAPI, boolean withoutHSM) {
        super(cryptoAPI);
        if (!withoutHSM) {
            this.provider = cryptoAPI.getLibraryInstance();
            this.secretKey = cryptoAPI.getKeyInstance(this.provider);
        } else {
            this.provider = null;
            try {
                ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream(LOCAL_KEY_NAME));
                this.secretKey = (Key) inputStream.readObject();
                inputStream.close();
            } catch (IOException e) {
                throw new RuntimeException(e);
            } catch (ClassNotFoundException e) {
                throw new RuntimeException(e);
            }
        }

        this.withoutHSM = withoutHSM;
    }

    @Override
    public String encrypt(String staticRandomText, String id, String colName, String plainText, boolean hsmIv) {

        try {
            Cipher c = null;
            byte[] iv = NCommonUtils.localIvComputation(NCommonUtils.getDataForIvToHash(staticRandomText, id, colName));

            if (withoutHSM) {
                c = Cipher.getInstance(MODE);
            } else {
                c = Cipher.getInstance(MODE, provider.getProvider());
            }
            c.init(Cipher.ENCRYPT_MODE, secretKey, new IvParameterSpec(iv));
            byte[] encrypted = c.doFinal(plainText.getBytes(StandardCharsets.UTF_8));
            return NCommonUtils.byteArrayToHex(encrypted);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        } catch (NoSuchPaddingException e) {
            throw new RuntimeException(e);
        } catch (InvalidAlgorithmParameterException e) {
            throw new RuntimeException(e);
        } catch (InvalidKeyException e) {
            throw new RuntimeException(e);
        } catch (IllegalBlockSizeException e) {
            throw new RuntimeException(e);
        } catch (BadPaddingException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public String decrypt(String staticRandomText, String id, String colName, String encrypted_text, boolean hsmIv) {
        try {
            Cipher c = null;
            byte[] iv = NCommonUtils.localIvComputation(NCommonUtils.getDataForIvToHash(staticRandomText, id, colName));
            if (withoutHSM) {
                c = Cipher.getInstance(MODE);
            } else {
                c = Cipher.getInstance(MODE, provider.getProvider());
            }
            c.init(Cipher.DECRYPT_MODE, secretKey, new IvParameterSpec(iv));
            byte[] decrypted = c.doFinal(NCommonUtils.hexStringToByteArray(encrypted_text));
            return new String(decrypted, StandardCharsets.UTF_8);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        } catch (InvalidAlgorithmParameterException e) {
            throw new RuntimeException(e);
        } catch (NoSuchPaddingException e) {
            throw new RuntimeException(e);
        } catch (IllegalBlockSizeException e) {
            throw new RuntimeException(e);
        } catch (BadPaddingException e) {
            throw new RuntimeException(e);
        } catch (InvalidKeyException e) {
            throw new RuntimeException(e);
        }
    }
}
