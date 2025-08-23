package com.princetsui.chatapp;

import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;

@Controller
public class ChatController {
    @MessageMapping("/chat") // client sends to /app/chat
    @SendTo("/topic/messages")
    public String receiveMessage(String message) {
        System.out.println("ChatController.receiveMessage() called");
        System.out.println("Received from client: " + message);
        return message;
    }
}