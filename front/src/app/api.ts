import axios from "axios";
import { toast } from "react-toastify";

const HOST = process.env.NEXT_PUBLIC_HOST;

export enum Type {
    MP3 = "mp3",
    MP4 = "mp4",
}

export async function Download(link: string, type: Type) {
    let endpoint = "";
    let filename = "";
    if (type === Type.MP3) {
        endpoint = `${HOST}/flask/api/downloadMP3`;
        filename = "audio.mp3";
    } else if (type === Type.MP4) {
        endpoint = `${HOST}/flask/api/downloadMP4`;
        filename = "video.mp4";
    } else {
        throw new Error("Unsupported type");
    }

    try {
        const response = await axios.get(`${endpoint}`, {
            params: { link },
            responseType: "blob",
        });

        const cd = response.headers["content-disposition"];

        if (cd) {
            const utf8Match = cd.match(/filename\*=UTF-8''([^;\n]+)/i);
            if (utf8Match) {
                filename = decodeURIComponent(utf8Match[1]);
            } else {
                const asciiMatch = cd.match(/filename="([^"]+)"/i);
                if (asciiMatch) {
                    filename = asciiMatch[1];
                }
            }
        }

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    } catch (error) {
        toast.error("Download failed. Please try again.");
        throw error;
    }
}
