package me.novascomp.files.services;

import me.novascomp.files.config.NVFUtils;
import me.novascomp.files.factory.RequestorFactory;
import me.novascomp.files.model.File;
import me.novascomp.files.model.Folder;
import me.novascomp.files.model.Server;
import me.novascomp.files.model.User;
import me.novascomp.files.repository.FileRepository;
import me.novascomp.files.server.webdav.FileWebdavRequestor;
import me.novascomp.files.server.webdav.response.WebDavFileResponse;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.HttpStatus;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@RunWith(MockitoJUnitRunner.class)
class FileServiceTest {

    @Mock
    private ServerService serverService;
    @Mock
    private UserService userService;
    @Mock
    private FolderService folderService;

    @Mock
    private FileRepository fileRepository;

    @Mock
    private NVFUtils nvfUtils;

    @InjectMocks
    private FileService fileService;

    private Server server;
    private Folder folder;
    private User user;
    MultipartFile file;

    FileWebdavRequestor webdavRequestor;
    RequestorFactory requestorFactory;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.initMocks(this);
        fileService.setNvfUtils(nvfUtils);
        fileService.setRepository(fileRepository);
        init();
        webdavRequestor = Mockito.spy(new FileWebdavRequestor(nvfUtils, server));
        requestorFactory = Mockito.spy(new RequestorFactory());
        fileService.setRequestorFactory(requestorFactory);
        doReturn(webdavRequestor).when(requestorFactory).getFileWebdavRequestor(any(), any());
    }

    @AfterEach
    void tearDown() {
    }

    @Test
    void addFile() {
        doReturn(HttpStatus.CREATED).when(webdavRequestor).createFile(any(), any(), any());

        WebDavFileResponse webDavFileResponse = fileService.addFile(file, server.getServerId(), folder.getFolderId(), user.getUserId());
        assertEquals(true, webDavFileResponse.getModel().isPresent());
        assertEquals(true, webDavFileResponse.getHttpStatus().is2xxSuccessful());
        assertEquals(true, webDavFileResponse.getRequirement().isValid());
        assertEquals(server.getServerId(), webDavFileResponse.getRequirement().getServer().get().getServerId());

        File fileModel = webDavFileResponse.getModel().get();
        assertEquals(true, Optional.ofNullable(fileModel).isPresent());

        assertNotNull(fileModel.getServer());
        assertNotNull(fileModel.getFolder());
        assertNotNull(fileModel.getUser());

        assertEquals(server.getServerId(), fileModel.getServer().getServerId());
        assertEquals(folder.getFolderId(), fileModel.getFolder().getFolderId());
        assertEquals(file.getOriginalFilename(), fileModel.getName());

        verify(fileRepository).save(fileModel);
    }

    @Test
    void removeFile() {
        doReturn(HttpStatus.NO_CONTENT).when(webdavRequestor).createFile(any(), any(), any());
        File fileModel = new File();
        fileService.delete(fileModel);
        verify(fileRepository).delete(fileModel);
    }

    private void init() {
        byte[] content = new byte[10];

        this.file = new MockMultipartFile("Test file", "Test Original file name", null, content);
        this.server = mockServer();
        this.folder = mockFolder(server.getServerId());
        this.user = mockUser();

        when(serverService.findById(any())).thenReturn(Optional.of(server));
        when(folderService.findById(any())).thenReturn(Optional.of(folder));
        when(userService.findById(any())).thenReturn(Optional.of(user));
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

    private Folder mockFolder(String serverId) {
        Folder folder = new Folder();
        folder.setFolderId(UUID.randomUUID().toString());
        folder.setName("Test-Folder");
        return folder;
    }

    private User mockUser() {
        User user = new User();
        user.setUserId(UUID.randomUUID().toString());
        user.setUid(UUID.randomUUID().toString());
        return user;
    }

}