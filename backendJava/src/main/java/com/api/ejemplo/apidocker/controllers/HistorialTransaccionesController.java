package com.api.ejemplo.apidocker.controllers;

import java.util.List;

//import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.api.ejemplo.apidocker.model.HistorialTransacciones;
import com.api.ejemplo.apidocker.servicio.HistorialTransaccionesService;

@RestController
@RequestMapping("/historialTransacciones")
public class HistorialTransaccionesController {

    private final HistorialTransaccionesService historialTransaccionesService;

    //@Autowired
    public HistorialTransaccionesController(HistorialTransaccionesService historialTransaccionesService) {
        this.historialTransaccionesService = historialTransaccionesService;
    }

    @GetMapping
    public List<HistorialTransacciones> getAllHistorialTransacciones() {
        return historialTransaccionesService.getAllHistorialTransacciones();
    }
}
