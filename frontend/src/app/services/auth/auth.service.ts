import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";
import { User } from '../../models/user';
import { BehaviorSubject } from 'rxjs';
import { Token } from '../../models/token';
import { Router } from '@angular/router';
import { jwtDecode, JwtPayload } from 'jwt-decode';


@Injectable({
  providedIn: 'root',
})
export class AuthService {

  tokenKey: string = 'token';
  private headers: HttpHeaders
  private baseUrl = 'http://127.0.0.1:8000/api/auth'
  isLoggedInSubject = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient, private router: Router) {
    this.headers = new HttpHeaders;
  }

  setToken(token?: string | undefined) {
    if (!token) return;
    localStorage.setItem(this.tokenKey, token);
  }
  getToken(): string | undefined {
    const token_string = localStorage.getItem(this.tokenKey) ?? "";
    if (token_string != null) {
      return token_string;
    }
    return undefined;
  }

  logout() {
    localStorage.removeItem(this.tokenKey);
    this.router.navigate(['/login']);
  }

  public async register(usuario: User) {
      return new Promise<any>((resolve, reject) => {
        this.http.post<any>(`${this.baseUrl}/register`, usuario, { headers: this.headers }).subscribe((r) => {
          resolve(true)
        }, 
        (error) => {
          reject(error.error.detail)
        });
      });

     
      // .catch(err => {
      //   const r: any = JSON.parse(err.error);
      //   r.Ok = false;
      //   r.error = this.tratarRespostaDeCadasto(err.error.detail);
      //   return r;
      // })
  }

  tratarRespostaDeCadasto(err: string) {
    if (err.toLowerCase().includes("username")) {
      return "El email ya esta registrado"
    }
    else if (err.toLowerCase().includes("email")) { }
    return ''
  }

   checkAuthStatus(): boolean /*Promise<boolean>*/ {
    // return new Promise<boolean>((resolve, reject) => {
      const token: string = localStorage.getItem(this.tokenKey) ?? '';
      try {
        const decodedToken = jwtDecode<JwtPayload>(token);
        const isTokenExpired = decodedToken.exp ? decodedToken.exp < Date.now() / 1000 : false;
        if (isTokenExpired) {

          const newToken = false //await this.renewToken(token);
          if (newToken) {
            localStorage.setItem('token', newToken);
            // resolve(true);
            return true
          }

          localStorage.removeItem('token');
          // resolve(false);
          return false

        }
        return true

      } catch (error) {
        // reject(true)
        return false
      }
      localStorage.removeItem('token');
    // });
    return false

  }

  public async login(usuario: User): Promise<boolean> {
    try {
      const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' })
      const body = new HttpParams()
        .set('grant_type', 'password')
        .set('username', usuario.email ?? "")
        .set('password', usuario.password ?? "")
        .set('client_id', 'string')
        .set('client_secret', 'string');
      const token = await this.http.post<Token>(`${this.baseUrl}/login`, body.toString(), { headers: headers }).toPromise();

      if (token) {
        this.setToken(token.access_token)
        this.isLoggedInSubject.next(true);
        return true;
      }

      return false;

    } catch (error) {
      console.log(error);
      return false;
    }
  }


  // async checkAuthStatus(): Promise<boolean> {
  //   return new Promise<boolean>((resolve) => {
  //     this.http.get<any>(`${this.baseUrl}/status`, { headers: this.headers }).subscribe(
  //       (r) => {
  //         if (r['logged'] === true) {
  //           resolve(true);
  //         } else {
  //           this.logoutUser();
  //           resolve(false);
  //         }
  //       },
  //       (error) => {
  //         if (error.status = 401) {
  //           console.error('Error checking authentication status:', error);
  //           resolve(false);
  //           return;
  //         }


  //       }
  //     );
  //   });
  // }

  public async googleLogin(): Promise<boolean>{
    try {
      const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' })
      const body = new HttpParams()
        .set('code', 'password')
        // .set('username', usuario.email ?? "")
        // .set('password', usuario.password ?? "")

      const token = await this.http.post<Token>(`${this.baseUrl}/google/callback`, body.toString(), { headers: headers }).toPromise();

      if (token) {
        this.setToken(token.access_token)
        this.isLoggedInSubject.next(true);
        return true;
      }

      return false;

    } catch (error) {
      console.log(error);
      return false;
    }
  }
}



