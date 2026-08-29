import React, { useState } from "react";

export const Footer = ({ onSendMessage }) => {
  //user type stored
  const [InputValue, setInputValue] = useState("");
  //send button
  const handleSend = () => {
    if (InputValue.trim()) {
      //user typed something
      onSendMessage(InputValue);
      //clear input box
      setInputValue("");
    }
  };
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };
  return (
    <>
      <div className="w-3/4 bg-gray-200 sticky flex items-center mx-auto gap-3">
        <input
          className="border border-2 px-3 rounded-full flex-1 h-14 border-black flex items-center justify-center"
          type="text"
          placeholder="Type your message..."
          value={InputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
        />

        <div onClick={handleSend} className="border rounded-full h-14 w-14 flex items-center justify-center bg-green-400 cursor-pointer">
          <span className="material-symbols-outlined justify-end">send</span>
        </div>
      </div>
    </>
  );
};
