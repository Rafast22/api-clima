import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";


@Injectable({
  providedIn: 'root',
})
export class UserService {

  private baseUrl = 'http://192.168.0.29:8000/'

  constructor(private http: HttpClient) { }

  cadastrar(usuario: any) {
    return this.http.post<any>(this.baseUrl, usuario)
  }

   async login(usuario: Usuario):Promise<boolean> {
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'  

    });
    let ret:boolean=false
    const body = new HttpParams()
      .set('grant_type', 'password')
      .set('username', usuario.username)
      .set('password', usuario.password) 

      .set('client_id', 'string') // Replace with your client ID
      .set('client_secret', 'string'); 
      await this.http.post(`${this.baseUrl}login`, body.toString(), { headers }).toPromise().then(r =>{
      ret=true
    })
    .catch(error => {
      ret=false
    })
    return ret
  }

  getUsuarios() {
    //return this.http.get<Array<any>>(this.apany)
    return [];
  }

  deletarUsuario(id: number) {
    //return this.http.delete<any>(`${this.apany}/${id}`)
    return true;
  }

  editarUsuario(usuario: any) {
    return this.http.put<any>(`${this.baseUrl}/${usuario.id}`, usuario)
  }

 
}

class Usuario{
  username:string;
  password:string;
  grant_type='password';
  scope=""
  client_id='string'
  client_secret='string'
  constructor(username:string, password:string){
    this.username = username;
    this.password = password;
    this.grant_type = 'password'
    this.client_id = 'string'
    this.client_secret = 'string'
  }
}