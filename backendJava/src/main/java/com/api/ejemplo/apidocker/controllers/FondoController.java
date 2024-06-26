package com.api.ejemplo.apidocker.controllers;

import java.util.List;
import java.util.Optional;

//import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
//import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.api.ejemplo.apidocker.model.Fondo;
import com.api.ejemplo.apidocker.servicio.FondoServiceAnt;

@RestController
//@CrossOrigin(origins = "*")
@RequestMapping("/fondos")
public class FondoController {

    private final FondoServiceAnt fondoService;

    //@Autowired
    public FondoController(FondoServiceAnt fondoService) {
        this.fondoService = fondoService;
    }

    @PostMapping
    public ResponseEntity<Fondo> crearFondo(@RequestBody Fondo fondo) {
        Fondo nuevoFondo = fondoService.crearFondo(fondo);
        return ResponseEntity.ok(nuevoFondo);
    }

    @GetMapping("/{fondoId}")
    public ResponseEntity<Fondo> obtenerFondo(@PathVariable String fondoId) {
        Optional<Fondo> fondo = fondoService.obtenerFondo(fondoId);
        return fondo.map(ResponseEntity::ok)
                    .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping
    public ResponseEntity<List<Fondo>> obtenerTodosLosFondos() {
        List<Fondo> fondos = fondoService.obtenerTodosLosFondos();
        return ResponseEntity.ok(fondos);
    }

    // Método para buscar fondo por nombre
    @GetMapping("/buscar/{nombreFondo}")
    public ResponseEntity<Fondo> buscarPorNombreFondo(@PathVariable String nombreFondo) {
        Fondo fondo = fondoService.buscarPorNombreFondo(nombreFondo);
        return ResponseEntity.ok(fondo);
    }

    @GetMapping("/validar-saldo")
    public ResponseEntity<String> validarSaldo(@RequestParam String clienteId, @RequestParam String fondoId) {
        String mensaje = fondoService.validarSaldo(clienteId, fondoId);
        return ResponseEntity.ok(mensaje);
    }

}
