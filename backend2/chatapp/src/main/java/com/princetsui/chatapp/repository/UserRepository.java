package com.princetsui.chatapp.repository;

import com.princetsui.chatapp.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long>{

    // Method for finding email. Returns either the user based off of the email or null.
    Optional<User> findByEmail(String email);
}
