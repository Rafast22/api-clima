import { AfterViewInit, ChangeDetectionStrategy,Component, model } from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import {MAT_DATE_LOCALE, provideNativeDateAdapter} from '@angular/material/core';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { BreakpointObserver } from '@angular/cdk/layout';
import {MatSelectModule} from '@angular/material/select';
import { CalendarDatapickerRangeComponent } from '../calendar-datapicker-range/calendar-datapicker-range.component';
import Chart from 'chart.js/auto';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import {MatGridListModule} from '@angular/material/grid-list';


@Component({
  selector: 'app-recomendaciones-card',
  standalone: true,
  imports: [MatToolbarModule ,MatCardModule, MatDatepickerModule, MatSelectModule,MatGridListModule , MatFormFieldModule, MatInputModule,CalendarDatapickerRangeComponent, MatButtonModule],
  templateUrl: './recomendaciones-card.component.html',
  styleUrl: './recomendaciones-card.component.css',
  providers: [provideNativeDateAdapter(), {provide: MAT_DATE_LOCALE, useValue: 'es-PY'}],
  changeDetection: ChangeDetectionStrategy.OnPush,

})
export class RecomendacionesCardComponent implements AfterViewInit{
  chart: any = [];
  private chartDatasource:any[] = [];
  private chartLabels:any[] = [];
  get isMobile():boolean {
    return this.breakpointObserver.isMatched('(max-width: 767px)');
  }
  selected = model<Date | null>(null);  
  cultivos:any[] = [  
    {value:"maiz", description:"Maíz"},
    {value:"trigo", description:"Trigo"},
    {value:"arroz", description:"Arroz"}
  ];
  tipo:any[] = [ 
    {value:"cosecha", description:"Cosecha"},
    {value:"siembra", description:"Siembra"}
  ];

  ngAfterViewInit(): void {
    const ctx = document.getElementById('chart') as HTMLCanvasElement;
    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: this.chartLabels,
        datasets: this.chartDatasource
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
  constructor(private breakpointObserver: BreakpointObserver){

  }
  
  public cargarClick(){
    this.chartDatasource = [
      {
        label: 'Temperatura',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        borderColor: "red",
      },
      {
        label: 'Humedad',
        data: [10, 17, 7, 2, 15, 6],
        borderWidth: 1,
        borderColor: "blue",
        tension: 0.4,


      },
      {
        label: 'Precipitacion',
        data: [10, 17, 7, 2, 15, 6],
        borderWidth: 1,
        borderColor: "green",

      },
    ];
    this.chartLabels = ['00', '01', '02', '03', '04', '05', '06', '07', '08'];
    this.chart.data.datasets = [...this.chartDatasource]
    this.chart.data.labels = [...this.chartLabels]
    this.chart.update()
  }
}
