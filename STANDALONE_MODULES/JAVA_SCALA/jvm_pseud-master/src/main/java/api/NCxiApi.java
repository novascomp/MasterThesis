package api;

import CryptoServerAPI.CryptoServerException;
import CryptoServerCXI.CryptoServerCXI;
import api.conf.bean.NCxiApiConfBean;
import crypto.utils.NCryptoAPI;

import java.io.IOException;

public class NCxiApi implements NCryptoAPI<CryptoServerCXI, CryptoServerCXI.Key> {


    private final NCxiApiConfBean conf;


    public NCxiApi(NCxiApiConfBean conf) {
        this.conf = conf;
    }

    @Override
    public CryptoServerCXI getLibraryInstance() {
        CryptoServerCXI cxi = null;
        try {
            cxi = new CryptoServerCXI(conf.getDeviceIp(), 3000);
            cxi.setTimeout(60000);
            cxi.setKeepSessionAlive(true);
            cxi.logon(conf.getUserName(), null, conf.getPin().getBytes());
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (CryptoServerException e) {
            throw new RuntimeException(e);
        }

        return cxi;
    }

    @Override
    public CryptoServerCXI.Key getKeyInstance(CryptoServerCXI libraryInstance) {
        CryptoServerCXI.KeyAttributes attr = new CryptoServerCXI.KeyAttributes();
        attr.setAlgo(CryptoServerCXI.KEY_ALGO_AES);
        attr.setSize(conf.getKeySize());
        try {
            attr.setName(conf.getKeyLabel());
        } catch (CryptoServerException e) {
            throw new RuntimeException(e);
        }

        CryptoServerCXI.Key aesKey = null;
        try {
            aesKey = libraryInstance.findKey(attr);
            if (aesKey == null) {
                System.out.println("Generating AES Key");
                aesKey = libraryInstance.generateKey(CryptoServerCXI.FLAG_OVERWRITE, attr);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (CryptoServerException e) {
            throw new RuntimeException(e);
        }

        return aesKey;
    }
}
