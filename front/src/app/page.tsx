"use client";
import React, { useState, useEffect, useRef } from "react";
import { toast } from "react-toastify";
import { Type, Download } from "./api";

export default function Home() {
    const [link, setLink] = useState("");
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const progressInterval = useRef<NodeJS.Timeout | null>(null);

    useEffect(() => {
        return () => {
            if (progressInterval.current) {
                clearInterval(progressInterval.current);
            }
        };
    }, []);

    async function startDownload(type: Type) {
        if (!link) {
            toast.error("Please enter a link!");
            return;
        }

        setLoading(true);
        setProgress(0);

        const startTime = Date.now();
        const duration = 30000;

        progressInterval.current = setInterval(() => {
            const elapsed = Date.now() - startTime;
            const newProgress = Math.min((elapsed / duration) * 100, 100);
            setProgress(newProgress);
        }, 100);

        try {
            await Download(link, type);
        } catch (error) {
            toast.error("Download failed. Please try again.");
        } finally {
            if (progressInterval.current) {
                clearInterval(progressInterval.current);
            }
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen flex flex-col justify-between items-center p-6 bg-gradient-to-br from-yellow-100 to-red-200 rounded-lg">
            {loading && (
                <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-white/70 backdrop-blur-sm">
                    <div className="w-64 bg-gray-200 rounded-full h-4 mb-4">
                        <div
                            className="bg-red-500 h-4 rounded-full transition-all duration-100 ease-linear"
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>
                    <p className="text-xl font-semibold text-red-600">
                        Processing your request... {Math.round(progress)}%
                    </p>
                </div>
            )}

            <div className="flex flex-col items-center mt-2 w-full max-w-md text-center space-y-6">
                <input
                    type="text"
                    placeholder="Enter your link…"
                    className="border-2 border-red-300 rounded-xl p-3 w-full text-center text-gray-700 focus:outline-none focus:border-red-500 placeholder-gray-400 shadow-sm"
                    value={link}
                    onChange={(e) => setLink(e.target.value)}
                />
                <div className="flex space-x-4">
                    <button
                        onClick={() => startDownload(Type.MP3)}
                        className="font-bold py-3 px-8 bg-red-400 hover:bg-red-500 text-white rounded-full shadow-lg transition-transform transform hover:scale-105"
                    >
                        MP3 🎵
                    </button>
                    <button
                        onClick={() => startDownload(Type.MP4)}
                        className="font-bold py-3 px-8 bg-yellow-400 hover:bg-yellow-500 text-white rounded-full shadow-lg transition-transform transform hover:scale-105"
                    >
                        MP4 🎬
                    </button>
                </div>
            </div>
        </div>
    );
}
