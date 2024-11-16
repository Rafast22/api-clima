import { Component, Input, ViewChild, ViewContainerRef } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { MatIconModule, MatIconRegistry } from "@angular/material/icon";
import { DomSanitizer } from "@angular/platform-browser";
import { PrincipalComponent } from './pages/principal/principal.component';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MatBadgeModule } from '@angular/material/badge';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule, MatDrawer } from '@angular/material/sidenav';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MatToolbarModule, MatIconModule, MatMenuModule, MatSidenavModule, 
    MatListModule, RouterOutlet, MatBadgeModule, MatButtonModule, MatTabsModule, PrincipalComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Front';
  @ViewChild('container', { read: ViewContainerRef }) container!: ViewContainerRef;
  @ViewChild('drawer') drawer: MatDrawer | any = undefined;

  @Input() component: any;
  get isMobile(): boolean {
    return this.breakpointObserver.isMatched('(max-width: 767px)');
  }
  constructor(private breakpointObserver: BreakpointObserver, private router:Router) { }
  
  ngOnInit(): void {
    // this.router.navigate(['/recomendaciones']);
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
