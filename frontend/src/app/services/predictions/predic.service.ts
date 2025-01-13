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

    public getPredictData( tipo:number, cultivo:number, fecha_inicial?:string, fecha_final?:string):Promise<any>{
      const params = new HttpParams()
        .set('fecha_inicio', fecha_inicial ?? "")
        .set('fecha_final', fecha_final ?? "")
        .set('tipo', tipo ?? "")
        .set('cultivo', cultivo ?? "")
        return lastValueFrom(
          this.http.post<any>(`${baseUrl}/previciones`, null, {
            headers: this.headers,
            params
          })
        );
    
    }
    
    public getPredictDataDay(user_id:number, Day:string):Promise<any>{
      const body = new HttpParams()
        .set('dia', Day)
      const request$ = this.http.post<any>(`${baseUrl}/previcion/${user_id}?dia=${Day}`, { headers: this.headers }).pipe(take(1));
      return lastValueFrom(request$);
    }

}
