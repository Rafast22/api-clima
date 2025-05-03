import { Injectable } from '@angular/core';
import { BaseService } from '../base.service';
import { Historico } from '../../models/historico';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HistoricoService extends BaseService<Historico, number> {

  constructor(http: HttpClient) {
    super(http);
    this.headers = new HttpHeaders;
  }

  getHistorico(page: number, per_page: number): Observable<Historico[]> {
    const url = `${this.baseUrl}/`;
    const params = new HttpParams()
      .set('page', page)
      .set('per_page', per_page)
    return this.http.get<Historico[]>(url, { headers: this.headers, params: params });
  }


  protected getEndpoint(): string {
    return 'historico';
  }
}
