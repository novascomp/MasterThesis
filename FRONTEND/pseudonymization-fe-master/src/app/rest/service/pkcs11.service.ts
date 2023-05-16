import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient, HttpParams, HttpResponse} from '@angular/common/http';
import {catchError} from 'rxjs/operators';
import {environment} from "../../../environments/environment";
import {OktaAuthService} from "../../security/okta-auth.service";
import {PKCS11Profile} from "../model/PKCS11Profile";
import {CryptoService} from "./crypto.service";
import {PseudonymizationService} from "./pseudonymization.service";
import {Sample} from "../model/Sample";
import {EncryptHTTPS} from "../model/encrypt/EncryptHTTPS";

@Injectable({
  providedIn: 'root'
})
export class Pkcs11Service extends PseudonymizationService<PKCS11Profile> {

  constructor(public http: HttpClient, public oktaAuth: OktaAuthService) {
    super(environment.pkcs11Service, http, oktaAuth);
  }

  public pseudonymize(model: EncryptHTTPS)
    : Observable<HttpResponse<any>> {
    const body = JSON.stringify(model);
    return this.http
      .post<any>(this.baseURL + '/v1/pseud/https', body, {
        headers: this.globalHeaders,
        params: new HttpParams(),
        observe: 'response',
      }).pipe(
        catchError(this.handleErrorGeneral)
      );
  }

  public getUserFiles(pageNumber, pageSize)
    : Observable<HttpResponse<PKCS11Profile[]>> {
    return this.http
      .get<PKCS11Profile[]>(this.baseURL + '/v1/user/files',
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
}
