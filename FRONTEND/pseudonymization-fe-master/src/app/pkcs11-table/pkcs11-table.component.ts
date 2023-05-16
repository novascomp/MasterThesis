import {AfterViewInit, Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {ModifiableResourcesComponent} from "../general/components-general/ModifiableResourcesComponent";
import {MatPaginator} from "@angular/material/paginator";
import {MatTable} from "@angular/material/table";
import {Sample} from "../rest/model/Sample";
import {RestGeneralResponse} from "../rest/response/RestGeneralResponse";
import {Pkcs11Service} from "../rest/service/pkcs11.service";
import {NVDataSource} from "../data-source/NVDataSource";
import {PKCS11Profile} from "../rest/model/PKCS11Profile";

@Component({
  selector: 'app-pkcs11-table',
  templateUrl: './pkcs11-table.component.html',
  styleUrls: ['./pkcs11-table.component.css']
})
export class Pkcs11TableComponent extends ModifiableResourcesComponent implements AfterViewInit, OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatTable) table: MatTable<any>;
  dataSource: NVDataSource<PKCS11Profile, Pkcs11Service>;

  displayedColumns: string[] = ["id", "key_label", "status", "start", "source_location", "encryption_location", "pseud_operation", "technology"];

  dataGenerating: boolean;

  constructor(private pkcs11Service: Pkcs11Service) {
    super();
  }

  @Input()
  set initComponent(num: number) {
    this.initAll();
  }

  @Output()
  afterDone = new EventEmitter<any>();

  async ngOnInit(): Promise<any> {
    this.dataSource = new NVDataSource(this.pkcs11Service);
    Promise.resolve().then(() => this.loadPage());
  }

  ngAfterViewInit(): void {
  }

  initAll(): void {
    this.dataGenerating = false
    super.initGlobal();
  }

  pageChange(event): void {
    this.loadPage();
  }

  loadPage(): void {
    this.initGlobal();
    this.dataSource.getUserFiles(this.paginator.pageIndex + 1, this.paginator.pageSize);
  }

  commonResponse(status): void {

    const restGeneralResponse = this.pkcs11Service.getStatusCodeToGeneralResponse(status.status);
    if (restGeneralResponse === RestGeneralResponse.ok) {
      this.dataGenerating = false
      this.loadPage();
    }
  }

  sendDataToPseudonymization(datGenId, file) {
    this.afterDone.emit(file);
  }
}

