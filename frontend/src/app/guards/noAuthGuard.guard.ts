import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth/auth.service';

export const noAuthGuard: CanActivateFn = (route, state) => {
    const router = inject(Router);
    const authService = inject(AuthService);
    let _logged:boolean = /* await */authService.checkAuthStatus();
    if (!_logged) {
      return true;
    }
    // router.navigate(['/principal'])
    return false;

};
