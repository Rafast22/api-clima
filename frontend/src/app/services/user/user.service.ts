import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '../../models/user';
import { BaseService } from '../base.service';

@Injectable({
  providedIn: 'root'
})
export class UserService extends BaseService<User, number> {
  constructor(http: HttpClient) {
    super(http)
    this.headers = new HttpHeaders;
  }

  public async updateUser(usuario: User) {
    this.headers = new HttpHeaders({ 'accept': "application/json" });
    return await this.http.put<any>(`${this.baseUrl}`, usuario, { headers: this.headers }).toPromise().then()
      .catch(ex => {
        console.log(ex);
      });
  }

  public async getUser(user_id: number) {
    this.headers = new HttpHeaders({ 'accept': "application/json" });
    return await this.http.get<User>(`${this.baseUrl}/`, { headers: this.headers }).toPromise().then()
      .catch(ex => {
        console.log(ex);
      });
  }

  public async deleteUser(user_id: number) {
    this.headers = new HttpHeaders({ 'accept': "application/json" });
    return await this.http.delete(`${this.baseUrl}/`, { headers: this.headers }).toPromise().then()
      .catch(ex => {
        console.log(ex);
      });
  }

  protected getEndpoint(): string {
    return 'user';
  }

}
