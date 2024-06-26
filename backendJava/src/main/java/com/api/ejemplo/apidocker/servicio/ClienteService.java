package com.api.ejemplo.apidocker.servicio;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;

//import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.api.ejemplo.apidocker.model.Cliente;
import com.api.ejemplo.apidocker.model.Fondo;
import com.api.ejemplo.apidocker.model.FondoSuscrito;
import com.api.ejemplo.apidocker.model.Transaccion;
import com.api.ejemplo.apidocker.repository.ClienteRepository;
import com.api.ejemplo.apidocker.repository.FondoRepository;


@Service
public class ClienteService {

    private final ClienteRepository clienteRepository;
    private final FondoRepository fondoRepository;
    private final NotificationService notificationService;

   // @Autowired
    public ClienteService(ClienteRepository clienteRepository, FondoRepository fondoRepository, NotificationService notificationService) {
        this.clienteRepository = clienteRepository;
        this.fondoRepository = fondoRepository;
        this.notificationService = notificationService;
    }


    public Cliente crearCliente(Cliente cliente) {
        return clienteRepository.save(cliente);
    }

    public Optional<Cliente> obtenerCliente(String id) {
        return clienteRepository.findById(id);
    }

   
   /* public Cliente asociarFondos(String clienteId, List<FondoSuscrito> fondosSuscritos) {
        Cliente cliente = clienteRepository.findById(clienteId)
                                           .orElseThrow(() -> new RuntimeException("Cliente no encontrado"));
    
        // Inicializar la lista de fondos suscritos del cliente si es null
        List<FondoSuscrito> fondos = cliente.getFondosSuscritos();
        if (fondos == null) {
            fondos = new ArrayList<>();
            cliente.setFondosSuscritos(fondos);
        }
    
        // Agregar los nuevos fondos suscritos
        fondos.addAll(fondosSuscritos);
    
        // Crear una nueva transacción de tipo "apertura" por cada fondo suscrito
        List<Transaccion> nuevasTransacciones = new ArrayList<>();
        for (FondoSuscrito fondo : fondosSuscritos) {
            Transaccion transaccionApertura = new Transaccion();

            transaccionApertura.setTipo("apertura");
            transaccionApertura.setMonto(fondo.getMontoSuscrito()); 
            transaccionApertura.setFecha(new Date()); // Opcional: establecer la fecha de la transacción
            nuevasTransacciones.add(transaccionApertura);
        }
    
        // Agregar las nuevas transacciones al historial de transacciones del cliente
        List<Transaccion> historialTransacciones = cliente.getHistorialTransacciones();
        if (historialTransacciones == null) {
            historialTransacciones = new ArrayList<>();
        }
        historialTransacciones.addAll(nuevasTransacciones);
    
        cliente.setHistorialTransacciones(historialTransacciones);
    
        // Guardar los cambios en DynamoDB
        return clienteRepository.save(cliente);
    }*/

