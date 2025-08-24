package com.princetsui.chatapp;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class FriendshipService {
    
    @Autowired
    private FriendshipRepo friendshipRepo;
    
    @Autowired
    private PersonRepo personRepo;
    
    public Friendship sendFriendRequest(String requesterUsername, String recipientUsername) {
            // Fetch requester and recipient as Person objects
    Person requester = personRepo.findByUsername(requesterUsername)
            .orElseThrow(() -> new RuntimeException("Requester not found"));
    Person recipient = personRepo.findByUsername(recipientUsername)
            .orElseThrow(() -> new RuntimeException("Recipient not found"));

        System.out.println(requesterUsername +" send a friend request to " +recipientUsername);
        Friendship friendship = new Friendship();
        friendship.setUser1(requester);
        friendship.setUser2(recipient);
        friendship.setStatus("Pending");

        friendshipRepo.save(friendship);

        return friendship;
        // Business logic here
    }
    
    public Friendship acceptFriendRequest(Long friendshipId) {
        return null;
        // Business logic here
    }
    
    public void rejectFriendRequest(Long friendshipId) {
        // Business logic here
    }
    
    public List<Friendship> getPendingRequests(String username) {
        return friendshipRepo.findPendingRequestsFor(username);
    }
    
    public List<Friendship> getFriends(String username) {
        return friendshipRepo.findAcceptedFriendships(username);
    }
    
    // etc...
}