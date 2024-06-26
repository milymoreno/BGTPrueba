// crear-fondo.component.ts
import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Fondo } from '../models/fondo.model';


@Component({
  selector: 'app-crear-fondo',
  templateUrl: './crear-fondos.component.html',
  styleUrls: ['./crear-fondos.component.css']
})
export class CrearFondoComponent {
  fondo: Fondo = {
    fondoId: '',
    nombreFondo: '',
    descripcion: '',
    montoSuscrito: 0,
    fechaSuscripcion: ''
  };

  constructor(private http: HttpClient) {}

  crearFondo() {
    const url = 'http://localhost:8082/crearFondo'; // Cambia la URL según tu backend
    this.http.post(url, this.fondo)
      .subscribe(
        response => {
          console.log('Fondo creado:', response);
          // Lógica adicional después de la creación del fondo, como redireccionamiento o mensaje de éxito
        },
        error => {
          console.error('Error al crear fondo:', error);
          // Manejo de errores, si es necesario
        }
      );
  }
}

