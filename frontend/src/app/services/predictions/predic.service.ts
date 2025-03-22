import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom, take } from 'rxjs';
import { BaseService } from '../base.service';
import { Predict } from '../../models/predict';

@Injectable({
  providedIn: 'root'
})
export class PredicService extends BaseService<Predict, number> {
  aheaders: HttpHeaders;
  constructor(http: HttpClient) {
    super(http);
    this.aheaders = new HttpHeaders({
      'accept': "application/json",
      'Content-Type': 'application/x-www-form-urlencoded'
    });

  }

  public getPredictWeekByDate(fecha_inicial: Date, fecha_final: Date): Promise<any> {
    const params = new HttpParams()
      .set('fecha_inicio', fecha_inicial.toJSON())
      .set('fecha_final', fecha_final.toJSON())

    return lastValueFrom(
      this.http.post<any>(`${this.baseUrl}/week/date`, null, {
        headers: this.headers,
        params
      })
    );

  }

  public getPredictWeek(): Promise<any> {
    const params = new HttpParams()
      .set('localidad', 1)
    // return lastValueFrom(
    //   this.http.get<any>(`${this.baseUrl}/${this.getEndpoint()}/week`, {
    //     headers: this.headers,
    //     params: params
    //   })
    // );
    return this.http.get<any>(`${this.baseUrl}/${this.getEndpoint()}/week`, {
      headers: this.headers,
      params: params
    }).toPromise()

  }


  public getPredictDataByRange(first: Date, last: Date, tipo: number, cultivo: number): Promise<any> {
    const params = new HttpParams()
    .set('fecha_inicio', first.toJSON())
    .set('fecha_fin', last.toJSON())
    .set('tipo', Number(tipo))
    .set('cultivo', Number(cultivo))
    .set('localidad', 1)
    const request$ = this.http.post<any>(`${this.baseUrl}/${this.getEndpoint()}/range`,null ,{ headers: this.headers, params: params }).pipe(take(1));
    return lastValueFrom(request$);
  }

  public getPredictDataDate(Day: Date): Promise<any> {
    const params = new HttpParams()
      // .set('tipo', tipo)
      // .set('cultivo', cultivo)
      // .set('localidad', localidad)
      .set('day', Day.toJSON())

    const request$ = this.http.post<any>(`${this.baseUrl}/${this.getEndpoint()}/day`, null, { headers: this.headers, params: params }).pipe(take(1));
    return lastValueFrom(request$);
  }

  protected getEndpoint(): string {
    return 'user/weather/forecast';
  }


}
