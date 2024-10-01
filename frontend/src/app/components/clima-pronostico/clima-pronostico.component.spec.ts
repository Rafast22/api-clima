import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClimaPronosticoComponent } from './clima-pronostico.component';

describe('ClimaPronosticoComponent', () => {
  let component: ClimaPronosticoComponent;
  let fixture: ComponentFixture<ClimaPronosticoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClimaPronosticoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ClimaPronosticoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
