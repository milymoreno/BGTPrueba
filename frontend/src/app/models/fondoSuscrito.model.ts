// models/fondo.ts
export interface FondoSuscrito {
    fondoId: string;
    montoSuscrito: number;
    fechaSuscripcion:string;
    selected?: boolean; // Campo opcional para selección en UI
  }
  