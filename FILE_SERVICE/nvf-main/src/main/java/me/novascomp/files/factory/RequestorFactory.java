package me.novascomp.files.factory;

import com.fasterxml.jackson.databind.ObjectMapper;
import me.novascomp.files.config.NVFUtils;
import me.novascomp.files.model.Server;
import me.novascomp.files.server.ocs.FileShareOcsRequestor;
import me.novascomp.files.server.webdav.FileWebdavRequestor;

public class RequestorFactory {

    public FileWebdavRequestor getFileWebdavRequestor(NVFUtils nvfUtils, Server server) {
        return new FileWebdavRequestor(nvfUtils, server);
    }
    public FileShareOcsRequestor getFileShareOcsRequestor(NVFUtils nvfUtils, ObjectMapper objectMapper, Server server) {
        return new FileShareOcsRequestor(nvfUtils, objectMapper, server);
    }
}
