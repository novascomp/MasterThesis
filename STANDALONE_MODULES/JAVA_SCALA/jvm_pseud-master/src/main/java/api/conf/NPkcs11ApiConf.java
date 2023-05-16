package api.conf;

import java.util.Optional;

public interface NPkcs11ApiConf extends NGeneralApiConf {
    String getLinuxModuleFileName();

    String getWindowsModuleFileName();

    String getKeyId();

    String getPathToLinuxModule();
}
