import api.NCxiApi;
import api.NJceApi;
import api.conf.NGeneralApiConf;
import api.conf.bean.NApiOptionConfBean;
import api.conf.bean.NCxiApiConfBean;
import api.conf.bean.NJceApiConfBean;
import api.conf.bean.NPkcs11ApiConfBean;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigBeanFactory;
import com.typesafe.config.ConfigFactory;
import crypto.cxi.NCryptoCXI;
import api.NPkcs11Api;
import crypto.jce.NCryptoJCE;
import crypto.pkcs11.NCryptoPKCS11;
import crypto.pkcs11.helper.SessionHandler;
import crypto.utils.Input;
import crypto.utils.NCrypto;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

// https://crypto-hsm.com/wp-content/uploads/Utimaco_PKCS11.pdf
public class Main {

    private static final String CXI = "cxi";
    private static final String JCE = "jce";
    private static final String PKCS11 = "pkcs11";

    private static final String CONF_API_DIR = "conf/api";
    private static final String CONF_INPUT_DIR = "conf/INPUT";

    private static final String GLOBAL = "global";
    private static final String OPTION = "option";

    private static final String TEST_FILE_NAME = "cisty.csv";

    private static Config globalConf;
    private static Config inputConf;

    public static void main(String[] args) throws IOException {

        NCrypto crypto = initCryptoApi();
        copyFileFromResourcesToLocalFileSystemAndGetPath(TEST_FILE_NAME);
        String plainText = new String(Input.readFile(new File(TEST_FILE_NAME)));
        System.out.println(plainText);

        String STATIC_RANDOM_TEXT = "STATIC_RANDOM_TEXT";
        String USER_ID = "USER_ID";
        String TEST_COL_NAME = "TEST_COL_NAME";


        //System.out.println("Plain text: " + plainText);
        String enc = crypto.encrypt(STATIC_RANDOM_TEXT, USER_ID, TEST_COL_NAME, plainText, false);
        System.out.println("Encrypted: " + enc);
        String dec = crypto.decrypt(STATIC_RANDOM_TEXT, USER_ID, TEST_COL_NAME, enc, false);
        System.out.println("Decrypted: " + dec);
    }

    public static NCrypto initCryptoApi() {
        loadGlobalConf();
        NApiOptionConfBean optionConf = loadGlobalConf();
        return getCryptoInstance(getApiEnum(System.getProperty("api")), System.getProperty("env"), System.getProperty("without_hsm"));
    }

    private static NApiOptionConfBean loadGlobalConf() {
        globalConf = ConfigFactory.load(CONF_API_DIR + "/" + GLOBAL + ".conf");
        inputConf = ConfigFactory.load(CONF_INPUT_DIR + "/" + OPTION + ".conf");
        //inputConf = loadOptionFromFile("C:\\Users\\novotnyp2\\Desktop\\test.conf");
        NApiOptionConfBean option = ConfigBeanFactory.create(inputConf.getConfig(OPTION), NApiOptionConfBean.class);
        return option;
    }

    private static Config loadOptionFromFile(String filePath) {
        Config config = null;
        File initialFile = new File(filePath);
        InputStream fileInputStream = null;
        try {
            fileInputStream = new FileInputStream(initialFile);
            config = parseFromFileInputStream(fileInputStream);
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
        return config;
    }

    private static Config parseFromFileInputStream(InputStream inputStream) {

        Config config = null;
        try {
            InputStreamReader reader = new InputStreamReader(inputStream);
            config = ConfigFactory.parseReader(reader);
            reader.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return config;
    }

    private static SupportedCryptoAPI getApiEnum(String api) {
        if (api.equals(CXI)) {
            return SupportedCryptoAPI.CXI;
        } else if (api.equals(PKCS11)) {
            return SupportedCryptoAPI.PKCS11;
        } else if (api.equals(JCE)) {
            return SupportedCryptoAPI.JCE;
        }
        throw new UnsupportedOperationException();
    }

    private static void copyFileFromResourcesToLocalFileSystemAndGetPath(String fileName) {
        try {
            try (InputStream inputStream = SessionHandler.class.getResourceAsStream("/" + fileName)) {
                File file = new File(fileName);
                copyInputStreamToFile(inputStream, file);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static void copyInputStreamToFile(InputStream inputStream, File file) throws IOException {

        // append = false
        try (FileOutputStream outputStream = new FileOutputStream(file, false)) {
            int read;
            byte[] bytes = new byte[1024];
            while ((read = inputStream.read(bytes)) != -1) {
                outputStream.write(bytes, 0, read);
            }
        }

    }

    //https://stackoverflow.com/questions/38123764/how-to-load-typesafe-configfactory-from-file-on-hdfs
    public static NCrypto getCryptoInstance(SupportedCryptoAPI api, String env, String withoutHSM) {

        Config conf = ConfigFactory.load(CONF_API_DIR + "/" + env);
        NCrypto cryptoApi = null;
        if (api.equals(SupportedCryptoAPI.CXI)) {
            NCxiApiConfBean confBean = ConfigBeanFactory.create(conf.getConfig(CXI).withFallback(conf).withFallback(globalConf.getConfig(CXI)), NCxiApiConfBean.class);
            cryptoApi = new NCryptoCXI(new NCxiApi(confBean));
        } else if (api.equals(SupportedCryptoAPI.PKCS11)) {
            NPkcs11ApiConfBean confBean = ConfigBeanFactory.create(conf.getConfig(PKCS11).withFallback(conf).withFallback(globalConf.getConfig(PKCS11)), NPkcs11ApiConfBean.class);
            copyFileFromResourcesToLocalFileSystemAndGetPath(confBean.getLinuxModuleFileName());
            copyFileFromResourcesToLocalFileSystemAndGetPath(confBean.getWindowsModuleFileName());
            copyFileFromResourcesToLocalFileSystemAndGetPath(confBean.getConfFileName());
            writeToConfFile(confBean);
            cryptoApi = new NCryptoPKCS11(new NPkcs11Api(confBean));
        } else if (api.equals(SupportedCryptoAPI.JCE)) {
            NJceApiConfBean confBean = ConfigBeanFactory.create(conf.getConfig(JCE).withFallback(conf).withFallback(globalConf.getConfig(JCE)), NJceApiConfBean.class);
            copyFileFromResourcesToLocalFileSystemAndGetPath(confBean.getConfFileName());
            copyFileFromResourcesToLocalFileSystemAndGetPath(NCryptoJCE.LOCAL_KEY_NAME);
            writeToConfFile(confBean);
            cryptoApi = new NCryptoJCE(new NJceApi(confBean), Boolean.valueOf(withoutHSM));
        }
        return cryptoApi;
    }

    //https://stackoverflow.com/questions/1625234/how-to-append-text-to-an-existing-file-in-java
    private static void writeToConfFile(NGeneralApiConf confBean) {
        try {
            Files.write(Paths.get(confBean.getConfFileName()), ("Device = " + confBean.getDeviceIp()).getBytes(), StandardOpenOption.APPEND);
        } catch (IOException e) {
            System.out.printf(String.valueOf(e));
        }
    }
}
