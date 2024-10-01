import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClimaActualComponent } from './clima-actual.component';

describe('ClimaActualComponent', () => {
  let component: ClimaActualComponent;
  let fixture: ComponentFixture<ClimaActualComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClimaActualComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ClimaActualComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
