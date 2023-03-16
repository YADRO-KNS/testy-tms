import axiosTMS from "./axiosTMS";
import axios from "axios";
import localStorageTMS from "./localStorageTMS";

export default class AttachmentService {
    static filenameReduce = (filename: string) => {
        const maxLengthOfName = 35;
        if (filename.length > maxLengthOfName) {
            return filename.slice(0, maxLengthOfName) + "..."
        } else {
            return filename
        }
    }

    private static postAttachment(file: File, objectId: number, contentType: number, token: string | null) {
        const formData = new FormData();
        const projectId = localStorageTMS.getCurrentProject().id;

        formData.append("project", projectId.toString());
        formData.append("comment", "");
        formData.append("content_type", contentType.toString());
        formData.append("object_id", objectId.toString());
        formData.append("file", file, file.name);

        return axios({
            method: "post",
            baseURL: process.env.REACT_APP_API_URL,
            url: "api/v1/attachments/",
            data: formData,
            headers: {"Content-Type": "multipart/form-data", Authorization: 'Bearer ' + token}
        })
    }

    static postAttachments(filesSelected: File[] | undefined, objectId: number, contentType: number) {
        if (!filesSelected) return new Promise<void>((resolve) => {resolve()});

        const token = localStorageTMS.getAccessToken();
        return new Promise<void>(async (resolve) => {
            await Promise.all(filesSelected.map(async (file) => {
                await this.postAttachment(file, objectId, contentType, token)
                    .catch((e) => {
                        console.log(e)
                    })
            }))
            resolve()
        })
    }

    static getAttachments() {
        return axiosTMS.get("api/v1/attachments/")
    }
}