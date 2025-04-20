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
export class CalendarComponent implements OnChanges{
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

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['perfectDays']) {
      const valorAnterior = changes['perfectDays'].previousValue;
      const valorAtual = changes['perfectDays'].currentValue;

      if (valorAnterior !== valorAtual) {
        this.updateCalendar();
      }
    }
  }

  clickChangeMonth(offset: number): void {
      this.currentDate = new Date(this.currentDate.getFullYear(), (this.currentDate.getMonth() + offset), 1);
      this.updateCalendar();
      this.changeMonth.emit(this.currentDate);
  }


  public updateCalendar(): void {
      this.monthYear = this.currentDate.toLocaleString('es-ES', { month: 'long', year: 'numeric' });
    this.getDatesInMonth(this.currentDate)
      this.monthYear = this.monthYear[0].toUpperCase() + this.monthYear.slice(1);

  }

  getDatesInMonth(date: Date){
      const a = new Date();
      const firstDayindex = (new Date(date.getFullYear(), date.getMonth(), 1).getDay() + 6) % 7;
      const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
      const dates: DateCalendar[] = [];
      for (let i = 1; i <= lastDay.getDate(); i++) {
        const currentDate = new Date(date.getFullYear(), date.getMonth(), i);
        const isWeekend = currentDate.getDay() === 0 || currentDate.getDay() === 6; 
        const day:DateCalendar = {day:i.toString(), isWeekend:isWeekend, dayInfo:<PerfectDay>{Date:currentDate}}
        const perfectDay = this.perfectDays.filter(perfect => perfect.date.getTime() == day.dayInfo?.Date?.getTime())
        if(perfectDay.length > 0){
          day.dayInfo.Optimo = perfectDay[0].perfect;
        }
        if(`${a.getDate()}${a.getMonth()}${a.getFullYear()}` == `${day.dayInfo?.Date.getDate()}${day.dayInfo?.Date.getMonth()}${day.dayInfo?.Date.getFullYear()}`) day.dayInfo.Today = true
        
        dates.push(day);

      }

      for (let i = 0; i < firstDayindex; i++) {
        dates.unshift({ "day":"", dayInfo:<PerfectDay>{}}); 
      }
      this.calendarDates = [...dates];
  }
  
  selectDay = (date?:Date)=>{
    this.selectedDay.emit(date);
  }
}


interface DateCalendar{
  day:string; //Dia exibido no calendario
  isWeekend?: boolean; //se e final de semana
  dayInfo:PerfectDay; //objet
}
interface PerfectDay{
  Today:boolean;
  Optimo?:number;
  Date:Date;
}

