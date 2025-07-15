"use client";
import React, { useState } from "react";
import { toast } from "react-toastify";
import { mp3Download, mp4Download } from "./api";

export default function Home() {
    const [link, setLink] = useState<string>("");

    async function handlemp3Click() {
        if (!link) {
            toast.error("Please enter a link!");
            return;
        }
        mp3Download(link);
        toast.success(`Your MP3 link: ${link}`);
    }
    async function handlemp4Click() {
        if (!link) {
            toast.error("Please enter a link!");
            return;
        }
        mp4Download(link);
        toast.success(`Your MP4 link: ${link}`);
    }

    return (
        <div className="min-h-screen flex flex-col justify-between items-center p-6 bg-gradient-to-br from-yellow-100 to-red-200 rounded-lg">
            <div className="flex flex-col items-center mt-2 w-full max-w-md text-center space-y-6">
                <div className="w-full max-w-md flex flex-col items-center mb-10 space-y-4">
                    <input
                        type="text"
                        placeholder="Enter your link..."
                        className="border-2 border-red-300 rounded-xl p-3 w-full text-center text-gray-700 focus:outline-none focus:border-red-500 placeholder-gray-400 shadow-sm"
                        value={link}
                        onChange={(e) => setLink(e.target.value)}
                    />
                    <div className="w-full max-w-md flex flex-col items-center mb-10 space-y-4">
                        <div className="flex space-x-4">
                            <button
                                onClick={handlemp3Click}
                                className="font-bold py-3 px-8 bg-red-400 hover:bg-red-500 text-white rounded-full shadow-lg transition-transform transform hover:scale-105"
                            >
                                MP3 🎵
                            </button>
                            <button
                                onClick={handlemp4Click}
                                className="font-bold py-3 px-8 bg-yellow-400 hover:bg-yellow-500 text-white rounded-full shadow-lg transition-transform transform hover:scale-105"
                            >
                                MP4 🎬
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
