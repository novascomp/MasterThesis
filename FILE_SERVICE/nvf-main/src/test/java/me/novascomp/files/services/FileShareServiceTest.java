package me.novascomp.files.services;

import com.fasterxml.jackson.databind.ObjectMapper;
import me.novascomp.files.config.NVFUtils;
import me.novascomp.files.download.DownloadSessionService;
import me.novascomp.files.factory.RequestorFactory;
import me.novascomp.files.factory.RequirementFactory;
import me.novascomp.files.model.File;
import me.novascomp.files.model.Server;
import me.novascomp.files.repository.FileShareRepository;
import me.novascomp.files.server.ocs.FileShareOcsRequestor;
import me.novascomp.files.server.ocs.response.OcsFileShareResponse;
import me.novascomp.files.services.requirement.FileShareRequirement;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.verify;

@RunWith(MockitoJUnitRunner.class)
class FileShareServiceTest {

    @Mock
    FileService fileService;

    @Mock
    DownloadSessionService downloadService;

    @Mock
    private NVFUtils nvfUtils;

    @Mock
    private ObjectMapper objectMapper;

    @Mock
    private FileShareRepository fileShareRepository;

    RequestorFactory requestorFactory;
    RequirementFactory requirementFactory;

    @InjectMocks
    private FileShareService fileShareService;

    private FileShareOcsRequestor fileShareOcsRequestor;

    private Server server;
    private File file;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.initMocks(this);
        fileShareService.setNvfUtils(nvfUtils);
        fileShareService.setRepository(fileShareRepository);
        init();
        fileShareOcsRequestor = Mockito.spy(new FileShareOcsRequestor(nvfUtils, objectMapper, server));
        requestorFactory = Mockito.spy(new RequestorFactory());
        requirementFactory = Mockito.spy(new RequirementFactory());
        fileShareService.setRequestorFactory(requestorFactory);
        fileShareService.setRequirementFactory(requirementFactory);
    }

    @Test
    void addFileShareBadRequestTest() {
        FileShareRequirement fileShareRequirement = Mockito.spy(new FileShareRequirement(null));
        doReturn(fileShareRequirement).when(requirementFactory).getRequirement(any(), any());
        doReturn(false).when(fileShareRequirement).isValid();
        OcsFileShareResponse ocsFileShareResponse = fileShareService.addFileShare(file);
        assertEquals(HttpStatus.BAD_REQUEST, ocsFileShareResponse.getHttpStatus());
    }

    @Test
    void findByFileId() {
        fileShareService.findByFileId(file, Pageable.unpaged());
        verify(fileShareRepository).findByFileId(any(), any());
    }

    private void init() {
        this.server = mockServer();
        this.file = new File();
    }

    private Server mockServer() {
        Server server = new Server();
        server.setServerId(UUID.randomUUID().toString());
        server.setBaseUrl("http://BASE-URL");
        server.setUsername("SERVER-USERNAME");
        server.setPassword("SERVER-PASSWORD");
        server.setOcsPath("SEVER-OCS-PATH");
        server.setWebdavPath("WEBDAV-PATH");
        return server;
    }
}