package com.api.ejemplo.apidocker.repository;

import com.api.ejemplo.apidocker.model.HistorialTransacciones;

import org.socialsignin.spring.data.dynamodb.repository.EnableScan;
import org.springframework.data.repository.CrudRepository;

@EnableScan
public interface HistorialTransaccionesRepository  extends CrudRepository<HistorialTransacciones , String> {
    
    
}
