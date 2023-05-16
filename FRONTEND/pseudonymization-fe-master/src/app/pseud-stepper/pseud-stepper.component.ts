import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {PseudStepperInit} from './PseudStepperInit';
import {ModifiableResourcesComponent} from "../general/components-general/ModifiableResourcesComponent";
import {MatChipEditedEvent, MatChipInputEvent} from "@angular/material/chips";
import {COMMA, ENTER} from "@angular/cdk/keycodes";
import {RestGeneralResponse} from "../rest/response/RestGeneralResponse";
import {DatGenService} from "../rest/service/dat-gen.service";
import {MatRadioChange, MatRadioGroup} from "@angular/material/radio";
import {PythonPseudFromHTTPS} from "../rest/model/encrypt/PythonPseudFromHTTPS";
import {Pkcs11Service} from "../rest/service/pkcs11.service";
import {Router} from "@angular/router";

export interface Col {
  name: string;
}

@Component({
  selector: 'app-pseud-stepper',
  templateUrl: './pseud-stepper.component.html',
  styleUrls: ['./pseud-stepper.component.css']
})
export class PseudStepperComponent extends ModifiableResourcesComponent implements OnInit {

  addOnBlur = true;
  readonly separatorKeysCodes = [ENTER, COMMA] as const;
  cols: Col[] = [];

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add our fruit
    if (value) {
      this.cols.push({name: value});
    }

    // Clear the input value
    event.chipInput!.clear();
  }

  remove(fruit: Col): void {
    const index = this.cols.indexOf(fruit);

    if (index >= 0) {
      this.cols.splice(index, 1);
    }
  }

  edit(fruit: Col, event: MatChipEditedEvent) {
    const value = event.value.trim();

    // Remove fruit if it no longer has a name
    if (!value) {
      this.remove(fruit);
      return;
    }

    // Edit existing fruit
    const index = this.cols.indexOf(fruit);
    if (index >= 0) {
      this.cols[index].name = value;
    }
  }

  schema = [];
  isLinear = false;
  colsFormGroup: FormGroup;
  methodForm: FormGroup;

  invalidForm: boolean;

  pkcs11EncryptHTTPS: PythonPseudFromHTTPS;

  fileLocation: string;

  constructor(private router: Router, private datGenService: DatGenService, private pseudonymizationModule: Pkcs11Service, private formBuilder: FormBuilder) {
    super();
  }

  @Input()
  set initComponent(fileLocation: string) {
    this.fileLocation = fileLocation;
  }

  @Output() afterDone = new EventEmitter<any>();

  async ngOnInit(): Promise<any> {
    this.pkcs11EncryptHTTPS = new PythonPseudFromHTTPS()
    this.colsFormGroup = this.formBuilder.group({});
    this.methodForm = this.formBuilder.group({});
    const schemaPromise = this.datGenService.getSchema().toPromise();
    Promise.all([schemaPromise]).then(this.processResponse.bind(this)).finally(this.interpretResponse.bind(this));
  }

  private processResponse([schemaPromise]): void {
    const myOrganizationsGeneralResponse = this.datGenService.getStatusCodeToGeneralResponse(schemaPromise.status);
    if (myOrganizationsGeneralResponse === RestGeneralResponse.ok) {
      this.schema = schemaPromise.body.schema;
    } else {
      this.serverUnavailable = true;
    }
  }

  public setTechnology(event: MatRadioChange): void {
    this.pkcs11EncryptHTTPS.technology = event.value
  }


  public setPseudOperation(event: MatRadioChange): void {
    this.pkcs11EncryptHTTPS.pseud_operation = event.value
  }

  private interpretResponse(): void {

    for (var col of this.schema) {
      this.cols.push({name: col});
    }
  }

  public submit(): void {
    this.pkcs11EncryptHTTPS.col_names_to_encrypt = []

    for (var col of this.cols) {
      this.pkcs11EncryptHTTPS.col_names_to_encrypt.push(col.name)
    }
    this.pkcs11EncryptHTTPS.key_label = "datGen_test";
    this.pkcs11EncryptHTTPS.file = this.fileLocation

    this.pseudonymizationModule.pseudonymize(this.pkcs11EncryptHTTPS)
      .subscribe(status => this.pkcs11Response(status));
  }

  pkcs11Response(status): void {

    const restGeneralResponse = this.datGenService.getStatusCodeToGeneralResponse(status.status);
    if (restGeneralResponse === RestGeneralResponse.ok) {
      this.afterDone.emit(this.pkcs11EncryptHTTPS);
    }
  }

}
