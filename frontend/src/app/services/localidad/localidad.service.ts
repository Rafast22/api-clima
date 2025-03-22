import { Injectable } from '@angular/core';
import { BaseService } from '../base.service';
import { Localidad } from '../../models/localidad';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LocalidadService extends BaseService<Localidad, number> {

  constructor(http:HttpClient) {
      super(http);
  }

  getByUserId(id: number): Observable<Localidad> {
    const url = `${this.baseUrl}/${this.getEndpoint()}/user/${id}`;
    return this.http.get<Localidad>(url, { headers: this.headers });
  }

  protected getEndpoint(): string {
    return 'localidad';
  }
}
