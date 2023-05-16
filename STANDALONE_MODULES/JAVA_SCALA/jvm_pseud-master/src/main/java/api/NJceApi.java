package api;

import CryptoServerAPI.CryptoServerException;
import api.conf.bean.NJceApiConfBean;
import api.helper.NJceProvider;
import crypto.jce.KeyManagement;
import crypto.utils.NCryptoAPI;

import java.io.IOException;
import java.security.InvalidAlgorithmParameterException;
import java.security.Key;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;

public class NJceApi implements NCryptoAPI<NJceProvider, Key> {

    private NJceApiConfBean conf;

    public NJceApi(NJceApiConfBean conf) {
        this.conf = conf;
    }

    @Override
    public NJceProvider getLibraryInstance() {
        try {
            return new NJceProvider(conf);
        } catch (CryptoServerException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (CertificateException e) {
            throw new RuntimeException(e);
        } catch (KeyStoreException e) {
            throw new RuntimeException(e);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Key getKeyInstance(NJceProvider libraryInstance) {
        try {
            return new KeyManagement(libraryInstance).findKeyByNameOrGenerate(conf.getKeyLabel());
        } catch (InvalidAlgorithmParameterException e) {
            throw new RuntimeException(e);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        } catch (KeyStoreException e) {
            throw new RuntimeException(e);
        }
    }
}
