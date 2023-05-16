import {RestGeneralService} from "./rest-general.service";
import {Observable} from "rxjs";
import {HttpResponse} from "@angular/common/http";

export abstract class CryptoService<T> extends RestGeneralService {

  public abstract getUserFiles(pageNumber, pageSize): Observable<HttpResponse<T[]>>;
}
