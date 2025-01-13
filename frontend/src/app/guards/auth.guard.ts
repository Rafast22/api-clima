import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { UserService } from '../services/user/user.service';

export const authGuard: CanActivateFn = async (route, state) => {
  const router = inject(Router);
  const userService = inject(UserService);
  const _logged:boolean = await userService.checkAuthStatus().then();
  if (!_logged) {
    userService.isLoggedInSubject.next(true);
    router.navigate(['/login']);
    return false;
  }
  return true;
  // else if (_logged && state.url==='/login') {
  //   userService.isLoggedInSubject.next(true);
  //   router.navigate(['/principal']);
  //   return true;
  // }
  // else if(_logged){
  //   userService.isLoggedInSubject.next(true);
  //   return true;
  // } 
  // else{
  //   userService.isLoggedInSubject.next(false);
  //   return router.navigate(['/login']);
  // }
};
