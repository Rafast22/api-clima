import { CommonModule } from '@angular/common';
import { Component, ElementRef, EventEmitter, input, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { DiaOptimoDirective } from './dia-optimo.directive';

@Component({
  selector: 'calendar',
  standalone: true,
  imports: [CommonModule, MatIconModule, DiaOptimoDirective],
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
  changeMonth = new EventEmitter<Date>();

  @Output()
  selectedDay = new EventEmitter<Date>();
 
  @Input()
  public perfectDays: any[];

  clickChangeMonth(offset: number): void {
      this.currentDate.setMonth(this.currentDate.getMonth() + offset);
      this.updateCalendar();
      this.changeMonth.emit(this.currentDate);
  }
  updateCalendarColors(){
    if(!this.calendarContainer) return;
    const container = this.calendarContainer.nativeElement;
    // const cards = container.querySelector('.container');

  }
  public updateCalendar(): void {
      this.monthYear = this.currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
      this.calendarDates = this.getDatesInMonth(this.currentDate);
      this.monthYear = this.monthYear[0].toUpperCase() + this.monthYear.slice(1)
      for (const day of this.calendarDates){
        if(day.Dia.UTCDate){ 
          const perfectDay = this.perfectDays.filter(d => d.getTime() == day.Dia.UTCDate?.getTime())
          if(perfectDay.length > 0){
            day.Dia.Optimo = true;
          }
          else
            day.Dia.Optimo = false;
        }      
        day.Dia.onClick = this.selectDay;

      }
  }

  getDatesInMonth(date: Date): DateCalendar[] {
      const a = new Date();
      const today = new Date(a.getFullYear(), a.getMonth(), a.getDate());
      const firstDayindex = (new Date(date.getFullYear(), date.getMonth(), 1).getDay() + 6) % 7;
      const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
      const dates: DateCalendar[] = [];

      for (let i = 1; i <= lastDay.getDate(); i++) {
        const currentDate = new Date(date.getFullYear(), date.getMonth(), i);
        const isWeekend = currentDate.getDay() === 0 || currentDate.getDay() === 6; 
        const d:DateCalendar = {date:i.toString(), isWeekend:isWeekend, Dia:<D>{UTCDate:currentDate}}
        if(d.Dia.UTCDate?.getTime() == today.getTime()) d.Dia.Today = true;
        dates.push(d);
      }

      for (let i = 0; i < firstDayindex; i++) {
        dates.unshift({ "date":"", Dia:<D>{}}); 
      }
      return dates;
  }
  
  selectDay = (date?:Date)=>{
    this.selectedDay.emit(date);
  }
}


class DateCalendar{
  public date:string
  public isWeekend?: boolean
  public Dia:D = <D>{}; 
  constructor(date: number, isWeekend: boolean, D: Date){
    this.date = date.toString();
    this.isWeekend = isWeekend;
  }
}
interface D{
  Optimo?:boolean;
  Today?:boolean;
  onClick?:any;
  UTCDate?:Date;
}

