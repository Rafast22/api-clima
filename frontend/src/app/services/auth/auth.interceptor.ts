import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { UserService } from '../user/user.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // const authToken = localStorage.getItem('authToken');
  const token= inject(UserService)
  const authToken = token.getToken();
  const authReq = req.clone({
    setHeaders: {
      Authorization: `Bearer ${authToken}`
    }
  });
  console.log("auth interceptor", authReq);
  return next(authReq);
};