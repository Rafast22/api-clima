import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Oauth2GoogleModalComponent } from './oauth2-google-modal.component';

describe('Oauth2GoogleModalComponent', () => {
  let component: Oauth2GoogleModalComponent;
  let fixture: ComponentFixture<Oauth2GoogleModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Oauth2GoogleModalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(Oauth2GoogleModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
