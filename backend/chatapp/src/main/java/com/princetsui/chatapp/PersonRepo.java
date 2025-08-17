package com.princetsui.chatapp;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface PersonRepo extends JpaRepository<Person, Long>{
    Optional<Person> findByUsername(String username);
}
