import {AfterViewInit, Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {MatPaginator} from "@angular/material/paginator";
import {ModifiableResourcesComponent} from "../general/components-general/ModifiableResourcesComponent";
import {DatGenService} from "../rest/service/dat-gen.service";
import {RestGeneralResponse} from "../rest/response/RestGeneralResponse";
import {Sample} from "../rest/model/Sample";
import {MatTable} from '@angular/material/table';
import {NVDataSource} from "../data-source/NVDataSource";
import {DatGenProfile} from "../rest/model/DatGenProfile";
import {Pkcs11Service} from "../rest/service/pkcs11.service";
import {PythonPseudFromHTTPS} from "../rest/model/encrypt/PythonPseudFromHTTPS";
import {DatGenEncryptSchema} from '../rest/schema/datGenEncryptSchema';

@Component({
  selector: 'app-datgen-table',
  templateUrl: './datgen-table.component.html',
  styleUrls: ['./datgen-table.component.css']
})
export class DatgenTableComponent extends ModifiableResourcesComponent implements AfterViewInit, OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatTable) table: MatTable<any>;
  dataSource: NVDataSource<DatGenProfile, DatGenService>;

  displayedColumns: string[] = ["id", "location"];

  dataGenerating: boolean;

  constructor(private datGenService: DatGenService, private pseudonymizationModule: Pkcs11Service) {
    super();
  }

  // @ts-ignore
  @Input()
  set initComponent(num: number) {
    this.initAll();
  }

  @Output()
  afterDone = new EventEmitter<any>();

  async ngOnInit(): Promise<any> {
    this.dataSource = new NVDataSource(this.datGenService);
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

  sendDataToPseudonymization(datGenId, file) {
    this.initGlobal();
    this.afterDone.emit(file);
    //this.pseudonymizationModule.pseudonymize(pkcs11EncryptHTTPS)
    //  .subscribe(status => this.pkcs11Response(status));
  }

  private getRandomStringFourDigit() {
    return this.getRandomStringDigit() + this.getRandomStringDigit() + this.getRandomStringDigit() + this.getRandomStringDigit();
  }

  private getRandomStringDigit() {
    return new Number(Math.floor(Math.random() * 10)).toString()
  }


  genData() {
    this.initGlobal();
    var sample = new Sample();
    sample.size = 1000;

    this.dataGenerating = true
    this.datGenService.getData(sample)
      .subscribe(status => this.commonResponse(status));

  }

  commonResponse(status): void {
    const restGeneralResponse = this.datGenService.getStatusCodeToGeneralResponse(status.status);
    if (restGeneralResponse === RestGeneralResponse.ok) {
      this.dataGenerating = false
      this.loadPage();
    }
  }

  pkcs11Response(status): void {

    const restGeneralResponse = this.datGenService.getStatusCodeToGeneralResponse(status.status);
    if (restGeneralResponse === RestGeneralResponse.ok) {
      this.afterDone.emit(restGeneralResponse);
      this.loadPage();
    }
  }
}

