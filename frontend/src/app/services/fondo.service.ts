import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Fondo } from '../models/fondo.model';


@Injectable({
  providedIn: 'root'
})
export class FondoService {

  private apiUrl = 'http://localhost:8082/fondos'; // Asegúrate de que la URL es correcta

  constructor(private http: HttpClient) { }

  getFondos(): Observable<Fondo[]> {
    return this.http.get<Fondo[]>(this.apiUrl);
  }

  validarSaldo(clienteId: string, fondoId: string): Observable<string> {
    return this.http.get<string>(`${this.apiUrl}/validar-saldo?clienteId=${clienteId}&fondoId=${fondoId}`);
  }
}
