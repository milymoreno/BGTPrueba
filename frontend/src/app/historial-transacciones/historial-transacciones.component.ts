// historial-transacciones.component.ts

import { Component, OnInit } from '@angular/core';
import { HistorialTransacciones } from '../models/historial-transacciones.model';
import { TransaccionesService } from '../services/transacciones.service';

@Component({
  selector: 'app-historial-transacciones',
  templateUrl: './historial-transacciones.component.html',
  styleUrls: ['./historial-transacciones.component.css']
})
export class HistorialTransaccionesComponent implements OnInit {

  historialTransacciones: HistorialTransacciones[] = [];

  constructor(private transaccionesService: TransaccionesService) { }

  ngOnInit(): void {
    this.obtenerHistorialTransacciones();
  }

  obtenerHistorialTransacciones(): void {
    this.transaccionesService.obtenerHistorialTransacciones()
      .subscribe(transacciones => {
        this.historialTransacciones = transacciones;
      });
  }

}
