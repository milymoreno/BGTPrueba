import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HistorialTransacciones } from '../models/historial-transacciones.model'; // Asegúrate de importar la interfaz

@Injectable({
  providedIn: 'root'
})
export class TransaccionesService {

  private apiUrl = 'http://localhost:8082/historialTransacciones';

  constructor(private http: HttpClient) { }

  obtenerHistorialTransacciones(): Observable<HistorialTransacciones[]> {
    return this.http.get<HistorialTransacciones[]>(`${this.apiUrl}`);
  }

  /*guardarHistorialTransacciones(transacciones: HistorialTransacciones[]): Observable<any> {
    return this.http.post(`${this.apiUrl}`, transacciones);
  }*/
  guardarHistorialTransacciones(transacciones: HistorialTransacciones[]): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}`, transacciones);
  }

}
