import { Component, model } from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import {MAT_DATE_LOCALE, provideNativeDateAdapter} from '@angular/material/core';
import {DateRange, DefaultMatCalendarRangeStrategy, MAT_DATE_RANGE_SELECTION_STRATEGY, MAT_RANGE_DATE_SELECTION_MODEL_PROVIDER, MatDatepickerModule} from '@angular/material/datepicker';
@Component({
  selector: 'calendar-datapicker-range',
  standalone: true,
  imports: [MatCardModule, MatDatepickerModule],
  // providers: [MAT_RANGE_DATE_SELECTION_MODEL_PROVIDER],
  providers:[{provide:MAT_DATE_RANGE_SELECTION_STRATEGY, useClass:DefaultMatCalendarRangeStrategy}, {provide: MAT_DATE_LOCALE, useValue: 'es-PY'}],
  templateUrl: './calendar-datapicker-range.component.html',
  styleUrl: './calendar-datapicker-range.component.css'
})
export class CalendarDatapickerRangeComponent {
selected=model<Date | null>(null);
sampleRange: DateRange<Date>
selectedDateRange: DateRange<Date|null> = new DateRange(null, null)
constructor(){

  this.sampleRange = new DateRange((() => {
    let v = new Date();
    v.setDate(v.getDate() - 7);
    return v;
  })(), new Date());

  }
  refreshDR() {
    
  }
  onChange(ev: any) {
    console.log(`cal onChange:`, ev);
  }
  _onSelectedChange(date:Date): void{
    if(this.selectedDateRange && this.selectedDateRange.start && date>this.selectedDateRange.start && !this.selectedDateRange.end){
      this.selectedDateRange = new DateRange(this.selectedDateRange.start, date)
    }
    else{
      this.selectedDateRange = new DateRange(date, null)
    }
  }
}
