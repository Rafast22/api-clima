import { AfterViewInit, Component, ViewChild, ViewContainerRef } from '@angular/core';
import { NavBarComponent } from '../../components/navebar/navbar.component';

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [NavBarComponent],
  templateUrl: './principal.component.html',
  styleUrl: './principal.component.css'
})
export class PrincipalComponent implements AfterViewInit {
  constructor(){}
 
  ngAfterViewInit(): void {}

}
