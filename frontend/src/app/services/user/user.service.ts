import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '../../models/user';
import { BaseService } from '../base.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService extends BaseService<User, number> {
  constructor(http: HttpClient) {
    super(http)
    this.headers = new HttpHeaders;
  }

    getMe(): Observable<User> {
      const url = `${this.baseUrl}/me`;
      return this.http.get<User>(url, { headers: this.headers });
    }
  

  protected getEndpoint(): string {
    return 'user';
  }

}
