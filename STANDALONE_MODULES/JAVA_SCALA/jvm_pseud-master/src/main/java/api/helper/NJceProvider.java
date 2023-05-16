package api.helper;

import CryptoServerAPI.CryptoServerException;
import CryptoServerJCE.CryptoServerProvider;
import api.conf.bean.NJceApiConfBean;

import java.io.IOException;
import java.security.*;
import java.security.cert.CertificateException;

public class NJceProvider {

    public static final String CONFIG = "CryptoServer.cfg";


    private NJceApiConfBean conf;

    private final CryptoServerProvider provider;
    private KeyStore ks;


    public NJceProvider(NJceApiConfBean conf) throws CryptoServerException, IOException, CertificateException, KeyStoreException, NoSuchAlgorithmException {
        this.conf = conf;
        this.provider = new CryptoServerProvider(conf.getConfFileName());
        authenticate();
        loadKeyStore();
    }

    public void loadKeyStore() throws KeyStoreException, CertificateException, IOException, NoSuchAlgorithmException {
        ks = KeyStore.getInstance("CryptoServer", provider);
        ks.load(null, null);
        System.out.println(ks.getType());
    }

    private void authenticate() throws CryptoServerException, IOException {
        provider.loginPassword(conf.getUserName(), conf.getPin());
    }

    public CryptoServerProvider getProvider() {
        return provider;
    }

    public KeyStore getKeyStore() {
        return ks;
    }

}
