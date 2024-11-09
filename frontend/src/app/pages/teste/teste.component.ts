import { Component } from '@angular/core';
import { ClimaCardComponent } from '../../components/clima-card/clima-card.component';
import { RecomendacionesCardComponent } from '../../components/recomendaciones-card/recomendaciones-card.component';
import { CalendarComponent } from '../../components/calendar/calendar.component';

@Component({
  selector: 'app-teste',
  standalone: true,
  imports: [RecomendacionesCardComponent],
  templateUrl: './teste.component.html',
  styleUrl: './teste.component.css'
})
export class TesteComponent {

}
