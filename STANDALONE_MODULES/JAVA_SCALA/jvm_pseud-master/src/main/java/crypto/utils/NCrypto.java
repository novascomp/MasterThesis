package crypto.utils;

//L - library
//K - Key instance
public abstract class NCrypto<L, K> {

    protected final String secretText = "sss";
    protected final NCryptoAPI<L, K> cryptoAPI;

    public NCrypto(NCryptoAPI<L, K> cryptoAPI) {
        
        this.cryptoAPI = cryptoAPI;
    }

    public abstract String encrypt(String staticRandomText, String id, String colName, String plainText, boolean hsmIv);

    public abstract String decrypt(String staticRandomText, String id, String colName, String encrypted_text, boolean hsmIv);

    public String getSecretText() {
        return secretText;
    }
}
