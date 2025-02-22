package com.sustainable.software.rest_service.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class GreetingsController {

    private final List<String> GREETINGS_IMAGES = List.of("electric_hello.jpg", "fun_hello.jpg", "minimal_hello.jpg",
            "vibrant_hello.jpg", "hello.jpg", "simple_hello.jpg");

    @GetMapping("/gallery")
    public String showGallery(Model model) {
        // List of image filenames in the static/images directory
        model.addAttribute("images", GREETINGS_IMAGES);
        return "gallery"; // Corresponds to gallery.html in src/main/resources/templates
    }
}
