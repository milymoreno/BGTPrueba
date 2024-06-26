import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BuscarAsociarFondosComponent } from './buscar-asociar-fondos/buscar-asociar-fondos.component';
import { FondosComponent } from './fondos/fondos.component';
import { CrearClienteComponent } from './crear-cliente/crear-cliente.component';
import { CrearFondoComponent } from './crear-fondos/crear-fondos.component';
import { HistorialTransaccionesComponent } from './historial-transacciones/historial-transacciones.component';



const routes: Routes = [
 
  { path: 'buscar-asociar-fondos', component:  BuscarAsociarFondosComponent },  
  { path: 'fondos', component:  FondosComponent },
  { path: 'crear-cliente', component:  CrearClienteComponent },    
  { path: 'crear-fondos', component:  CrearFondoComponent  }, 
  { path: 'historial-transacciones', component:  HistorialTransaccionesComponent   },
  { path: '', redirectTo: '/buscar-asociar-fondos', pathMatch: 'full' }
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
