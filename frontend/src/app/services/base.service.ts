import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export abstract class BaseService<T, ID> {
  protected baseUrl: string;
  protected headers: HttpHeaders;

  constructor(protected http: HttpClient) {
    this.baseUrl = 'http://127.0.0.1:8000/api';
    this.headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
  }

  getById(id: ID): Observable<T> {
    const url = `${this.baseUrl}/${this.getEndpoint()}/${id}`;
    return this.http.get<T>(url, { headers: this.headers });
  }

  create(item: T): Observable<T> {
    const url = `${this.baseUrl}/${this.getEndpoint()}`;
    return this.http.put<T>(url, item, { headers: this.headers });
  }

  update(id: ID, item: T): Observable<T> {
    const url = `${this.baseUrl}/${this.getEndpoint()}/${id}`;
    return this.http.put<T>(url, item, { headers: this.headers });
  }

  delete(id: ID): Observable<void> {
    const url = `${this.baseUrl}/${this.getEndpoint()}/${id}`;
    return this.http.delete<void>(url, { headers: this.headers });
  }

  protected abstract getEndpoint(): string;
}