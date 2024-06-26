import { Component } from '@angular/core';
import { Fondo } from '../models/fondo.model';
import { ClienteService } from '../services/cliente.service';
import { FondoService } from '../services/fondo.service';
import { TransaccionesService } from '../services/transacciones.service';

import { Cliente } from '../models/cliente.model';
import { HistorialTransacciones } from '../models/historial-transacciones.model';
import { Transaccion } from '../models/transaccion.model';


@Component({
  selector: 'app-buscar-asociar-fondos',
  templateUrl: './buscar-asociar-fondos.component.html',
  styleUrls: ['./buscar-asociar-fondos.component.css']
})
export class BuscarAsociarFondosComponent {
/* */
numeroIdentificacion: string = ''; 
fondosDisponibles: Fondo[] = [];
mensaje: string = '';
cliente: Cliente = {
  Id: '',
  Nombres: '',
  Apellidos: '',
  tipoIdentificacion: '',
  numeroIdentificacion: '',
  Email: '',
  Telefono: '',
  saldoActual: 0,
  preferenciaNotificacion: '',
  fondosSuscritos: [],
  historialTransacciones: []
};

constructor(
  private fondoService: FondoService,
  private clienteService: ClienteService,
  private transaccionesService: TransaccionesService // Inyecta el nuevo servicio
) { }

  ngOnInit(): void {
    this.getFondos(); // Llama al método getFondos() al iniciar el componente
  }

  getFondos(): void {
    this.fondoService.getFondos().subscribe(
      fondos => {
        this.fondosDisponibles = fondos; // Asigna los fondos recibidos al array fondosDisponibles
      },
      error => {
        console.error('Error al obtener los fondos:', error);
        // Manejo de errores, si es necesario
      }
    );
  }



  /**/
 
  buscarCliente() {
    this.clienteService.buscarClientePorNumeroIdentificacion(this.numeroIdentificacion).subscribe(response => {
      this.cliente = response;
    });
  }

   /*asociarFondos() {
    const fondosSeleccionados = this.fondosDisponibles.filter(fondo => fondo.selected).map(fondo => ({
      fondoId: fondo.id,
      montoSuscrito: fondo.monto,
      fechaSuscripcion: new Date().toISOString()
    }));
    this.clienteService.asociarFondos(this.cliente.id, fondosSeleccionados).subscribe(response => {
      console.log('Fondos asociados', response);
      this.buscarCliente();  // Recargar los datos del cliente después de asociar fondos
    });
  }*/

   /* asociarFondos(): void {
      const fondosSeleccionados = this.fondosDisponibles
        .filter(fondo => fondo.selected)
        .map(fondo => ({
          fondoId: fondo.fondoId, // Accede a fondoId en lugar de id
          montoSuscrito: fondo.montoSuscrito, // Accede a montoSuscrito en lugar de monto
          fechaSuscripcion: new Date().toISOString()
        }));
    
      this.clienteService.asociarFondos(this.cliente.id, fondosSeleccionados).subscribe(
        response => {
          console.log('Fondos asociados', response);
          this.buscarCliente();  // Recargar los datos del cliente después de asociar fondos
        },
        error => {
          console.error('Error al asociar fondos:', error);
          // Manejo de errores, si es necesario
        }
      );
    }*/

      /*asociarFondos(): void {
        const fondosSeleccionados = this.fondosDisponibles
          .filter(fondo => fondo.selected)
          .map(fondo => ({
            fondoId: fondo.fondoId,
            montoSuscrito: fondo.montoSuscrito,
            fechaSuscripcion: new Date().toISOString()
          }));
    
        this.clienteService.asociarFondos(this.cliente.id, fondosSeleccionados).subscribe(
          response => {
            console.log('Fondos asociados:', response);
    
            // Generar transacción
            const transaccion: Transaccion = {
              tipo: 'Asociación de fondos',
              descripcion: 'Asociación de fondos a cliente',
              monto: fondosSeleccionados.reduce((total, fondo) => total + fondo.montoSuscrito, 0),
              fecha: new Date().toISOString()
            };
    
            this.clienteService.realizarTransaccion(this.cliente.id, transaccion).subscribe(
              response => {
                console.log('Transacción realizada:', response);
                this.buscarCliente(); // Recargar los datos del cliente después de asociar fondos y transacción
              },
              error => {
                console.error('Error al realizar transacción:', error);
                // Manejo de errores, si es necesario
              }
            );
    
          },
          error => {
            console.error('Error al asociar fondos:', error);
            // Manejo de errores, si es necesario
          }
        );
      }*/
     
