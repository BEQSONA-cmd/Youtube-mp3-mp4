import axios from "axios";

const HOST = process.env.NEXT_PUBLIC_HOST || "http://localhost:8080";

export async function mp3Download(link: string) {
    try {
        const { data } = await axios.get(`${HOST}/api/downloadMP3`, {
            params: { link },
            responseType: "blob",
        });

        const url = window.URL.createObjectURL(new Blob([data]));
        const a = document.createElement("a");
        a.href = url;
        a.download = "video.mp3";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function mp4Download(link: string) {
    try {
        const { data } = await axios.get(`${HOST}/api/downloadMP4`, {
            params: { link },
            responseType: "blob",
        });

        const url = window.URL.createObjectURL(new Blob([data]));
        const a = document.createElement("a");
        a.href = url;
        a.download = "video.mp4";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    } catch (error) {
        console.error(error);
        throw error;
    }
}
