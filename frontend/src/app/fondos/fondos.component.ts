import { Component, OnInit } from '@angular/core';
import { FondoService } from '../services/fondo.service';
import { Fondo } from '../models/fondo.model';
@Component({
  selector: 'app-fondos',
  templateUrl: './fondos.component.html',
  styleUrls: ['./fondos.component.css']
})
export class FondosComponent implements OnInit {

  fondosDisponibles: Fondo[] = [];

  constructor(private fondoService: FondoService) { }

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

  asociarFondos(): void {
    const fondosSeleccionados = this.fondosDisponibles.filter(fondo => fondo.selected);
    console.log(fondosSeleccionados);    
  }
}