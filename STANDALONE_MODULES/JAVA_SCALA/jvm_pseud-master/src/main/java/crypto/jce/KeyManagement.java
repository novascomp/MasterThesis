package crypto.jce;

import CryptoServerJCE.CryptoServerKeyGenParameterSpec;
import api.helper.NJceProvider;

import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.security.*;
import java.util.Date;
import java.util.Enumeration;

public class KeyManagement {

    private final NJceProvider provider;

    public KeyManagement(NJceProvider provider) {
        this.provider = provider;
    }

    public SecretKey findKeyByName(String keyName) {
        SecretKey key = null;
        try {
            key = (SecretKey)provider.getKeyStore().getKey(keyName, new char[]{});
        } catch (Exception exception) {
            System.out.println("Not Found EX");
        }
        if (key == null) {
            System.out.println("Not Found");
        }
        return key;
    }

    public SecretKey findKeyByNameOrGenerate(String keyName) throws InvalidAlgorithmParameterException, NoSuchAlgorithmException, KeyStoreException {
        SecretKey key = (SecretKey) findKeyByName(keyName);
        if (key == null) {
            System.out.println("Generating AES Key");
            key = generateKey(keyName, 256);
        }
        return key;
    }

    private static CryptoServerKeyGenParameterSpec specifyParam(Integer keySize) {
        CryptoServerKeyGenParameterSpec spec = new CryptoServerKeyGenParameterSpec(keySize);
        spec.setPlainExportable(false);
        spec.setExportable(false);
        return spec;
    }

    public SecretKey generateKey(String keyName, Integer keySize) throws NoSuchAlgorithmException, InvalidAlgorithmParameterException, KeyStoreException {
        KeyGenerator kg = KeyGenerator.getInstance("AES", provider.getProvider());
        kg.init(specifyParam(keySize), null);
        SecretKey key = kg.generateKey();
        System.out.println(key.toString());
        provider.getKeyStore().setKeyEntry(keyName, key, null, null);
        return key;
    }

    public void deleteAllKeys() throws KeyStoreException {
        Enumeration<String> enumeration = provider.getKeyStore().aliases();
        while (enumeration.hasMoreElements()) {
            provider.getKeyStore().deleteEntry(enumeration.nextElement());
        }
    }

    public void listAllKeys() throws KeyStoreException {
        Enumeration<String> enumeration = provider.getKeyStore().aliases();
        while (enumeration.hasMoreElements()) {
            String name = enumeration.nextElement();
            Date date = provider.getKeyStore().getCreationDate(name);
            String type;

            if (provider.getKeyStore().isKeyEntry(name))
                type = "Key";
            else
                type = "Other";

            System.out.println(String.format("%-12s %-20s %s", type, name, date));
        }
    }
}
