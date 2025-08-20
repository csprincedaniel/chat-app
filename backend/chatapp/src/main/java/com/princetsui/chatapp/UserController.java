package com.princetsui.chatapp;

import java.util.*;

import javax.crypto.SecretKey;

import org.springframework.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.princetsui.chatapp.Person;
import com.princetsui.chatapp.PersonRepo;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.http.HttpSession;
import org.springframework.web.bind.annotation.RequestMethod;


@CrossOrigin(
    origins = "http://localhost:3000",
    methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.OPTIONS},
    allowedHeaders = "*",
    allowCredentials = "true"
)
@RestController
@RequestMapping("/info")
public class UserController {
    private final PersonRepo personRepo;

    public UserController(PersonRepo personRepo){
        this.personRepo = personRepo;
    }

    @GetMapping("/id/{id}")
    public ResponseEntity<Map<String, String>> getUser(@PathVariable Long id){
        return personRepo.findById(id).map(x -> {
            Map <String, String> result = Map.of(
                "username", x.getUsername(),
                "password", x.getPassword()
            );
            return ResponseEntity.ok(result);
        })
        .orElse(ResponseEntity.notFound().build());
    }
    @GetMapping("/username")
    public ResponseEntity<Map<String, String>> getUserByUsername(@RequestParam String username) {
        return personRepo.findByUsername(username).map(x ->{
            Map <String, String> result = Map.of(
                "username", x.getUsername(),
                "password",x.getPassword()
            );
            return ResponseEntity.ok(result);
        })
        .orElse(ResponseEntity.notFound().build());
    }
    @PostMapping("/login")
    public ResponseEntity<Map<String, String>> login(@RequestBody Map<String, String> body, HttpSession session){
        String username = body.get("username");
        String password = body.get("password");

        return personRepo.findByUsername(username).map(user -> {
            if (!user.getPassword().equals(password)) {
                return ResponseEntity.status(401).body(Map.of("error", "Invalid password"));
            }

            // store username in session
            session.setAttribute("username", username);

            return ResponseEntity.ok(Map.of("username", username));
        }).orElse(ResponseEntity.status(404).body(Map.of("error", "User not found")));
    }

    //didn't write
@GetMapping("/me")
public ResponseEntity<Map<String, String>> me(HttpSession session) {
    System.out.println("Session ID: " + session.getId());
    System.out.println("Is new session: " + session.isNew());
    
    String username = (String) session.getAttribute("username");
    if (username != null) {
        return ResponseEntity.ok(Map.of("username", username));
    }
    return ResponseEntity.status(401).body(Map.of("error", "Not logged in"));
}
    @GetMapping("/")
    public ResponseEntity<String> sayHello(){
        return ResponseEntity.ok("Hello");
    }
}
