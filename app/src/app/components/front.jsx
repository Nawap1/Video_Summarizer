"use client";
import React, { useState } from "react";
import { Headphones, Send } from "lucide-react";

const EchoSummarizeFrontPage = () => {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const fetchSummary = async (youtubeUrl) => {
    try {
      const response = await fetch("http://localhost:8000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: youtubeUrl }),
      });
      if (!response.ok) {
        console.error(`HTTP Error: ${response.status}`);
        throw new Error(`HTTP Error: ${response.status}`);
      }
      const data = await response.json();
      return data.summary;
    } catch (error) {
      console.error("Error:", error);
      return "An error occurred while fetching the summary.";
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const fetchedSummary = await fetchSummary(url);
    setSummary(fetchedSummary);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-700 via-indigo-800 to-blue-900 flex items-center justify-center p-4">
      <div className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-3xl p-8 w-full max-w-3xl shadow-2xl">
        <div className="flex flex-col items-center mb-12">
          <div className="bg-purple-500 rounded-full p-4 mb-4">
            <Headphones size={48} className="text-white" />
          </div>
          <h1 className="text-5xl font-bold text-white mb-4">EchoSummarize</h1>
          <p className="text-center text-xl text-purple-200">
            Distill YouTube videos into concise summaries with AI magic.
          </p>
        </div>
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="relative">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste your YouTube URL here..."
              className="w-full px-6 py-4 bg-white bg-opacity-20 rounded-full text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:bg-opacity-30 transition-all duration-300"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="absolute right-2 top-2 px-6 py-2 bg-purple-500 hover:bg-purple-400 text-white font-semibold rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 focus:ring-offset-purple-700 disabled:bg-purple-800 disabled:cursor-not-allowed"
            >
              {isLoading ? "Processing..." : <Send size={24} />}
            </button>
          </div>
        </form>
        {summary && (
          <div className="bg-white bg-opacity-20 rounded-2xl p-6 backdrop-filter backdrop-blur-sm">
            <h2 className="text-2xl font-semibold mb-4 text-purple-200">
              Summary:
            </h2>
            {/* Render the summary with line breaks */}
            <p className="text-white leading-relaxed">
              {summary.split("\n").map((line, index) => (
                <span key={index}>
                  {line}
                  <br />
                </span>
              ))}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default EchoSummarizeFrontPage;
