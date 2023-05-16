package me.novascomp.files.version;

public class NAppInformationImpl implements iNAppInformation {

    private final String creator;
    private final String email;
    private final iNVersion version;

    public NAppInformationImpl(String creator, String email, iNVersion version) {
        this.creator = creator;
        this.email = email;
        this.version = version;
    }

    @Override
    public String getCreator() {
        return creator;
    }

    @Override
    public String getEmail() {
        return email;
    }

    @Override
    public iNVersion getVersion() {
        return version;
    }

    @Override
    public String toString() {
        return "NAppInformationImpl{" + "creator=" + creator + ", email=" + email + " + , version=" + version.toString() + '}';
    }

}
