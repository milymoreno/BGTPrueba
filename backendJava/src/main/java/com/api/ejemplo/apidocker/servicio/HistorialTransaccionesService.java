package com.api.ejemplo.apidocker.servicio;

import com.api.ejemplo.apidocker.model.HistorialTransacciones;
import com.api.ejemplo.apidocker.repository.HistorialTransaccionesRepository;
import org.springframework.stereotype.Service;


import java.util.List;
import java.util.Optional;

@Service
public class HistorialTransaccionesService {

    private final HistorialTransaccionesRepository historialTransaccionesRepository;
    //private final DynamoDbTable<HistorialTransacciones> dynamoDbTable;

   // @Autowired
    public HistorialTransaccionesService(HistorialTransaccionesRepository historialTransaccionesRepository) {
        this.historialTransaccionesRepository = historialTransaccionesRepository;
    }

     public HistorialTransacciones crearHistorialTransaccion(HistorialTransacciones transaccion) {
        return historialTransaccionesRepository.save(transaccion); 
    }
    
    public List<HistorialTransacciones> getAllHistorialTransacciones() {
        return (List<HistorialTransacciones>) historialTransaccionesRepository.findAll();
    }

     public Optional<HistorialTransacciones> obtenerHistorialTransacciones(String clienteId) {
        return historialTransaccionesRepository.findById(clienteId);
    }


}
