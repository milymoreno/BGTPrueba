// crear-cliente.component.ts
import { Component } from '@angular/core';
import { Cliente } from '../models/cliente.model';
import { ClienteService } from '../services/cliente.service';

@Component({
  selector: 'app-crear-cliente',
  templateUrl: './crear-cliente.component.html',
  styleUrls: ['./crear-cliente.component.css']
})
export class CrearClienteComponent {
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
  
  constructor(private clienteService: ClienteService) {}

  crearCliente() {
    this.clienteService.agregarCliente(this.cliente).subscribe(
      response => {
        console.log('Cliente creado:', response);
        // Lógica adicional después de la creación del cliente, como redireccionamiento o mensaje de éxito
      },
      error => {
        console.error('Error al crear cliente:', error);
        // Manejo de errores, si es necesario
      }
    );
  }
}
