package com.api.ejemplo.apidocker.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;



@RestController
@RequestMapping("/")
public class HolaController {

    @GetMapping("/saludo")
    public String saludar() {
        return "¡Hola, mundo!";
    }

    @PostMapping("/crear")
    public String crear(@RequestBody String data) {
        // Lógica para crear algo
        return "Objeto creado: " + data;
    }

    
    
}
