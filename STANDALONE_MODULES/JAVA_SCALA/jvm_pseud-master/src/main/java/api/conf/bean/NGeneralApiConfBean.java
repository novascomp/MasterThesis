package api.conf.bean;

import api.conf.NGeneralApiConf;

public abstract class NGeneralApiConfBean implements NGeneralApiConf {

    protected String deviceIp;

    protected String userName;
    protected String pin;

    protected String keyLabel;

    protected String confFileName;

    @Override
    public String getDeviceIp() {
        return deviceIp;
    }

    @Override
    public String getUserName() {
        return userName;
    }

    @Override
    public String getPin() {
        return pin;
    }

    @Override
    public String getKeyLabel() {
        return keyLabel;
    }

    @Override
    public String getConfFileName() {
        return confFileName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public void setPin(String pin) {
        this.pin = pin;
    }

    public void setKeyLabel(String keyLabel) {
        this.keyLabel = keyLabel;
    }

    public void setConfFileName(String confFileName) {
        this.confFileName = confFileName;
    }

    public void setDeviceIp(String deviceIp) {
        this.deviceIp = deviceIp;
    }

}
