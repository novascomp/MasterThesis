package crypto.pkcs11.helper;

import iaik.pkcs.pkcs11.*;
import iaik.pkcs.pkcs11.Module;

import java.io.IOException;

public class SessionHandler {
    public static Session initSession(boolean init, String userPIN, String modulePath) throws IOException, TokenException {

        Module pkcs11Module = Module.getInstance(modulePath);

        if (init) {
            pkcs11Module.initialize(null);
        }

        Slot[] slotsWithTokens = pkcs11Module.getSlotList(Module.SlotRequirement.TOKEN_PRESENT);
        Token token = slotsWithTokens[0].getToken();
        Session session = token.openSession(Token.SessionType.SERIAL_SESSION, Token.SessionReadWriteBehavior.RW_SESSION, null, null);
        session.login(Session.UserType.USER, userPIN.toCharArray());
        return session;
    }
}
