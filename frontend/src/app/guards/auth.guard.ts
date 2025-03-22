import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth/auth.service';

export const authGuard: CanActivateFn = async (route, state) => {
  const router = inject(Router);
  const authService = inject(AuthService);
  let _logged:boolean = await authService.checkAuthStatus();
  if (!_logged) {
    router.navigate(['/login']);
    return false;
  }
  return true;

};
