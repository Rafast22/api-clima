import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GiantCardComponent } from './giant-card.component';

describe('GiantCardComponent', () => {
  let component: GiantCardComponent;
  let fixture: ComponentFixture<GiantCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GiantCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GiantCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
