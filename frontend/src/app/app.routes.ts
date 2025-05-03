import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { authGuard } from './guards/auth.guard';
import { RecomendacionesComponent } from './pages/recomendaciones/recomendaciones.component';
import { EmailVerifyComponent } from './pages/email-verify/email-verify.component';
import { HistoricoComponent } from './pages/user/historico/historico.component';
import { noAuthGuard } from './guards/noAuthGuard.guard';
import { ForgotPasswordComponent } from './pages/forgot-password/forgot-password.component';

export const routes: Routes = [
    { path: "login", component: LoginComponent, pathMatch: "full", canActivate: [noAuthGuard]},
    { path: "register", component: RegisterComponent, pathMatch: "full", canActivate: [noAuthGuard]},
    { path: "recuperar-contrasena", component: ForgotPasswordComponent, pathMatch: "full", canActivate: [noAuthGuard]},
    { path: "verificar-email", component: EmailVerifyComponent, pathMatch: "full", canActivate: [noAuthGuard]},
    { path: "recomendaciones", component: RecomendacionesComponent, pathMatch: "full", canActivate: [authGuard]},
    { path: "**", pathMatch: "full", redirectTo:"login"},

  ];
  


