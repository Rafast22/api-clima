import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { PrincipalComponent } from './pages/principal/principal.component';
import { TesteComponent } from './pages/teste/teste.component';

export const routes: Routes = [
    { path: "teste", component: TesteComponent, pathMatch: "full" },
    { path: "login", component: LoginComponent, pathMatch: "full" },
    { path: "register", component: RegisterComponent, pathMatch: "full" },
    { path: "principal", component: PrincipalComponent, pathMatch: "full" },
    { path: "testeAngular", component: TesteComponent, pathMatch: "full" },
 
  ];
  

