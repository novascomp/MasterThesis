package me.novascomp.api;

import me.novascomp.api.model.FileXDto;
import me.novascomp.files.model.File;
import me.novascomp.files.model.FileShare;
import me.novascomp.files.rest.FileController;
import me.novascomp.files.rest.FileShareController;
import me.novascomp.files.rest.simple.SimpleFileAndShareUploadController;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.multipart.MultipartFile;

import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;

@Service
public class XfilesApiDelegateImpl implements XfilesApiDelegate {

    public final FileController fileController;
    public final FileShareController fileShareController;
    private final SimpleFileAndShareUploadController simpleFileAndShareUploadController;

    private static final Logger LOG = Logger.getLogger(XfilesApiDelegateImpl.class.getName());

    @Autowired
    public XfilesApiDelegateImpl(FileController fileController, FileShareController fileShareController, SimpleFileAndShareUploadController simpleFileAndShareUploadController) {
        this.fileController = fileController;
        this.fileShareController = fileShareController;
        this.simpleFileAndShareUploadController = simpleFileAndShareUploadController;
    }

    @Override
    public ResponseEntity<FileXDto> getFileById(String fileId) {
        FileXDto fileXDto = new FileXDto();
        ResponseEntity<File> responseEntity = (ResponseEntity<File>) fileController.getEntityById(fileId);
        File file = responseEntity.getBody();

        if (Optional.ofNullable(file).isPresent()) {
            fileXDto.setId(responseEntity.getBody().getFileId());
            fileXDto.setName(responseEntity.getBody().getName());
            FileShare fileShare = ((Page<FileShare>) this.fileShareController.getFileShares(fileId, Pageable.unpaged()).getBody()).getContent().get(0);
            fileXDto.setLink(fileShare.getLink());
            return new ResponseEntity<FileXDto>(fileXDto, HttpStatus.OK);
        }

        return new ResponseEntity<FileXDto>(HttpStatus.NOT_FOUND);
    }

    @Override
    public ResponseEntity<String> uploadFile(MultipartFile file) {
        if (Optional.ofNullable(file).isEmpty()) {
            return new ResponseEntity(HttpStatus.BAD_REQUEST);
        }

        ResponseEntity response = this.simpleFileAndShareUploadController.postFile(file, Optional.ofNullable(null));
        if (response.getStatusCode().is2xxSuccessful()) {
            final HttpHeaders headers = new HttpHeaders();
            headers.setLocation(URI.create(((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest().getRequestURL().toString().split("/")[0] + "//" + ((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest().getRequestURL().toString().split("/")[2] + "/xfiles/" + response.getHeaders().getFirst("fileId")));
            ResponseEntity newResponse = new ResponseEntity(headers, response.getStatusCode());
            return newResponse;
        }

        return response;
    }

    @Override
    public ResponseEntity<String> deleteFileById(String fileId) {
        ResponseEntity responseEntity = fileController.deleteEntityById(fileId);
        return responseEntity;
    }

    @Override
    public ResponseEntity<List<FileXDto>> listAllFiles() {
        List<FileXDto> xFiles = new ArrayList<>();
        List<File> files = fileController.getAll(Pageable.unpaged()).getContent();
        for (File file : files) {
            FileXDto fileXDto = new FileXDto();
            fileXDto.setId(file.getFileId());
            fileXDto.setName(file.getName());
            FileShare fileShare = ((Page<FileShare>) this.fileShareController.getFileShares(file.getFileId(), Pageable.unpaged()).getBody()).getContent().get(0);
            fileXDto.setLink(fileShare.getLink());
            xFiles.add(fileXDto);
        }

        return ResponseEntity.ok(xFiles);
    }

}
