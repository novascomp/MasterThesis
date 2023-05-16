package crypto.utils;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;

public class NCommonUtils {
    private static final String HASH_ALGORITHM = "SHA-256";

    public static String getDataForIvToHash(String staticRandomString, String id, String colName) {
        StringBuilder sb = new StringBuilder(3);
        sb.append(staticRandomString);
        sb.append(id);
        sb.append(colName);
        return sb.toString();
    }

    public static byte[] localIvComputation(String textToHash) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance(HASH_ALGORITHM);
        return Arrays.copyOfRange(digest.digest(textToHash.getBytes(StandardCharsets.UTF_8)), 0, 16);
    }

    public static byte[] concat(byte[] a, byte[] b) {
        byte[] res = new byte[a.length + b.length];
        System.arraycopy(a, 0, res, 0, a.length);
        System.arraycopy(b, 0, res, a.length, b.length);
        return res;
    }

    public static byte[] copyOf(byte[] a, int ofs, int len) {
        byte[] res = new byte[len];
        System.arraycopy(a, ofs, res, 0, len);
        return res;
    }

    //reference: https://stackoverflow.com/questions/9655181/how-to-convert-a-byte-array-to-a-hex-string-in-java
    public static String byteArrayToHex(byte[] bytes) {
        final char[] HEX_ARRAY = "0123456789ABCDEF".toCharArray();
        char[] hexChars = new char[bytes.length * 2];
        for (int j = 0; j < bytes.length; j++) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 2] = HEX_ARRAY[v >>> 4];
            hexChars[j * 2 + 1] = HEX_ARRAY[v & 0x0F];
        }
        return new String(hexChars);
    }

    //https://stackoverflow.com/questions/140131/convert-a-string-representation-of-a-hex-dump-to-a-byte-array-using-java
    public static byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i + 1), 16));
        }
        return data;
    }
}
