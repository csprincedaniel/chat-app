"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import {Client} from "@stomp/stompjs"
import styles from "./chat-area.module.css"

interface Message {
  id: string
  user: string
  content: string
  timestamp: Date
  avatar: string
}

interface ChatAreaProps {
  channelName: string
  serverName: string
  currentUser: { username: string; email: string }
}

export default function ChatArea({ channelName, serverName, currentUser }: ChatAreaProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      user: "Alice",
      content: "Hey everyone! How's it going?",
      timestamp: new Date(Date.now() - 3600000),
      avatar: "👩",
    },
    {
      id: "2",
      user: "Bob",
      content: "Pretty good! Just working on some code.",
      timestamp: new Date(Date.now() - 3000000),
      avatar: "👨",
    },
    {
      id: "3",
      user: "Charlie",
      content: "Anyone want to play some games later?",
      timestamp: new Date(Date.now() - 1800000),
      avatar: "🧑",
    },
  ])

  const [newMessage, setNewMessage] = useState("")
  const [stompClient, setStompClient] = useState<Client | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    const client = new Client({
      brokerURL: 'ws://localhost:8080/ws',
      debug: function (str) {
        console.log('STOMP: ' + str);
      },
    })

    client.onConnect = () => {
      // Subscribe to receive messages from server
      client.subscribe('/topic/messages', (message) => {
        const chatMessage = JSON.parse(message.body);
        const newMsg: Message = {
          id: Date.now().toString(),
          user: chatMessage.user,
          content: chatMessage.content,
          timestamp: new Date(chatMessage.timestamp),
          avatar: "👤",
        };
        setMessages(prev => [...prev, newMsg]);
      });
    }

    client.activate()
    setStompClient(client)

    return () => {
      if (client.active) {
        client.deactivate()
      }
    }
  }, [])

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (newMessage.trim() && stompClient) {
      const messageToSend = {
        user: currentUser.username,
        content: newMessage.trim()
      }

      stompClient.publish({
        destination: '/app/chat', 
        body: JSON.stringify(messageToSend)
      })

      setNewMessage("")
    }
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  const formatDate = (date: Date) => {
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    if (date.toDateString() === today.toDateString()) {
      return "Today"
    } else if (date.toDateString() === yesterday.toDateString()) {
      return "Yesterday"
    } else {
      return date.toLocaleDateString()
    }
  }

async function handleFriendClick(): Promise<void> {
  try {
    const res = await fetch("http://localhost:8080/info/me", {
      credentials: "include", // sends the session cookie automatically
    });
    if (!res.ok) throw new Error("Not logged in");

    const data = await res.json(); // e.g., { username: "me" }

    const user = prompt("What is the username of the friend you want to add?");
    if (!user) return;

    alert(`Sending a friend request to ${user}.`);

    const requestRes = await fetch("http://localhost:8080/api/friendships/request", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        requester: data.username, // send only what backend expects
        recipient: user
      }),
      credentials: "include"
    });

    if (!requestRes.ok) throw new Error("Request failed");

    alert(`Friend request sent to ${user}.`);
  } catch (err) {
    console.error(err);
    alert("ERR");
  }
}

  return (
    <div className={styles.chatArea}>
      <div className={styles.chatHeader}>
        <div className={styles.channelInfo}>
          <span className={styles.channelIcon}>#</span>
          <h3 className={styles.channelName}>{channelName}</h3>
        </div>
        <div className={styles.headerControls}>
          <button className={styles.headerButton}>📞</button>
          <button className={styles.headerButton}>📹</button>
          <button className={styles.headerButton}>📌</button>
          <button onClick={() => handleFriendClick()} className={styles.headerButton}>👥</button>
          <button className={styles.headerButton}>🔍</button>
          <button className={styles.headerButton}>📥</button>
          <button className={styles.headerButton}>❓</button>
        </div>
      </div>

      <div className={styles.messagesContainer}>
        <div className={styles.channelStart}>
          <div className={styles.channelStartIcon}>#</div>
          <h2>Welcome to #{channelName}!</h2>
          <p>This is the start of the #{channelName} channel.</p>
        </div>

        {messages.map((message, index) => {
          const showDate = index === 0 || formatDate(message.timestamp) !== formatDate(messages[index - 1].timestamp)

          return (
            <div key={message.id}>
              {showDate && (
                <div className={styles.dateDivider}>
                  <span>{formatDate(message.timestamp)}</span>
                </div>
              )}
              <div className={styles.message}>
                <div className={styles.messageAvatar}>{message.avatar}</div>
                <div className={styles.messageContent}>
                  <div className={styles.messageHeader}>
                    <span className={styles.username}>{message.user}</span>
                    <span className={styles.timestamp}>{formatTime(message.timestamp)}</span>
                  </div>
                  <div className={styles.messageText}>{message.content}</div>
                </div>
              </div>
            </div>
          )
        })}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.messageInput}>
        <form onSubmit={handleSendMessage} className={styles.inputForm}>
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder={`Message #${channelName}`}
            className={styles.textInput}
          />
          <button type="submit" className={styles.sendButton}>
            ➤
          </button>
        </form>
      </div>
    </div>
  )
}