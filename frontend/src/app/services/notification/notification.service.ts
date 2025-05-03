import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { snackBarColors } from '../../models/snackBar';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  constructor(private snackBar:MatSnackBar) { }

    abrirNotificacaoParametros(message:string, action:string, duration:number, snackAction:string ) {
      
      this.snackBar.open(message, action, {
        duration: duration, 
        horizontalPosition: 'center',
        verticalPosition: 'top',
        panelClass:snackAction
      });
    }

    abrirNotificacionMensaje(message:string, action:string){
      this.abrirNotificacaoParametros(message, 'Cerrar', 2000, action)
    }
}
