import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { baseUrl } from '../../environments/environment.development'
import { lastValueFrom, take } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PredicService {
  headers:HttpHeaders;
  constructor(private http: HttpClient) {
    this.headers = new HttpHeaders({
      'accept': "application/json",
      'Content-Type': 'application/x-www-form-urlencoded'  
    });

   }

    public getPredictData(user_id:number):Promise<any>{
      const body = new HttpParams()
        .set('user_id', user_id ?? "")
      const request$ = this.http.get<any>(`${baseUrl}/historico/${user_id}`, { headers: this.headers }).pipe(take(1));
      return lastValueFrom(request$);
    }
    
    public getPredictDataDay(user_id:number, Day:string):Promise<any>{
      const body = new HttpParams()
        .set('dia', Day)
      const request$ = this.http.post<any>(`${baseUrl}/previcion/${user_id}?dia=${Day}`, { headers: this.headers }).pipe(take(1));
      return lastValueFrom(request$);
    }

}
