package com.princetsui.chatapp;

import java.security.Principal;
import java.util.Date;

import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;

@Controller
public class ChatController {
    @MessageMapping("/chat") // client sends to /app/chat
    @SendTo("/topic/messages")
    public ChatMessage receiveMessage(ChatMessage incomingMessage) {
        return new ChatMessage(
            incomingMessage.getUser(), 
            incomingMessage.getContent(), 
            new Date()
        );
    }
    
}

class ChatMessage {
    private String user;
    private String content;
    private Date timestamp;
    
    // Constructor
    public ChatMessage(String user, String content, Date timestamp) {
        this.user = user;
        this.content = content;
        this.timestamp = timestamp;
    }
    
    // Getters and setters
    public String getUser() {
        return user;
    }
    
    public void setUser(String user) {
        this.user = user;
    }
    
    public String getContent() {
        return content;
    }
    
    public void setContent(String content) {
        this.content = content;
    }
    
    public Date getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }
}