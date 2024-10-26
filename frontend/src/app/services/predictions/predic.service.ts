import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PredicService {
  private baseUrl = 'http://192.168.0.29:8000/'

  constructor(private http: HttpClient) { }
  public getPredictData():Promise<>{}
}
