import { Component, Input, ViewChild, ViewContainerRef } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

import { BreakpointObserver } from '@angular/cdk/layout';


import { NavBarComponent } from './components/navebar/navbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NavBarComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Front';
  // @ViewChild('container', { read: ViewContainerRef }) container!: ViewContainerRef;
  // @ViewChild('drawer') drawer: MatDrawer | any = undefined;

  // @Input() component: any;
  // get isMobile(): boolean {
  //   return this.breakpointObserver.isMatched('(max-width: 767px)');
  // }
  constructor(private breakpointObserver: BreakpointObserver) { }
  
  ngOnInit(): void {
  }

  // loadComponent(component: any) {
  //   this.container.clear();
  //   this.container.createComponent(component);

  // }

}
