// app/components/ChatWidget.tsx
'use client';
import React, { useState, useEffect, useRef } from 'react';

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{ user: string; bot: string | null }[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [waitingForResponse, setWaitingForResponse] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const toggleChatWindow = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() !== '') {
      setWaitingForResponse(true);
      setMessages((prevMessages) => [...prevMessages, { user: inputValue, bot: null }]);
      setInputValue('');
      try {
        const response = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ message: inputValue }),
        });
        if (response.ok) {
          const data = await response.json();
          setMessages((prevMessages) => {
            const newMessages = [...prevMessages];
            newMessages[newMessages.length - 1].bot = data.response;
            return newMessages;
          });
        } else {
          const data = await response.json();
          console.error('Error from Flask backend:', data.error);
        }
        setWaitingForResponse(false);
      } catch (error) {
        console.error('Error sending message:', error);
        setWaitingForResponse(false);
      }
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <>
      <button
        className="fixed bottom-4 right-4 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-full shadow-lg transition duration-300 ease-in-out"
        onClick={toggleChatWindow}
      >
        Chat
      </button>
      {isOpen && (
        <div className="fixed bottom-20 right-4 w-[600px] h-[600px] bg-white border border-gray-300 rounded-lg shadow-lg overflow-hidden">
          <div className="px-4 py-2 bg-gray-100 border-b border-gray-300">
            <h2 className="text-sm font-semibold">Chat</h2>
          </div>
          <div className="p-4 overflow-y-auto" style={{ height: 'calc(100% - 104px)' }} ref={chatContainerRef}>
            {messages.map((message, index) => (
              <div key={index}>
                {message.user && (
                  <div className="mb-2 text-left">
                    <p className="inline-block px-3 py-2 rounded-lg bg-gray-200 text-gray-800 text-sm">
                      {message.user}
                    </p>
                  </div>
                )}
                {message.bot && (
                  <div className="mb-2 text-right">
                    <p className="inline-block px-3 py-2 rounded-lg bg-blue-500 text-white text-sm">
                      {message.bot}
                    </p>
                  </div>
                )}
              </div>
            ))}
            {waitingForResponse && (
              <div className="mb-2 text-right">
                <p className="inline-block px-3 py-2 rounded-lg bg-blue-500 text-white text-sm">
                  Loading...
                </p>
              </div>
            )}
          </div>
          <div className="p-4 bg-gray-100 border-t border-gray-300">
            <div className="flex">
              <input
                type="text"
                className="flex-grow border border-gray-300 rounded-l-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                placeholder="Type your message..."
                value={inputValue}
                onChange={handleInputChange}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              />
              <button
                className="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-1.5 rounded-r-lg transition duration-300 ease-in-out text-sm"
                onClick={handleSendMessage}
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;