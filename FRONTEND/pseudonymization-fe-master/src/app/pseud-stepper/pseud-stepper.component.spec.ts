import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PseudStepperComponent } from './pseud-stepper.component';

describe('CommitteeStepperComponent', () => {
  let component: PseudStepperComponent;
  let fixture: ComponentFixture<PseudStepperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PseudStepperComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PseudStepperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
