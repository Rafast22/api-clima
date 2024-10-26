import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClimaCardComponent } from './clima-card.component';

describe('ClimaCardComponent', () => {
  let component: ClimaCardComponent;
  let fixture: ComponentFixture<ClimaCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClimaCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ClimaCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
