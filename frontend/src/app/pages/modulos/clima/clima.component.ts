import { Component } from '@angular/core';
import { ClimaActualComponent } from '../../../components/clima-actual/clima-actual.component';
import { ClimaActualDetallesComponent } from '../../../components/clima-actual-detalles/clima-actual-detalles.component';
interface pp{
  feels_like:number
  humidity:number
  uvi:number
  visibility:number
  dew_point:number
  pressure:number
}
@Component({
  selector: 'app-clima',
  standalone: true,
  imports: [
    ClimaActualComponent,
    ClimaActualDetallesComponent
  ],
  templateUrl: './clima.component.html',
  styleUrl: './clima.component.css'
})
export class ClimaComponent {
  public data:pp = <pp>{};
  constructor(){
    
    this.data.feels_like =5 
    this.data.humidity =5 
    this.data.uvi =5 
    this.data.visibility =5 
    this.data.dew_point =5 
    this.data.pressure =5 
  }
}
