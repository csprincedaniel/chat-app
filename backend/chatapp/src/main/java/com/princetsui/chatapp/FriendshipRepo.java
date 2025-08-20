package com.princetsui.chatapp;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;


public interface FriendshipRepo extends JpaRepository<Friendship, Long>{
    //all friendship records where a specific user is involved
    @Query("SELECT f FROM Friendship f WHERE f.user1.username = :username OR f.user2.username = :username")
    List<Friendship> findByUsername(@Param("username") String username);

    // Find pending requests sent TO a user
    @Query("SELECT f FROM Friendship f WHERE f.user2.username = :username AND f.status = 'PENDING'")
    List<Friendship> findPendingRequestsFor(@Param("username") String username);
    
    // Find only accepted friendships for a user
    @Query("SELECT f FROM Friendship f WHERE (f.user1.username = :username OR f.user2.username = :username) AND f.status = 'ACCEPTED'")
    List<Friendship> findAcceptedFriendships(@Param("username") String username);
}
