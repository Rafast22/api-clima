import { CommonModule } from '@angular/common';
import { Component, ElementRef, EventEmitter, input, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [CommonModule, MatIconModule],
  templateUrl: './calendar.component.html',
  styleUrl: './calendar.component.css'
})
export class CalendarComponent{
  @ViewChild('calendarContainer') calendarContainer: ElementRef | undefined = undefined;

  currentDate: Date = new Date();
  monthYear: string = '';
  calendarDates: DateCalendar[] = [];

  constructor() {
    this.perfectDays = [];

    this.updateCalendar();

  }

  @Output()
  selectedDay = new EventEmitter<Date>();
 
  @Input()
  public perfectDays: any[];

  @Input()
  public ListPerfectDays = (day:Date)=>{};

  changeMonth(offset: number): void {
      this.currentDate.setMonth(this.currentDate.getMonth() + offset);
      this.updateCalendar();
  }
  updateCalendarColors(){
    if(!this.calendarContainer) return;
    const container = this.calendarContainer.nativeElement;
    console.log(container)
    console.log(container.childs)
    // const cards = container.querySelector('.container');

  }
  updateCalendar(): void {
      this.monthYear = this.currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
      this.calendarDates = this.getDatesInMonth(this.currentDate);
      for (const day of this.calendarDates){
        for(const perfect of this.perfectDays){
          if(day.UTCDate.getTime() == perfect.getTime()){
            day.Style = {"background-color":"green"}
          }
        }
      }
  }

  getDatesInMonth(date: Date): DateCalendar[] {
      const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
      const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
      const dates: DateCalendar[] = [];

      for (let i = 1; i <= lastDay.getDate(); i++) {
        const currentDate = new Date(date.getFullYear(), date.getMonth(), i);
        const isWeekend = currentDate.getDay() === 0 || currentDate.getDay() === 6; 
        const newCalendarDate:DateCalendar = new DateCalendar(i, isWeekend, currentDate);
        
        dates.push({date:i, isWeekend:isWeekend, UTCDate:currentDate});
      }

      return dates;
  }
  selectDay(date:Date){

    this.selectedDay.emit(date);
  }
}


class DateCalendar{
  public date:number
  public isWeekend: boolean
  public UTCDate:Date;
  public Style?:any;
  constructor(date: number, isWeekend: boolean, D: Date){
    this.date = date;
    this.isWeekend = isWeekend;
    this.UTCDate = D;
  }
}