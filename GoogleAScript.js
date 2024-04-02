function doPost(e) {
    var data = Utilities.base64Decode(e.parameters.data);
    var blob = Utilities.newBlob(data, e.parameters.mimetype, e.parameters.filename);
    var fileID = DriveApp.getFolderById(e.parameters.folderId).createFile(blob).getId();
    return ContentService.createTextOutput(fileID);
    }