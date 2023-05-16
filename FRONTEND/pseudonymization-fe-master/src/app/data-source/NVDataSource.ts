import {DataSource, CollectionViewer} from '@angular/cdk/collections';
import {finalize} from 'rxjs/operators';
import {Observable, BehaviorSubject} from 'rxjs';
import {HttpResponse} from '@angular/common/http';
import {RestGeneralResponse} from "../rest/response/RestGeneralResponse";
import {CryptoService} from "../rest/service/crypto.service";
import {Profile} from "../rest/model/Profile";

export class NVDataSource<T extends Profile, S extends CryptoService<T>> extends DataSource<T> {

  private content = new BehaviorSubject<T[]>([]);
  private loadingContent = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingContent.asObservable();
  public totalElements: any;
  public unavailable: boolean;

  constructor(private service: S) {
    super();
  }

  connect(collectionViewer: CollectionViewer): Observable<T[]> {
    return this.content.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.content.complete();
    this.loadingContent.complete();
  }

  getUserFiles(pageNumber: number, pageSize: number): void {
    this.loadingContent.next(true);
    this.service.getUserFiles(pageNumber, pageSize).pipe(
      finalize(() => this.loadingContent.next(false)))
      .subscribe(page => {
        this.processResponse(page);
      });
  }


  private processResponse(page: HttpResponse<T[]>): void {
    if (this.service.getStatusCodeToGeneralResponse(page.status) === RestGeneralResponse.ok) {
      this.unavailable = false;
      this.content.next(page.body);
      if (page.body.length > 0) {
        this.totalElements = page.body[0].total_elements
      } else {
        this.totalElements = 0
      }

    } else {
      this.content.next(null);
      this.unavailable = true;
    }
  }
}
