import React, { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

export const Body = ({ messages, isLoading }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col flex-grow bg-gray-100 w-3/4 p-3 gap-2 overflow-y-auto mx-auto">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`flex ${msg.role === "ai" ? "justify-start" : "justify-end"}`}
        >
          <div
            className={`max-w-[70%] rounded-2xl p-3 ${
              msg.role === "ai" ? "bg-gray-300" : "bg-blue-500 text-white"
            }`}
          >
            {msg.role === "ai" ? (
              <ReactMarkdown
                components={{
                  ul: ({ children }) => <ul className="list-disc pl-4 space-y-1">{children}</ul>,
                  ol: ({ children }) => <ol className="list-decimal pl-4 space-y-1">{children}</ol>,
                  li: ({ children }) => <li className="ml-2">{children}</li>,
                  strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                  p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                  code: ({ children }) => (
                    <code className="bg-gray-200 px-1 rounded text-sm font-mono">{children}</code>
                  ),
                }}
              >
                {msg.text}
              </ReactMarkdown>
            ) : (
              msg.text
            )}
          </div>
        </div>
      ))}
      <div ref={bottomRef}></div>
    </div>
  );
};