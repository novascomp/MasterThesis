package me.novascomp.files.factory;

import me.novascomp.files.model.File;
import me.novascomp.files.model.FileShare;
import me.novascomp.files.services.FileService;
import me.novascomp.files.services.FileShareService;
import me.novascomp.files.services.requirement.FileShareDownloadRequirement;
import me.novascomp.files.services.requirement.FileShareRequirement;

import java.util.Optional;

public class RequirementFactory {

    public FileShareRequirement getRequirement(FileService fileService, String fileID) {
        final Optional<File> file = fileService.findById(fileID);
        return new FileShareRequirement(file);
    }

    public FileShareDownloadRequirement getDownloadRequirement(FileShareService fileShareService, String fileShareID) {
        final Optional<FileShare> fileShare = fileShareService.findById(fileShareID);
        return new FileShareDownloadRequirement(fileShare);
    }
}
