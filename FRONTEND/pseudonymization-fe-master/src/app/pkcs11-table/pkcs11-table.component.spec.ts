import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pkcs11TableComponent } from './pkcs11-table.component';

describe('Pkcs11TableComponent', () => {
  let component: Pkcs11TableComponent;
  let fixture: ComponentFixture<Pkcs11TableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ Pkcs11TableComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Pkcs11TableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
