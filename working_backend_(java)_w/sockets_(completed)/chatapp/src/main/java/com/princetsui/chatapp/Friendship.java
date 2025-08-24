package com.princetsui.chatapp;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import lombok.Data;

@Data
@Entity
public class Friendship {

    @ManyToOne
    @JoinColumn(name="user1_id")
    private Person user1;
    @Id @GeneratedValue
    private Long id;

    @ManyToOne
    @JoinColumn(name="user2_id")
    private Person user2;

    private String status;
    private String requester;
    
}
