package com.api.ejemplo.apidocker.repository;

import org.socialsignin.spring.data.dynamodb.repository.EnableScan;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;
import com.api.ejemplo.apidocker.model.Cliente;

@EnableScan
public interface ClienteRepository extends CrudRepository<Cliente, String> {
    // Métodos adicionales según las necesidades
    Optional<Cliente> findByNumeroIdentificacion(String numeroIdentificacion);
}

