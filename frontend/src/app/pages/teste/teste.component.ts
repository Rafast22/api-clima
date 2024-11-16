import { Component } from '@angular/core';
import { ClimaCardComponent } from '../../components/clima-card/clima-card.component';
import { RecomendacionesCardComponent } from '../../components/recomendaciones-card/recomendaciones-card.component';
import { CalendarComponent } from '../../components/calendar/calendar.component';
import {MatTabsModule} from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { PrincipalComponent } from '../principal/principal.component';

@Component({
  selector: 'app-teste',
  standalone: true,
  imports: [RecomendacionesCardComponent, MatTabsModule, MatIconModule, PrincipalComponent],
  templateUrl: './teste.component.html',
  styleUrl: './teste.component.css'
})
export class TesteComponent {
  activeLink:any
  public links:any[]=[]
  constructor(){
    this.links.push("principal")
  }
}
