package com.princetsui.chatapp;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin(
    origins = "http://localhost:3000",
    allowCredentials = "true"
)
@RestController
@RequestMapping("/api/friendships")
public class FriendshipController {
    @Autowired
    private FriendshipService friendshipService;
        // Send friend request
    @PostMapping("/request")
    public ResponseEntity<Map<String, Friendship>> sendFriendRequest(@RequestBody Map<String, String> body){
        String requester = body.get("requester");
        String recipient = body.get("recipient");
        Friendship friendship = friendshipService.sendFriendRequest(requester, recipient);
        return ResponseEntity.ok(Map.of("code", friendship));
    }
    
    // Accept friend request  
    //@PutMapping("/accept/{friendshipId}")
    //public ResponseEntity<?> acceptFriendRequest(@PathVariable Long friendshipId)
    
    // Reject/decline friend request
    //@PutMapping("/reject/{friendshipId}")  
    //public ResponseEntity<?> rejectFriendRequest(@PathVariable Long friendshipId)
    
    // Get pending requests for user
    //@GetMapping("/pending/{username}")
    //public ResponseEntity<List<Friendship>> getPendingRequests(@PathVariable String username)
    
    // Get all friends for user
    //@GetMapping("/friends/{username}")
    //public ResponseEntity<List<Friendship>> getFriends(@PathVariable String username)
    
    // Remove/unfriend
    //@DeleteMapping("/{friendshipId}")
    //public ResponseEntity<?> removeFriendship(@PathVariable Long friendshipId)
}
