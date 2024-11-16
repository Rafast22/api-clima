import { AfterViewInit, ChangeDetectionStrategy, Component, ElementRef, model, ViewChild } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MAT_DATE_LOCALE, provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MatSelectModule } from '@angular/material/select';
import { CalendarDatapickerRangeComponent } from '../calendar-datapicker-range/calendar-datapicker-range.component';
import Chart from 'chart.js/auto';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatGridListModule } from '@angular/material/grid-list';
import { PredicService } from '../../services/predictions/predic.service';
import { CalendarComponent } from '../calendar/calendar.component';
import { ClimaCardComponent } from '../clima-card/clima-card.component';


@Component({
  selector: 'app-recomendaciones-card',
  standalone: true,
  imports: [MatToolbarModule, MatCardModule, MatDatepickerModule, MatSelectModule, MatGridListModule, MatFormFieldModule, MatInputModule, MatButtonModule, CalendarComponent, ClimaCardComponent],
  templateUrl: './recomendaciones-card.component.html',
  styleUrl: './recomendaciones-card.component.css',
  providers: [provideNativeDateAdapter(), { provide: MAT_DATE_LOCALE, useValue: 'es-PY' }],
  changeDetection: ChangeDetectionStrategy.OnPush,

})
export class RecomendacionesCardComponent implements AfterViewInit {
  @ViewChild('calendarComponent') calendarComponent: CalendarComponent | undefined = undefined;

  chart: any = [];
  perfectDays:any[] = []
  private chartDatasource: any = {};
  get isMobile(): boolean {
    return this.breakpointObserver.isMatched('(max-width: 767px)');
  }
  selected = model<Date | null>(null);
  cultivos: any[] = [
    { value: "maiz", description: "Maíz" },
    { value: "trigo", description: "Trigo" },
    { value: "arroz", description: "Arroz" }
  ];
  tipo: any[] = [
    { value: "cosecha", description: "Cosecha" },
    { value: "siembra", description: "Siembra" }
  ];

  ngAfterViewInit(): void {
    const ctx = document.getElementById('chart') as HTMLCanvasElement;
    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [],
        datasets: []
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
  constructor(private breakpointObserver: BreakpointObserver, private service: PredicService) {
    this.perfectDays = []
    const d:Date = new Date();
    const newDate = new Date(d.getFullYear(), d.getMonth(), d.getDate())
    this.perfectDays.push(newDate)
  }

  async _onChangeDate(e: any) {
    const day = e.toJSON().substring(0, 12)+"0:00:00";
    this.chartDatasource = await this.service.getPredictDataDay(0, day).then()
    this.changeChartInfo(day);
  }

  public perfect = (e:any) => {
    console.log(e)
  }

  private changeChartInfo(event:string) {
    const indexOf = this.chartDatasource["date"].find((r:string) => r == event.substring(0, 12)+"0:00:00") 
    const dayIndex = this.chartDatasource["date"].findIndex((ind:any) => ind == indexOf)
    const dayList = this.chartDatasource["date"].slice(dayIndex, dayIndex+25)
    const tempList = this.chartDatasource["t2m"].slice(dayIndex, dayIndex+24)
    const humList = this.chartDatasource["rh2m"].slice(dayIndex, dayIndex+24)
    const preList = this.chartDatasource["prectotcorr"].slice(dayIndex, dayIndex+24)
    const dataSources = [
      {
        label: 'Temperatura',
        data: tempList,
        borderWidth: 1,
        borderColor: "red",
        tension: 0.4,
      },
      {
        label: 'Humedad',
        data: humList,
        borderWidth: 1,
        borderColor: "blue",
        tension: 0.4,


      },
      {
        label: 'Precipitacion',
        data: preList,
        borderWidth: 1,
        borderColor: "green",
        tension: 0.4,

      },
    ];
    const labels = dayList.map((m: string) => {
      const d = new Date(m);
      return `${d.getHours() < 10 ? '0' + d.getHours() : d.getHours()}:${d.getMinutes() < 10 ? '0' + d.getMinutes() : d.getMinutes()}`;
    });
    this.chart.data.datasets = [...dataSources]
    this.chart.data.labels = [...labels]
    this.chart.update()
  }

  public async cargarClick() {
    // this.chartDatasource = await this.service.getPredictData(1).then();
    const d = new Date()
    const e = new Date(d.getFullYear(), d.getMonth(), d.getDate()+3)
    this.perfectDays.push(e)
    if(this.calendarComponent)
    this.calendarComponent.updateCalendar()
  }
}
