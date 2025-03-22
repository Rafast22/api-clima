import { AfterViewInit, Component, inject, Input, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { MatToolbarModule } from "@angular/material/toolbar"
import { MatIconModule } from "@angular/material/icon"
import { MatMenuModule } from "@angular/material/menu"
import { MatDrawer, MatSidenavModule } from "@angular/material/sidenav"
import { MatListModule } from "@angular/material/list"
import { Router, RouterOutlet } from '@angular/router';
import { MatBadgeModule } from '@angular/material/badge';
import { MatButtonModule } from "@angular/material/button"
import { BreakpointObserver } from '@angular/cdk/layout';
import { MatTabsModule } from '@angular/material/tabs';
import { AuthService } from '../../services/auth/auth.service';
import { MatDialog } from '@angular/material/dialog';
import { HistoricoComponent } from '../../pages/user/historico/historico.component';
import { SettingsComponent } from '../../pages/user/settings/settings.component';
import { CultivosComponent } from '../../pages/user/cultivos/cultivos.component';
@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
  standalone: true,
  imports: [MatToolbarModule, MatIconModule, MatMenuModule, MatSidenavModule,
    MatListModule, RouterOutlet, MatBadgeModule, MatButtonModule, MatTabsModule]
})
export class NavBarComponent implements AfterViewInit, OnInit {
  @ViewChild('container', { read: ViewContainerRef }) container!: ViewContainerRef;
  @ViewChild('drawer') drawer: MatDrawer | any = undefined;
  readonly dialog = inject(MatDialog);

  private small: boolean = false;
  get isMobile(): boolean {
    const isSmall = this.breakpointObserver.isMatched('(max-width: 767px)');
    if (this.small != isSmall) {
      if (this.drawer)
        if (isSmall)
          this.drawer.close();
        else
          this.drawer.open();
        this.small = isSmall;
      
    }
    return isSmall;
  }
  constructor(
    private breakpointObserver: BreakpointObserver,
    protected auth: AuthService,
    private router: Router) { }

  ngOnInit(): void {
  }
  ngAfterViewInit() { }

  loadComponent(component: any) {
    this.container.clear();
    this.container.createComponent(component);

  }

  badgevisible = false;
  badgevisibility() {
    this.badgevisible = true;
  }

  logout() {
    this.auth.logout();
  }

  openModalHistory() {
    // historico
    const dialogRef = this.dialog.open(HistoricoComponent, {
      data: {},
    });

  }

  openModalSettings() {
    const dialogRef = this.dialog.open(SettingsComponent, {
      data: {},
    });

  }

  openModalCultivo() {
    const dialogRef = this.dialog.open(CultivosComponent, {
      data: {},
    });

  }

}
