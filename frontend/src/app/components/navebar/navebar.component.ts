import { AfterViewInit, Component, Input, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { MatToolbarModule } from "@angular/material/toolbar"
import { MatIconModule } from "@angular/material/icon"
import { MatMenuModule } from "@angular/material/menu"
import { MatDrawer, MatSidenavModule } from "@angular/material/sidenav"
import { MatListModule } from "@angular/material/list"
import { Router, RouterOutlet } from '@angular/router';
import { MatBadgeModule } from '@angular/material/badge';
import { MatButtonModule } from "@angular/material/button"
import { RecomendacionesCardComponent } from '../recomendaciones-card/recomendaciones-card.component';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MatTabsModule } from '@angular/material/tabs';
import { PrincipalComponent } from '../../pages/principal/principal.component';



@Component({
  selector: 'app-navebar',
  templateUrl: './navebar.component.html',
  styleUrls: ['./navebar.component.css'],
  standalone: true,
  imports: [MatToolbarModule, MatIconModule, MatMenuModule, MatSidenavModule, 
    MatListModule, RouterOutlet, MatBadgeModule, MatButtonModule, MatTabsModule, PrincipalComponent]
})
export class NaveBarComponent implements AfterViewInit, OnInit {
  @ViewChild('container', { read: ViewContainerRef }) container!: ViewContainerRef;
  @ViewChild('drawer') drawer: MatDrawer | any = undefined;

  @Input() component: any;
  get isMobile(): boolean {
    return this.breakpointObserver.isMatched('(max-width: 767px)');
  }
  constructor(private breakpointObserver: BreakpointObserver, private router:Router) { }
  
  ngOnInit(): void {
    this.router.navigate(['/recomendaciones']);
  }
  ngAfterViewInit() {
    if (this.component) {
      // this.loadComponent(this.component);
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
