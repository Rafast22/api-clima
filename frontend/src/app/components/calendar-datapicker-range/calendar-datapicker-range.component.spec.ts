import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalendarDatapickerRangeComponent } from './calendar-datapicker-range.component';

describe('CalendarDatapickerRangeComponent', () => {
  let component: CalendarDatapickerRangeComponent;
  let fixture: ComponentFixture<CalendarDatapickerRangeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CalendarDatapickerRangeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CalendarDatapickerRangeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
