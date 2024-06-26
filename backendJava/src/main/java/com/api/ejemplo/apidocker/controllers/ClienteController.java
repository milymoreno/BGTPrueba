package com.api.ejemplo.apidocker.controllers;

import java.util.List;
import java.util.Optional;

import org.springframework.http.ResponseEntity;
//import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.api.ejemplo.apidocker.model.Cliente;
import com.api.ejemplo.apidocker.model.FondoSuscrito;
import com.api.ejemplo.apidocker.model.Transaccion;
import com.api.ejemplo.apidocker.servicio.ClienteService;

@RestController
//@CrossOrigin(origins = "*")
@RequestMapping("/clientes")
public class ClienteController {

    private final ClienteService clienteService;

    //@Autowired
    public ClienteController(ClienteService clienteService) {
        this.clienteService = clienteService;
    }

    @PostMapping
    public Cliente crearCliente(@RequestBody Cliente cliente) {
        return clienteService.crearCliente(cliente);
    }

    @GetMapping("/{clienteId}")
    public Optional<Cliente> obtenerCliente(@PathVariable String clienteId) {
        return clienteService.obtenerCliente(clienteId);
    }

     // Método para buscar cliente por número de identificación
     @GetMapping("/buscar/{numeroIdentificacion}")
     public ResponseEntity<Cliente> buscarPorNumeroIdentificacion(@PathVariable String numeroIdentificacion) {
         Cliente cliente = clienteService.buscarPorNumeroIdentificacion(numeroIdentificacion);
         return ResponseEntity.ok(cliente);
     }

   /* @PostMapping("/{clienteId}/fondos")
    public Cliente asociarFondo(@PathVariable String clienteId, @RequestBody FondoSuscrito fondoSuscrito) {
        return clienteService.asociarFondo(clienteId, fondoSuscrito);
    }*/

    /*public Cliente asociarFondos(@PathVariable String clienteId, @RequestBody List<FondoSuscrito> fondosSuscritos) {
        return clienteService.asociarFondos(clienteId, fondosSuscritos);
    }*/

    @PostMapping("/{clienteId}/fondos")
    public ResponseEntity<?> asociarFondos(@PathVariable String clienteId, @RequestBody List<FondoSuscrito> fondosSuscritos) {
        Cliente clienteActualizado = clienteService.asociarFondos(clienteId, fondosSuscritos);
        return ResponseEntity.ok(clienteActualizado);
    }


    @PostMapping("/{clienteId}/transacciones")
    public Cliente realizarTransaccion(@PathVariable String clienteId,@RequestBody List<Transaccion> transaccion) {
        return clienteService.realizarTransaccion(clienteId, transaccion);
    }

    // Otros métodos para consultar clientes, fondos, transacciones, etc.
}
