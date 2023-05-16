package api.conf.bean;

import api.conf.NPkcs11ApiConf;

public class NPkcs11ApiConfBean extends NGeneralApiConfBean implements NPkcs11ApiConf {

    private String linuxModuleFileName;

    private String windowsModuleFileName;

    private String keyId;

    private String pathToLinuxModule;

    @Override
    public String getLinuxModuleFileName() {
        return linuxModuleFileName;
    }

    @Override
    public String getWindowsModuleFileName() {
        return windowsModuleFileName;
    }


    @Override
    public String getKeyId() {
        return keyId;
    }

    @Override
    public String getPathToLinuxModule() {
        return pathToLinuxModule;
    }

    public void setLinuxModuleFileName(String linuxModuleFileName) {
        this.linuxModuleFileName = linuxModuleFileName;
    }

    public void setWindowsModuleFileName(String windowsModuleFileName) {
        this.windowsModuleFileName = windowsModuleFileName;
    }

    public void setKeyId(String keyId) {
        this.keyId = keyId;
        if (keyId.equals("")) {
            this.keyId = null;
        }
    }

    public void setPathToLinuxModule(String pathToLinuxModule) {
        this.pathToLinuxModule = pathToLinuxModule;
    }
}
