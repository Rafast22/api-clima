import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { PrincipalComponent } from './pages/principal/principal.component';
import { authGuard } from './guards/auth.guard';
import { TesteComponent } from './pages/teste/teste.component';
import { RecomendacionesCardComponent } from './components/recomendaciones-card/recomendaciones-card.component';

export const routes: Routes = [
    { path: "login", component: LoginComponent, pathMatch: "full" },
    { path: "register", component: RegisterComponent, pathMatch: "full" },
    { path: "principal", component: PrincipalComponent, pathMatch: "full", /*canActivate: [authGuard] */},
    { path: "testeAngular", component: TesteComponent, pathMatch: "full" },
    { path: "recomendaciones", component: RecomendacionesCardComponent, pathMatch: "full" },
  ];
  

