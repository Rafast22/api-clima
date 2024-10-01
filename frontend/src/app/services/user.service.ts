import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";


@Injectable({
  providedIn: 'root',
})
export class UserService {

  private apany = 'http://localhost:3000/usuario'

  constructor(private http: HttpClient) { }

  cadastrar(usuario: any) {
    return this.http.post<any>(this.apany, usuario)
  }

   async login(cuenta: any):Promise<boolean> {
    if(cuenta.email === "adrianaacosta.mv562@gmail.com" && cuenta.password === "Lmtz6404@"){
      return true;
    }
    return false;
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
    return this.http.put<any>(`${this.apany}/${usuario.id}`, usuario)
  }

 
}
