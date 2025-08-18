package com.princetsui.chatapp;

import java.util.*;
import org.springframework.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.princetsui.chatapp.Person;
import com.princetsui.chatapp.PersonRepo;


@RestController
@RequestMapping("/info")
@CrossOrigin(origins="*")
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

    @GetMapping("/")
    public String sayHello(){
        return "Hello";
    }
}
