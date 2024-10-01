import { Component } from '@angular/core';
import {MatToolbarModule} from "@angular/material/toolbar"
import {MatIconModule} from "@angular/material/icon"
import {MatMenuModule} from "@angular/material/menu"
import {MatSidenavModule} from "@angular/material/sidenav"
import {MatListModule} from "@angular/material/list"
import { RouterOutlet } from '@angular/router';
import {MatBadgeModule} from '@angular/material/badge';
import {MatButtonModule} from "@angular/material/button"



@Component({
  selector: 'app-navebar',
  templateUrl: './navebar.component.html',
  styleUrls: ['./navebar.component.css'],
  standalone:true,
  imports :[ MatToolbarModule, MatIconModule,
    MatMenuModule,
    MatSidenavModule, MatListModule, RouterOutlet, MatBadgeModule, MatButtonModule ]
})
export class NaveBarComponent {
  badgevisible = false;
  badgevisibility() {
    this.badgevisible = true;
  }
}
