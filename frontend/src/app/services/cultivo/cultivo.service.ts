import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Cultivo } from '../../models/cultivo';
import { BaseService } from '../base.service';

@Injectable({
  providedIn: 'root'
})
export class CultivoService extends BaseService<Cultivo, number>{
  // private baseUrl = 'http://127.0.0.1:8000/api/auth'
  // private headers: HttpHeaders

  constructor(http: HttpClient) {
    super(http);
    this.headers = new HttpHeaders;
  }

  // public async getByCodigo(cultivo_id: number) {
  //   this.headers = new HttpHeaders({ 'accept': "application/json" });
  //   return await this.http.get<Cultivo>(`${this.baseUrl}/`, { headers: this.headers }).toPromise().then()
  //     .catch(ex => {
  //       console.log(ex);
  //     });
  // }

  protected getEndpoint(): string {
    return 'cultivo';
  }

}
