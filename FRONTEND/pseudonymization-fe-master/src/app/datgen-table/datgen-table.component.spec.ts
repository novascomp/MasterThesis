import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatgenTableComponent } from './datgen-table.component';

describe('DatgenTableComponent', () => {
  let component: DatgenTableComponent;
  let fixture: ComponentFixture<DatgenTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DatgenTableComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DatgenTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
