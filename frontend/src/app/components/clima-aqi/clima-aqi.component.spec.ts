import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClimaAqiComponent } from './clima-aqi.component';

describe('ClimaAqiComponent', () => {
  let component: ClimaAqiComponent;
  let fixture: ComponentFixture<ClimaAqiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClimaAqiComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ClimaAqiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
