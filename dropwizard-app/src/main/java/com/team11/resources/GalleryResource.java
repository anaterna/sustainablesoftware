package com.team11.resources;

import com.team11.ThymeleafRenderer;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.core.Response;

import java.util.HashMap;
import java.util.List;
import java.util.Map;


@Path("/gallery")
public class GalleryResource {
    private final List<String> GREETINGS_IMAGES = List.of("electric_hello.jpg", "fun_hello.jpg", "minimal_hello.jpg",
            "vibrant_hello.jpg", "hello.jpg", "simple_hello.jpg");
    @GET
    public Response gallery() {
        Map<String, Object> model = new HashMap<>();
        model.put("images", GREETINGS_IMAGES);

        String html = ThymeleafRenderer.render("gallery", model);
        return Response.ok(html).build();
    }
}