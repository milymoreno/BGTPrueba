package com.api.ejemplo.apidocker.servicio;

import java.util.List;
import java.util.Optional;

//import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.api.ejemplo.apidocker.model.Cliente;
import com.api.ejemplo.apidocker.model.Fondo;
import com.api.ejemplo.apidocker.repository.ClienteRepository;
import com.api.ejemplo.apidocker.repository.FondoRepository;

@Service
public class FondoServiceAnt {

    private final FondoRepository fondoRepository;

    //@Autowired
    private ClienteRepository clienteRepository;


    //@Autowired
    public FondoServiceAnt(FondoRepository fondoRepository) {
        this.fondoRepository = fondoRepository;
    }

     public String validarSaldo(String clienteId, String fondoId) {
        Cliente cliente = clienteRepository.findById(clienteId)
            .orElseThrow(() -> new RuntimeException("Cliente no encontrado"));
        Fondo fondo = fondoRepository.findById(fondoId)
        .orElseThrow(() -> new RuntimeException("Fondo no encontrado"));

        if (cliente.getSaldoActual() < fondo.getMontoMinimo()) {
            return "No tiene saldo disponible para vincularse al fondo " + fondo.getNombreFondo();
        }

        return "Puede vincularse al fondo " + fondo.getNombreFondo();
    }

    public Fondo crearFondo(Fondo fondo) {
        return fondoRepository.save(fondo);
    }

    public Optional<Fondo> obtenerFondo(String fondoId) {
        return fondoRepository.findById(fondoId);
    }

    public List<Fondo> obtenerTodosLosFondos() {
        return (List<Fondo>) fondoRepository.findAll();
    }

    public Fondo buscarPorNombreFondo(String nombreFondo) {
        return fondoRepository.findByNombreFondo(nombreFondo).orElse(null);
    }
}
