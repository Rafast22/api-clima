import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Cultivo } from '../../models/cultivo';
import { BaseService } from '../base.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CultivoService extends BaseService<Cultivo, number> {

  constructor(http: HttpClient) {
    super(http);
    this.headers = new HttpHeaders;
  }

  getByUserId(user: number): Observable<Cultivo[]> {
    const url = `${this.baseUrl}/user/${user}`;
    return this.http.get<Cultivo[]>(url, { headers: this.headers });
  }

  protected getEndpoint(): string {
    return 'cultivo';
  }

}
