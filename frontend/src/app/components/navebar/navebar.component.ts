import { AfterViewInit, Component, Input, ViewChild, ViewContainerRef } from '@angular/core';
import { MatToolbarModule } from "@angular/material/toolbar"
import { MatIconModule } from "@angular/material/icon"
import { MatMenuModule } from "@angular/material/menu"
import { MatSidenavModule } from "@angular/material/sidenav"
import { MatListModule } from "@angular/material/list"
import { RouterOutlet } from '@angular/router';
import { MatBadgeModule } from '@angular/material/badge';
import { MatButtonModule } from "@angular/material/button"
import { RecomendacionesCardComponent } from '../recomendaciones-card/recomendaciones-card.component';



@Component({
  selector: 'app-navebar',
  templateUrl: './navebar.component.html',
  styleUrls: ['./navebar.component.css'],
  standalone: true,
  imports: [MatToolbarModule, MatIconModule,
    MatMenuModule,
    MatSidenavModule, MatListModule, RouterOutlet, MatBadgeModule, MatButtonModule, RecomendacionesCardComponent]
})
export class NaveBarComponent implements AfterViewInit {
  @ViewChild('container', { read: ViewContainerRef }) container!: ViewContainerRef;
  @Input() component: any;

  constructor() { }
  // ngOnChanges() {
  //   // if (changes['component'] && !changes['component'].isFirstChange()) { 
  //   //   this.loadComponent(this.component);
  //   // }

  //   if (this.component) {
  //     this.loadComponent(this.component);
  //   }
  // }

  ngAfterViewInit() {
    if (this.component) {
      this.loadComponent(this.component);
    }
  }

  loadComponent(component: any) {
    this.container.clear();
    this.container.createComponent(component);

  }

  badgevisible = false;
  badgevisibility() {
    this.badgevisible = true;
  }
}
