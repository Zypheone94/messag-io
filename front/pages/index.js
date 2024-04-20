// pages/index.js
import React, { useState } from 'react';
import { useRouter } from 'next/router';

const IndexPage = () => {
  const router = useRouter();
  const [roomName, setRoomName] = useState('');

  const handleFormSubmit = (e) => {
    e.preventDefault();
    router.push(`/room/${roomName}`);
  };

  const handleInputChange = (e) => {
    setRoomName(e.target.value);
  };

  return (
    <div>
      <h1>Join a Chat Room</h1>
      <form onSubmit={handleFormSubmit}>
        <input
          type="text"
          placeholder="Enter Room Name"
          value={roomName}
          onChange={handleInputChange}
        />
        <button type="submit">Join</button>
      </form>
    </div>
  );
};

export default IndexPage;
