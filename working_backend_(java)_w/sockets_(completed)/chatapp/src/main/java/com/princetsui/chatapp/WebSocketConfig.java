package com.princetsui.chatapp;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer{
    @Override
    public void configureMessageBroker(MessageBrokerRegistry config){
        config.enableSimpleBroker("/topic"); // messages server -> clients
        config.setApplicationDestinationPrefixes("/app"); // messages client -> server
    }
    
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry){
        // Native WebSocket endpoint
        registry.addEndpoint("/ws").setAllowedOriginPatterns("*");
        
        // SockJS endpoint as fallback
        registry.addEndpoint("/ws").setAllowedOriginPatterns("*").withSockJS();
    }
}