    public Cliente asociarFondos(String clienteId, List<FondoSuscrito> fondosSuscritos) {
        Cliente cliente = clienteRepository.findById(clienteId)
                                           .orElseThrow(() -> new RuntimeException("Cliente no encontrado"));

        // Inicializar la lista de fondos suscritos del cliente si es null
        List<FondoSuscrito> fondosCliente = cliente.getFondosSuscritos();
        if (fondosCliente == null) {
            fondosCliente = new ArrayList<>();
            cliente.setFondosSuscritos(fondosCliente);
        }

        List<Transaccion> historialTransacciones = cliente.getHistorialTransacciones();
        if (historialTransacciones == null) {
            historialTransacciones = new ArrayList<>();
        }

        for (FondoSuscrito fondoSuscrito : fondosSuscritos) {
            // Consultar el fondo por fondoId para obtener el monto mínimo de suscripción
            Fondo fondo = fondoRepository.findById(fondoSuscrito.getFondoId())
                                         .orElseThrow(() -> new RuntimeException("Fondo no encontrado"));

            double montoMinimoSuscripcion = fondo.getMontoMinimo();

            // Verificar si el monto mínimo de suscripción es menor o igual que el saldo actual del cliente
            if (montoMinimoSuscripcion > cliente.getSaldoActual()) {
                throw new RuntimeException("No tiene saldo disponible para vincularse al fondo " + fondo.getNombreFondo());
            }

            // Añadir el fondo suscrito a la lista de fondos del cliente
            fondosCliente.add(fondoSuscrito);

            // Crear una nueva transacción de tipo "apertura"
            Transaccion transaccionSuscripcion = new Transaccion();
            transaccionSuscripcion.setTipo("apertura");
            transaccionSuscripcion.setMonto(montoMinimoSuscripcion);
            transaccionSuscripcion.setFecha(new Date());

            // Restar el monto de suscripción al saldo actual del cliente
            cliente.setSaldoActual(cliente.getSaldoActual() - montoMinimoSuscripcion);

            // Agregar la transacción al historial de transacciones del cliente
            historialTransacciones.add(transaccionSuscripcion);

            // Enviar notificación al cliente por cada suscripción
            String preferenciaNotificacion = cliente.getPreferenciaNotificacion();
            if ("email".equalsIgnoreCase(preferenciaNotificacion)) {
                notificationService.sendEmail(cliente.getEmail(), "Suscripción a fondo: " + fondo.getNombreFondo(), "Se ha suscrito exitosamente al fondo " + fondo.getNombreFondo() + ".");
            } else if ("sms".equalsIgnoreCase(preferenciaNotificacion)) {
                notificationService.sendSms(cliente.getTelefono(), "Se ha suscrito exitosamente al fondo " + fondo.getNombreFondo() + ".");
            }
        }

        cliente.setHistorialTransacciones(historialTransacciones);

        // Guardar los cambios en DynamoDB
        return clienteRepository.save(cliente);
    }


public Cliente cancelarSuscripcion(String clienteId, List<FondoSuscrito> fondos) {
    Cliente cliente = clienteRepository.findById(clienteId)
                                       .orElseThrow(() -> new RuntimeException("Cliente no encontrado"));

    List<FondoSuscrito> fondosCliente = cliente.getFondosSuscritos();
    if (fondosCliente == null || fondosCliente.isEmpty()) {
        throw new RuntimeException("El cliente no tiene fondos suscritos para cancelar.");
    }

    List<Transaccion> historialTransacciones = cliente.getHistorialTransacciones();
    if (historialTransacciones == null) {
        historialTransacciones = new ArrayList<>();
    }

    for (FondoSuscrito fondoSuscrito : fondos) {
        // Buscar el fondo suscrito por su ID
        Optional<FondoSuscrito> optionalFondo = fondosCliente.stream()
                .filter(fs -> fs.getFondoId().equals(fondoSuscrito.getFondoId()))
                .findFirst();
    
        if (optionalFondo.isPresent()) {
            // No es necesario declarar nuevamente `fondoSuscrito` aquí
            FondoSuscrito fondoEncontrado = optionalFondo.get();
    
            // Consultar el fondo por su ID para obtener detalles y monto de cancelación
            Fondo fondo = fondoRepository.findById(fondoEncontrado.getFondoId())
                                         .orElseThrow(() -> new RuntimeException("Fondo no encontrado"));
    
            double montoCancelacion = fondo.getMontoMinimo(); 
    
            // Generar transacción de cancelación
            Transaccion transaccionCancelacion = new Transaccion();
            transaccionCancelacion.setTipo("cancelacion");
            transaccionCancelacion.setMonto(montoCancelacion);
            transaccionCancelacion.setFecha(new Date());
    
            // Devolver el monto de cancelación al saldo actual del cliente
            cliente.setSaldoActual(cliente.getSaldoActual() + montoCancelacion);
    
            // Agregar la transacción al historial de transacciones del cliente
            historialTransacciones.add(transaccionCancelacion);
    
            // Eliminar el fondo suscrito de la lista de fondos del cliente
            fondosCliente.remove(fondoEncontrado);
    
            // Enviar notificación al cliente por la cancelación
            String preferenciaNotificacion = cliente.getPreferenciaNotificacion();
            if ("email".equalsIgnoreCase(preferenciaNotificacion)) {
                notificationService.sendEmail(cliente.getEmail(), "Cancelación de suscripción a fondo: " + fondo.getNombreFondo(), "Se ha cancelado la suscripción al fondo " + fondo.getNombreFondo() + ".");
            } else if ("sms".equalsIgnoreCase(preferenciaNotificacion)) {
                notificationService.sendSms(cliente.getTelefono(), "Se ha cancelado la suscripción al fondo " + fondo.getNombreFondo() + ".");
            }
        } else {
            throw new RuntimeException("El fondo con ID " + fondoSuscrito.getFondoId() + " no está suscrito por el cliente.");
        }
    }
    

    cliente.setFondosSuscritos(fondosCliente);
    cliente.setHistorialTransacciones(historialTransacciones);

    // Guardar los cambios en DynamoDB u el repositorio correspondiente
    return clienteRepository.save(cliente);
}



    public Cliente buscarPorNumeroIdentificacion(String numeroIdentificacion) {
        return clienteRepository.findByNumeroIdentificacion(numeroIdentificacion)
                .orElseThrow(() -> new RuntimeException("Cliente no encontrado"));
    }    

    public Cliente realizarTransaccion(String clienteId, List<Transaccion> transacciones) {
        Cliente cliente = clienteRepository.findById(clienteId)
                                           .orElseThrow(() -> new RuntimeException("Cliente no encontrado"));

        List<Transaccion> historialTransacciones = cliente.getHistorialTransacciones();
        if (historialTransacciones == null) {
            historialTransacciones = new ArrayList<>();
        }

        for (Transaccion transaccion : transacciones) {
            if ("apertura".equals(transaccion.getTipo())) {
                cliente.setSaldoActual(cliente.getSaldoActual() - transaccion.getMonto());
            } else if ("cancelacion".equals(transaccion.getTipo())) {
                cliente.setSaldoActual(cliente.getSaldoActual() + transaccion.getMonto());
            }

            historialTransacciones.add(transaccion);
        }

        cliente.setHistorialTransacciones(historialTransacciones);
        return clienteRepository.save(cliente);
    }
  
}
    


    
   

    

