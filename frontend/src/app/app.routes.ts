import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { PrincipalComponent } from './pages/principal/principal.component';
import { ClimaComponent } from './pages/modulos/clima/clima.component';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
    { path: "", component: LoginComponent, pathMatch: "full",  },
    { path: "login", component: LoginComponent, pathMatch: "full" },
    { path: "register", component: RegisterComponent, pathMatch: "full" },
    { path: "principal", component: PrincipalComponent, pathMatch: "full", canActivate: [authGuard] },
    
 
  ];
  

