package crypto.cxi;

import CryptoServerAPI.*;
import CryptoServerCXI.*;
import crypto.utils.NCommonUtils;
import crypto.utils.NCrypto;
import crypto.utils.NCryptoAPI;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;

public class NCryptoCXI extends NCrypto<CryptoServerCXI, CryptoServerCXI.Key> {

    private final CryptoServerCXI cxi;
    private final CryptoServerCXI.Key aesKey;

    public NCryptoCXI(NCryptoAPI cryptoAPI) {
        super(cryptoAPI);
        cxi = super.cryptoAPI.getLibraryInstance();
        aesKey = super.cryptoAPI.getKeyInstance(cxi);
    }

    @Override
    public String encrypt(String staticRandomText, String id, String colName, String plainText, boolean hsmIv) {


        byte[] crypto = new byte[0];
        CryptoServerCXI.ByteArray iv = getCustomIv(NCommonUtils.getDataForIvToHash(staticRandomText, id, colName), hsmIv, cxi);

        int mech = CryptoServerCXI.MECH_MODE_ENCRYPT | CryptoServerCXI.MECH_CHAIN_CBC | CryptoServerCXI.MECH_PAD_PKCS5;

        try {
            crypto = cxi.crypt(aesKey, mech, null, plainText.getBytes(StandardCharsets.UTF_8), iv);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (CryptoServerException e) {
            throw new RuntimeException(e);
        }

        return NCommonUtils.byteArrayToHex(crypto);
    }

    @Override
    public String decrypt(String staticRandomText, String id, String colName, String encrypted_text, boolean hsmIv) {
        CryptoServerCXI.ByteArray iv = getCustomIv(NCommonUtils.getDataForIvToHash(staticRandomText, id, colName), hsmIv, cxi);

        int mech = CryptoServerCXI.MECH_MODE_DECRYPT | CryptoServerCXI.MECH_CHAIN_CBC | CryptoServerCXI.MECH_PAD_PKCS5;
        try {
            byte[] plain = cxi.crypt(aesKey, mech, null, NCommonUtils.hexStringToByteArray(encrypted_text), iv);
            return new String(plain, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (CryptoServerException e) {
            throw new RuntimeException(e);
        }
    }

    private static CryptoServerCXI.ByteArray getCustomIv(String textToHash, boolean hsmIv, CryptoServerCXI cxi) {
        try {
            if (hsmIv) {
                return new CryptoServerCXI.ByteArray(hsmIvComputation(textToHash, cxi));
            }
            return new CryptoServerCXI.ByteArray(NCommonUtils.localIvComputation(textToHash));
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        } catch (CryptoServerException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static byte[] hsmIvComputation(String textToHash, CryptoServerCXI cxi) throws CryptoServerException, IOException {

        byte[] data = textToHash.getBytes(StandardCharsets.UTF_8);
        int data_len = data.length;
        int flags = CryptoServerCXI.FLAG_HASH_PART;
        int mech = CryptoServerCXI.MECH_MODE_HASH | CryptoServerCXI.MECH_HASH_ALGO_SHA256;
        int len = 64;
        int ofs = 0;
        byte[] hash = null;

        while (data_len > 0) {
            if (data_len <= 64) {
                flags = 0;
                len = data_len;
            }

            byte[] chunk = NCommonUtils.copyOf(data, ofs, len);
            hash = cxi.computeHash(flags, mech, chunk, hash, null);

            data_len -= len;
            ofs += len;
        }

        return Arrays.copyOfRange(hash, 0, 16);
    }
}