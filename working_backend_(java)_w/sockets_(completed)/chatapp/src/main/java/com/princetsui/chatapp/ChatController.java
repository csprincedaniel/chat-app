package com.princetsui.chatapp;

import java.security.Principal;
import java.util.Date;
import com.princetsui.chatapp.ChatMessage;

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