        /*asociarFondos(): void {
          const fondosSeleccionados: any[] = this.fondosDisponibles
            .filter(fondo => fondo.selected)
            .map(fondo => ({
              fondoId: fondo.fondoId,
              montoSuscrito: fondo.montoSuscrito,
              fechaSuscripcion: new Date().toISOString()
            }));
      
          // Arreglo para almacenar las transacciones
          const transacciones: Transaccion[] = [];
      
          // Generar transacciones para cada fondo seleccionado
          fondosSeleccionados.forEach((fondo, index) => {
            const transaccion: Transaccion = {
              tipo: 'apertura',
              transactionId: 'id_transaccion',
              monto: fondo.montoSuscrito,
              fecha: new Date().toISOString(),
              fondoId: fondo.fondoId
            };
            transacciones.push(transaccion);
          });
      
          // Llamar al servicio para asociar los fondos con las transacciones correspondientes
          this.clienteService.asociarFondos(this.cliente.Id, fondosSeleccionados).subscribe(
            response => {
              console.log('Fondos asociados:', response);
      
              // Llamar al servicio para realizar las transacciones
              this.clienteService.realizarTransaccion(this.cliente.Id, transacciones).subscribe(
                response => {
                  console.log('Transacciones realizadas:', response);
      
                  // Guardar las transacciones en el historial
                  this.transaccionesService.guardarHistorialTransacciones(transacciones).subscribe(
                    response => {
                      console.log('Historial de transacciones guardado:', response);
      
                      // Actualizar el cliente después de la transacción
                      this.clienteService.getCliente(this.cliente.Id).subscribe(
                        (clienteActualizado: Cliente) => {
                          this.cliente = clienteActualizado;
                          console.log('Cliente actualizado:', this.cliente);
                        },
                        error => {
                          console.error('Error al obtener el cliente actualizado:', error);
                          // Manejo de errores, si es necesario
                        }
                      );
                    },
                    error => {
                      console.error('Error al guardar historial de transacciones:', error);
                      // Manejo de errores, si es necesario
                    }
                  );
                },
                error => {
                  console.error('Error al realizar transacciones:', error);
                  // Manejo de errores, si es necesario
                }
              );
            },
            error => {
              console.error('Error al asociar fondos:', error);
              // Manejo de errores, si es necesario
            }
          );
        }*/

          asociarFondos(): void {
            const fondosSeleccionados = this.fondosDisponibles
              .filter(fondo => fondo.selected)
              .map(fondo => ({
                fondoId: fondo.fondoId,
                montoSuscrito: fondo.montoSuscrito,
                fechaSuscripcion: new Date().toISOString()                
              }));
        
            if (fondosSeleccionados.length === 0) {
              this.mensaje = 'Por favor, seleccione al menos un fondo para asociar.';
              return;
            }
        
            let validacionPendiente = 0;
            let validacionFallida = false;
        
            fondosSeleccionados.forEach(fondo => {
              validacionPendiente++;
              this.fondoService.validarSaldo(this.cliente.Id, fondo.fondoId).subscribe(
                (data: string) => {
                  if (data.startsWith('No tiene saldo disponible')) {
                    this.mensaje = data;
                    validacionFallida = true;
                  }
                  validacionPendiente--;
                  if (validacionPendiente === 0 && !validacionFallida) {
                    this.procederAsociacion(fondosSeleccionados);
                  }
                },
                (error: any) => {
                  console.error('Error al validar el saldo', error);
                  this.mensaje = 'Error al validar el saldo, por favor intente de nuevo más tarde.';
                  validacionPendiente--;
                }
              );
            });
          }
        
          procederAsociacion(fondosSeleccionados: any[]): void {
            // Arreglo para almacenar las transacciones
            const transacciones: Transaccion[] = [];
        
            // Generar transacciones para cada fondo seleccionado
            fondosSeleccionados.forEach((fondo, index) => {
              const tipoTransaccion = (fondo.tipo === 'apertura') ? 'apertura' : 'cancelacion';
        
              const transaccion: Transaccion = {
                transactionId: '',
                fondoId: fondo.fondoId,
                tipo: tipoTransaccion,
                monto: fondo.montoSuscrito,
                fecha: new Date().toISOString()
              };
              transacciones.push(transaccion);
            });
        
            // Llamar al servicio para asociar los fondos con las transacciones correspondientes
            this.clienteService.asociarFondos(this.cliente.Id, fondosSeleccionados).subscribe(
              response => {
                console.log('Fondos asociados:', response);
        
                // Llamar al servicio para realizar las transacciones
                this.clienteService.realizarTransaccion(this.cliente.Id, transacciones).subscribe(
                  response => {
                    console.log('Transacciones realizadas:', response);
        
                    // Preparar los datos para el historial de transacciones en DynamoDB
                    const historialTransacciones: HistorialTransacciones[] = response.map((transaccion: any) => ({
                      TransaccionId: transaccion.transactionId,
                      fondoId: transaccion.fondoId,
                      clienteId: this.cliente.Id,
                      tipo: transaccion.tipo,
                      monto: transaccion.monto,
                      fecha: transaccion.fecha
                    }));
        
                    // Llamar al servicio para guardar el historial de transacciones
                    this.transaccionesService.guardarHistorialTransacciones(historialTransacciones).subscribe(
                      response => {
                        console.log('Historial de transacciones guardado:', response);
        
                        // Actualizar el cliente después de la transacción
                        this.clienteService.getCliente(this.cliente.Id).subscribe(
                          (clienteActualizado: Cliente) => {
                            this.cliente = clienteActualizado;
                            console.log('Cliente actualizado:', this.cliente);
                          },
                          error => {
                            console.error('Error al obtener el cliente actualizado:', error);
                            // Manejo de errores, si es necesario
                          }
                        );
                      },
                      error => {
                        console.error('Error al guardar historial de transacciones:', error);
                        // Manejo de errores, si es necesario
                      }
                    );
                  },
                  error => {
                    console.error('Error al realizar transacciones:', error);
                    // Manejo de errores, si es necesario
                  }
                );
              },
              error => {
                console.error('Error al asociar fondos:', error);
                // Manejo de errores, si es necesario
              }
            );
          }
  }
        

