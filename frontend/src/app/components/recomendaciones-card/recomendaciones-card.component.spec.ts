import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecomendacionesCardComponent } from './recomendaciones-card.component';

describe('RecomendacionesCardComponent', () => {
  let component: RecomendacionesCardComponent;
  let fixture: ComponentFixture<RecomendacionesCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecomendacionesCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecomendacionesCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
