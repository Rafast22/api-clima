import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NaveBarComponent } from '../../components/navebar/navebar.component';

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [RouterOutlet, NaveBarComponent],
  templateUrl: './principal.component.html',
  styleUrl: './principal.component.css'
})
export class PrincipalComponent {

}
