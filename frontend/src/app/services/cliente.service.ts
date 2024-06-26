import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Cliente } from '../models/cliente.model';
import { Fondo } from '../models/fondo.model';
import { Transaccion } from '../models/transaccion.model';



@Injectable({
  providedIn: 'root'
})
export class ClienteService {
  private apiUrl = 'http://localhost:8082/clientes';

  constructor(private http: HttpClient) { }

  buscarClientePorNumeroIdentificacion(numeroIdentificacion: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/buscar/${numeroIdentificacion}`);
  }

  agregarCliente(cliente: Cliente): Observable<any> {
    return this.http.post<any>(this.apiUrl, cliente);
  }


  asociarFondos(clienteId: string, fondosSuscritos: Fondo[]): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/${clienteId}/fondos`, fondosSuscritos);
  }

  realizarTransaccion(clienteId: string, transacciones: Transaccion[]): Observable<any> {
    const url = `${this.apiUrl}/${clienteId}/transacciones`;
    
    // Imprimir el JSON que se va a enviar
    console.log('JSON a enviar a la transacción:', transacciones);

    // Enviar la solicitud HTTP POST al backend
    return this.http.post(url, transacciones);
  }

  getCliente(clienteId: string): Observable<Cliente> {
    const url = `${this.apiUrl}/${clienteId}`;
    return this.http.get<Cliente>(url);
  }
  
  
  actualizarTransaccionesCliente(clienteId: string, transacciones: any[]): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${clienteId}/actualizarTransacciones`, transacciones);
  }
}
