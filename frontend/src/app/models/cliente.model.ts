import { Fondo } from './fondo.model';
import { Transaccion } from './transaccion.model';

export interface Cliente {
  Id: string;
  Nombres: string;
  Apellidos: string;
  tipoIdentificacion: string;
  numeroIdentificacion: string;
  Email: string;
  Telefono: string;
  saldoActual: number;
  fondosSuscritos: Fondo[];
  historialTransacciones: Transaccion[];
  preferenciaNotificacion: string;
}
