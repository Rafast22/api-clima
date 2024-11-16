import { AfterViewInit, Component, TemplateRef, ViewChild, ViewContainerRef } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NaveBarComponent } from '../../components/navebar/navebar.component';
import { RecomendacionesCardComponent } from '../../components/recomendaciones-card/recomendaciones-card.component';

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [RouterOutlet, NaveBarComponent,RecomendacionesCardComponent],
  templateUrl: './principal.component.html',
  styleUrl: './principal.component.css'
})
export class PrincipalComponent implements AfterViewInit {
  @ViewChild('telaContainer', { read: ViewContainerRef }) telaContainerRef!: ViewContainerRef;
  public rcomponent = RecomendacionesCardComponent
  constructor(){

  }
  abrirTela1(){
    this.telaContainerRef.createComponent(RecomendacionesCardComponent)

  }
  

  ngAfterViewInit(): void {

  }

}
