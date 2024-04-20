import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";

const RoomPage = () => {
  const router = useRouter();
  const { room_name } = router.query;
  const [message, setMessage] = useState("");
  const [receivedMessages, setReceivedMessages] = useState([]);
  const [sentMessages, setSentMessages] = useState([]);
  const [ws, setWs] = useState(null);

  const handleSendMessage = (e) => {
    e.preventDefault()
    if (message.trim() !== "" && ws) {
      // Envoyer le message au serveur Django via WebSocket
      ws.send(JSON.stringify({ message, sent: true })); // Ajoutez une propriété 'sent' au message
      setMessage("");
    }
  };

  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  useEffect(() => {
    if (room_name) {
      const newWs = new WebSocket(`ws://localhost:8000/ws/chat/${room_name}/`);
  
      newWs.onopen = () => {
        console.log("WebSocket connected!");
      };
  
      newWs.onmessage = (message) => {
        const parsedMessage = JSON.parse(message.data);
        if (!parsedMessage.sent) {
          setReceivedMessages((prevMessages) => [...prevMessages, parsedMessage]);
        }
      };
  
      newWs.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
  
      newWs.onclose = () => {
        console.log("WebSocket connection closed.");
      };
  
      setWs(newWs);
    }
  }, [room_name]);

  return (
    <div>
      <h1>Room Page</h1>
      <p>Room Name: {room_name}</p>
      <div>
        <h2>Received Messages</h2>
        <div>
          {receivedMessages.map((msg, index) => (
            <div key={index}>{msg.message}</div>
          ))}
        </div>
      </div>
      <div>
        <h2>Sent Messages</h2>
        <div>
          {sentMessages.map((msg, index) => (
            <div key={index}>{msg.message}</div>
          ))}
        </div>
      </div>
      <form onSubmit={e => handleSendMessage(e)}>
        <input
          type="text"
          placeholder="Type your message..."
          value={message}
          onChange={handleInputChange}
        />
        <button>Send</button>
      </form>
    </div>
  );
};

export default RoomPage;
