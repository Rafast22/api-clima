import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";
import { User } from './user';
import { BehaviorSubject } from 'rxjs';


@Injectable({
  providedIn: 'root',
})
export class UserService {
  
  tokenKey:string = 'token';
  private headers:HttpHeaders
  private baseUrl = 'http://127.0.0.1:8000/api/'
  isLoggedInSubject = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {
    this.headers = new HttpHeaders({
      'accept': "application/json",
      'Content-Type': 'application/x-www-form-urlencoded'  
    });
   }


   getAuthenticatedHeaders(): HttpHeaders {
    const token = this.getToken();
    if (token) {
      return new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
      });
    }
    return new HttpHeaders({
      'Accept': 'application/json'
    });
  }
  setToken(token?: string | undefined){
    // First, serialize it (but just if token is not string type).
    if(!token) return;
    // const tokenString:string = JSON.stringify( token );
    localStorage.setItem(this.tokenKey, token);
  }
  getToken(): string{
    const token_string = localStorage.getItem( this.tokenKey ) ?? "";
    let token:string = "";
    if( token_string !=null){
      token = token_string;
    }
    return token;
  }

  logoutUser() {
    localStorage.removeItem(this.tokenKey)
  }

  public async cadastrar(usuario: User) {
    return await this.http.post<any>(`${this.baseUrl}/register`, usuario, { headers:this.headers }).toPromise().then(r => {
      console.log(r);
    })
  }

  public async login(usuario: User):Promise<boolean> {
    let ret:boolean=false
    const body = new HttpParams()
      .set('grant_type', 'password')
      .set('username', usuario.username ?? "")
      .set('password', usuario.password ?? "") 
      .set('client_id', 'string') 
      .set('client_secret', 'string'); 
      await this.http.post<Token>(`${this.baseUrl}login`, body.toString(), { headers:this.headers }).toPromise().then(r =>{
        if(r){
          this.setToken(r.access_token)
          ret = true;
          localStorage.setItem('isLoggedIn', 'true');
          return;
        }
        ret = false;
      })
      .catch(error => {
        console.log(error)
      });
    return ret
  }
  
  public async EditarUsuario(usuario: User) {
    const body = this.getAuthenticatedHeaders()
      .set('Content-Type', 'application/json')
      .set('accept', 'application/json');
    return await this.http.put<any>(`${this.baseUrl}/user`, usuario, { headers:this.headers }).toPromise().then();
  }

  async checkAuthStatus():Promise<boolean> {
    const body = this.getAuthenticatedHeaders()
    .set('Content-Type', 'application/json')
    .set('accept', 'application/json');
    return new Promise<boolean>((resolve) => {
      this.http.get<any>(`${this.baseUrl}status`, { headers: this.headers }).subscribe(
        (r) => {
          if (r['logged'] === true) {
            resolve(true);
          } else {
            this.logoutUser();
            resolve(false);
          }
        },
        (error) => {
          if (error.status = 401){
            console.error('Error checking authentication status:', error);
            resolve(false); 
            return;
          }
          
          
        }
      );
    });
  }


 
}

interface Token{
  access_token:string;
  token_type:string;
}

