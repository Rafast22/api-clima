import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../../auth/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // const authToken = localStorage.getItem('authToken');
  const token = inject(AuthService)
  const authToken = token.getToken();
  const dict = {
    Accept: "application/json"
  };

  if (!req.headers.get("Content-Type")) {
    Object.assign(dict, { "Content-Type": `application/json` })
  }

  if (authToken) {
    Object.assign(dict, { 'Authorization': `Bearer ${authToken}` })
  }
  const authReq = req.clone({
    setHeaders: dict
  });
  // console.log("auth interceptor", authReq);
  return next(authReq);
};