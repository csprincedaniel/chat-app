'use client';

import { Client } from '@stomp/stompjs';
import { useEffect } from 'react';

export default function TestPage() {
  useEffect(() => {
    const stompClient = new Client({
      brokerURL: 'ws://localhost:8080/ws',
      debug: function (str) {
        console.log('STOMP: ' + str);
      },
    });

    stompClient.onConnect = () => {
      console.log('Connected to WebSocket');

      // Send a message to the server
      console.log('Sending message to server...');
      stompClient.publish({
        destination: '/app/chat', 
        body: 'Hello server!'
      });
      console.log('Message sent');
    };

    stompClient.onStompError = (frame) => {
      console.error('STOMP error:', frame);
    };

    stompClient.onWebSocketError = (error) => {
      console.error('WebSocket error:', error);
    };

    stompClient.activate();

    // Cleanup on component unmount
    return () => {
      stompClient.deactivate();
    };
  }, []);

  return <div>WebSocket Test</div>;
}