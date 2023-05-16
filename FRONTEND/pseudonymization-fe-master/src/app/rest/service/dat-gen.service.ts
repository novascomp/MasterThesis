import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient, HttpParams, HttpResponse} from '@angular/common/http';
import {catchError} from 'rxjs/operators';
import {environment} from "../../../environments/environment";
import {OktaAuthService} from "../../security/okta-auth.service";
import {DatGenProfile} from "../model/DatGenProfile";
import {Sample} from "../model/Sample";
import {CryptoService} from "./crypto.service";
import {DatGenSchema} from "../model/DatGenSchema";

@Injectable({
  providedIn: 'root'
})
export class DatGenService extends CryptoService<DatGenProfile> {

  constructor(public http: HttpClient, public oktaAuth: OktaAuthService) {
    super(environment.datGenService, http, oktaAuth);
  }

  public getData(sample: Sample)
    : Observable<HttpResponse<any>> {
    const body = JSON.stringify(sample);
    return this.http
      .post<any>(this.baseURL + '/v1/genData', body, {
        headers: this.globalHeaders,
        params: new HttpParams(),
        observe: 'response',
      }).pipe(
        catchError(this.handleErrorGeneral)
      );
  }

  public getUserFiles(pageNumber, pageSize)
    : Observable<HttpResponse<DatGenProfile[]>> {
    return this.http
      .get<DatGenProfile[]>(this.baseURL + '/v1/user/files',
        {
          headers: this.globalHeaders,
          params: new HttpParams()
            .set('page_id', pageNumber)
            .set('per_page', pageSize),
          observe: 'response',
        }).pipe(
        catchError(super.handleErrorGeneral)
      );
  }

  public getSchema()
    : Observable<HttpResponse<DatGenSchema>> {
    return this.http
      .get<DatGenSchema>(this.baseURL + '/v1/schema',
        {
          headers: this.globalHeaders,
          observe: 'response',
        }).pipe(
        catchError(super.handleErrorGeneral)
      );
  }
}
