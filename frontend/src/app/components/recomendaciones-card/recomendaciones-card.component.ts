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
import {MatExpansionModule} from '@angular/material/expansion';
import { FormControl, FormGroup } from '@angular/forms';


@Component({
  selector: 'app-recomendaciones-card',
  standalone: true,
  imports: [MatToolbarModule, MatCardModule, MatDatepickerModule,MatExpansionModule, MatSelectModule, MatGridListModule, MatFormFieldModule, MatInputModule, MatButtonModule, CalendarComponent, ClimaCardComponent],
  templateUrl: './recomendaciones-card.component.html',
  styleUrl: './recomendaciones-card.component.css',
  providers: [provideNativeDateAdapter(), { provide: MAT_DATE_LOCALE, useValue: 'es-PY' }],
  changeDetection: ChangeDetectionStrategy.OnPush,

})
export class RecomendacionesCardComponent implements AfterViewInit {
  @ViewChild('calendarComponent') calendarComponent: CalendarComponent | undefined = undefined;
  public predicciones:any=[];
  chart: any = [];
  perfectDays:any[] = []
  public chartDatasource: any = {};
  public diaSeleccionado: any;
  public hideHeader:boolean = false
  public _CardClimaOpen:boolean = true;
  public _CardDiasOptimos:boolean = false;
  public filtros:any={};

  public get _diaSelecionado():boolean{
    return (this.diaSeleccionado?false:true)
  }
  public get getCultivoSelecionado():string{
    if(this.filtros.cultivoSeleccionado)
      return this.cultivos.find(f => f.value==this.filtros.cultivoSeleccionado).description  
    else return ""

  }
  public get getTipoSelecionado():string{
    if(this.filtros.tipoActividadSeleccionado)
      return this.tipo.find(f => f.value==this.filtros.tipoActividadSeleccionado).description  
    else return ""
  }
  get isMobile(): boolean {
    return this.breakpointObserver.isMatched('(max-width: 767px)');
  }
  public get CardClimaOpen():boolean{
    return !this._CardDiasOptimos;
  }
  public set CardClimaOpen(v:boolean){
    this._CardClimaOpen = v;
  }
  public get CardDiasOptimos():boolean{
    return !this._CardClimaOpen;
  }
  public set CardDiasOptimos(v:boolean){
    this._CardDiasOptimos = v;
  }
  range = new FormGroup({
    start: new FormControl<Date | undefined>(undefined),
    end: new FormControl<Date | undefined>(undefined),
  });
  selected = model<Date | null>(null);
  cultivos: any[] = [
    { value: "1", description: "Maíz" },
    { value: "2", description: "Trigo" },
    { value: "3", description: "Soja" }
  ];
  tipo: any[] = [
    { value: "1", description: "Cosecha" },
    { value: "2", description: "Siembra" }
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
    this.predicciones=[
      {min:'20', max:"30", precip:0, precipMM:0},
      {min:'20', max:"30", precip:0, precipMM:0},
      {min:'20', max:"30", precip:0, precipMM:0},
      {min:'21', max:"30", precip:80, precipMM:1.7},
      {min:'20', max:"29", precip:90, precipMM:25},
      {min:'22', max:"30", precip:90, precipMM:4},
      {min:'21', max:"32", precip:80, precipMM:1.9},

      
    ]
  }

  async _onChangeDate(e: any) {
    this.diaSeleccionado = {}
    const day = e.toJSON().substring(0, 12)+"0:00:00";
    const day_str = day.split("T")[0].split("-").join("")
    // this.chartDatasource = await this.service.getPredictDataDay(0, day).then()
    const d = await this.preencherValores().then()
    this.chartDatasource = d.filter(a => a.date.split("T")[0].split("-").join("") == day_str)
    this.diaSeleccionado.Dia = e;
    this.diaSeleccionado.HumedadMedia = (this.chartDatasource.reduce((acumuladorH:number, humedad:any) => acumuladorH + humedad.rh2m, 0) / this.chartDatasource.length).toFixed(2);
    this.diaSeleccionado.PrecipitacionMedia = (this.chartDatasource.reduce((acumuladorP:number, precip:any) => acumuladorP + precip.prectotcorr, 0) / this.chartDatasource.length).toFixed(2);
    this.diaSeleccionado.TemperaturaMedia = (this.chartDatasource.reduce((acumuladorT:number, temperatura:any) => acumuladorT + temperatura.t2m, 0) / this.chartDatasource.length).toFixed(2);
    this.changeChartInfo(day);
  }

  public perfect = (e:any) => {
    console.log(e)
  }
  async prepareDataDeLoco(){
    const v:any = {};
    v["date"] = this.chartDatasource.map((a:any) => a.date);
    v["t2m"] = this.chartDatasource.map((a:any) => a.t2m);
    v["rh2m"] = this.chartDatasource.map((a:any) => a.rh2m);
    v["prectotcorr"] = this.chartDatasource.map((a:any) => a.prectotcorr);
    this.chartDatasource = v;
  }
  private async changeChartInfo(event:string) {
    await this.prepareDataDeLoco().then();
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
  _onSelectedChange(start:any, end:any){
    this.filtros.fecha_inicial = start.value.split('/').reverse().join('-');
    this.filtros.fecha_final = end.value.split('/').reverse().join('-');
  }

  protected async preencherValores(){
    const data = [
      {date:'2025-05-14T00:00:00' ,t2m: 11.01, rh2m:88.06 ,prectotcorr:0},
      {date:'2025-05-14T01:00:00' ,t2m: 10.51, rh2m:92.88 ,prectotcorr:0},
      {date:'2025-05-14T02:00:00' ,t2m: 9.98, rh2m:98.75 ,prectotcorr:0},
      {date:'2025-05-14T03:00:00' ,t2m: 9.46, rh2m:100 ,prectotcorr:0},
      {date:'2025-05-14T04:00:00' ,t2m: 9.05, rh2m:100 ,prectotcorr:0},
      {date:'2025-05-14T05:00:00' ,t2m: 8.74, rh2m:100 ,prectotcorr:0},
      {date:'2025-05-14T06:00:00' ,t2m: 9, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-14T07:00:00' ,t2m: 12.36, rh2m:93.31 ,prectotcorr:0 },
      {date:'2025-05-14T08:00:00' ,t2m: 15.12, rh2m:83.12 ,prectotcorr:0 },
      {date:'2025-05-14T09:00:00' ,t2m: 18.99, rh2m:62.25 ,prectotcorr:0 },
      {date:'2025-05-14T10:00:00' ,t2m: 21.47, rh2m:52.88 ,prectotcorr:0 },
      {date:'2025-05-14T11:00:00' ,t2m: 22.66, rh2m:50.75 ,prectotcorr:0 },
      {date:'2025-05-14T12:00:00' ,t2m: 23.25, rh2m:50.19 ,prectotcorr:0 },
      {date:'2025-05-14T13:00:00' ,t2m: 23.48, rh2m:50.12 ,prectotcorr:0 },
      {date:'2025-05-14T14:00:00' ,t2m: 23.36, rh2m:50.44 ,prectotcorr:0 },
      {date:'2025-05-14T15:00:00' ,t2m: 22.81, rh2m:54.19 ,prectotcorr:0 },
      {date:'2025-05-14T16:00:00' ,t2m: 21.31, rh2m:65 ,prectotcorr:0 },
      {date:'2025-05-14T17:00:00' ,t2m: 19.53, rh2m:62.12 ,prectotcorr:0 },
      {date:'2025-05-14T18:00:00' ,t2m: 18.19, rh2m:65.69 ,prectotcorr:0 },
      {date:'2025-05-14T19:00:00' ,t2m: 16.89, rh2m:70.44 ,prectotcorr:0 },
      {date:'2025-05-14T20:00:00' ,t2m: 15.74, rh2m:74.75 ,prectotcorr:0 },
      {date:'2025-05-14T21:00:00' ,t2m: 14.55, rh2m:80 ,prectotcorr:0 },
      {date:'2025-05-14T22:00:00' ,t2m: 13.6, rh2m:84.69 ,prectotcorr:0 },
      {date:'2025-05-14T23:00:00' ,t2m: 12.87, rh2m:89.38 ,prectotcorr:0 },
      {date:'2025-05-15T00:00:00' ,t2m: 12.26, rh2m:94.19 ,prectotcorr:0 },
      {date:'2025-05-15T01:00:00' ,t2m: 11.77, rh2m:98.12 ,prectotcorr:0 },
      {date:'2025-05-15T02:00:00' ,t2m: 11.35, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-15T03:00:00' ,t2m: 10.9, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-15T04:00:00' ,t2m: 10.44, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-15T05:00:00' ,t2m: 10.09, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-15T06:00:00' ,t2m: 10.22, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-15T07:00:00' ,t2m: 13.56, rh2m:91.81 ,prectotcorr:0 },
      {date:'2025-05-15T08:00:00' ,t2m: 16.22, rh2m:81.94 ,prectotcorr:0 },
      {date:'2025-05-15T09:00:00' ,t2m: 19.6, rh2m:68.75 ,prectotcorr:0 },
      {date:'2025-05-15T10:00:00' ,t2m: 22.25, rh2m:57.19 ,prectotcorr:0 },
      {date:'2025-05-15T11:00:00' ,t2m: 23.55, rh2m:54.12 ,prectotcorr:0 },
      {date:'2025-05-15T12:00:00' ,t2m: 24.2, rh2m:52.88 ,prectotcorr:0 },
      {date:'2025-05-15T13:00:00' ,t2m: 24.49, rh2m:52 ,prectotcorr:0 },
      {date:'2025-05-15T14:00:00' ,t2m: 24.41, rh2m:52.56 ,prectotcorr:0 },
      {date:'2025-05-15T15:00:00' ,t2m: 24.03, rh2m:55.31 ,prectotcorr:0 },
      {date:'2025-05-15T16:00:00' ,t2m: 22.33, rh2m:65.06 ,prectotcorr:0 },
      {date:'2025-05-15T17:00:00' ,t2m: 20.23, rh2m:64.38 ,prectotcorr:0 },
      {date:'2025-05-15T18:00:00' ,t2m: 19.09, rh2m:66.5 ,prectotcorr:0 },
      {date:'2025-05-15T19:00:00' ,t2m: 18.23, rh2m:69.06 ,prectotcorr:0 },
      {date:'2025-05-15T20:00:00' ,t2m: 17.34, rh2m:72.38 ,prectotcorr:0 },
      {date:'2025-05-15T21:00:00' ,t2m: 16.38, rh2m:76.62 ,prectotcorr:0 },
      {date:'2025-05-15T22:00:00' ,t2m: 15.26, rh2m:82.69 ,prectotcorr:0 },
      {date:'2025-05-15T23:00:00' ,t2m: 14.13, rh2m:89.81 ,prectotcorr:0 },
      {date:'2025-05-16T00:00:00' ,t2m: 13.28, rh2m:95.69 ,prectotcorr:0 },
      {date:'2025-05-16T01:00:00' ,t2m: 12.75, rh2m:99.69 ,prectotcorr:0 },
      {date:'2025-05-16T02:00:00' ,t2m: 12.29, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-16T03:00:00' ,t2m: 11.87, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-16T04:00:00' ,t2m: 11.45, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-16T05:00:00' ,t2m: 11.19, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-16T06:00:00' ,t2m: 11.32, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-16T07:00:00' ,t2m: 14.18, rh2m:93.88 ,prectotcorr:0 },
      {date:'2025-05-16T08:00:00' ,t2m: 16.82, rh2m:83.38 ,prectotcorr:0 },
      {date:'2025-05-16T09:00:00' ,t2m: 20.04, rh2m:68.56 ,prectotcorr:0 },
      {date:'2025-05-16T10:00:00' ,t2m: 22.62, rh2m:58.5 ,prectotcorr:0 },
      {date:'2025-05-16T11:00:00' ,t2m: 24.23, rh2m:52.62 ,prectotcorr:0 },
      {date:'2025-05-16T12:00:00' ,t2m: 24.83, rh2m:50.94 ,prectotcorr:0 },
      {date:'2025-05-16T13:00:00' ,t2m: 25, rh2m:50.44 ,prectotcorr:0 },
      {date:'2025-05-16T14:00:00' ,t2m: 24.83, rh2m:51.25 ,prectotcorr:0 },
      {date:'2025-05-16T15:00:00' ,t2m: 24.37, rh2m:54.06 ,prectotcorr:0 },
      {date:'2025-05-16T16:00:00' ,t2m: 22.25, rh2m:66.62 ,prectotcorr:0 },
      {date:'2025-05-16T17:00:00' ,t2m: 19.58, rh2m:68.56 ,prectotcorr:0 },
      {date:'2025-05-16T18:00:00' ,t2m: 17.96, rh2m:72.75 ,prectotcorr:0 },
      {date:'2025-05-16T19:00:00' ,t2m: 16.73, rh2m:76.69 ,prectotcorr:0 },
      {date:'2025-05-16T20:00:00' ,t2m: 15.8, rh2m:79.69 ,prectotcorr:0 },
      {date:'2025-05-16T21:00:00' ,t2m: 15.26, rh2m:81.5 ,prectotcorr:0 },
      {date:'2025-05-16T22:00:00' ,t2m: 14.69, rh2m:84.12 ,prectotcorr:0 },
      {date:'2025-05-16T23:00:00' ,t2m: 14.03, rh2m:88.5 ,prectotcorr:0 },
      {date:'2025-05-17T00:00:00' ,t2m: 13.4, rh2m:93.56 ,prectotcorr:0 },
      {date:'2025-05-17T01:00:00' ,t2m: 12.88, rh2m:98.69 ,prectotcorr:0 },
      {date:'2025-05-17T02:00:00' ,t2m: 12.3, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-17T03:00:00' ,t2m: 11.65, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-17T04:00:00' ,t2m: 11.19, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-17T05:00:00' ,t2m: 10.92, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-17T06:00:00' ,t2m: 11.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-17T07:00:00' ,t2m: 14.29, rh2m:91.5 ,prectotcorr:0 },
      {date:'2025-05-17T08:00:00' ,t2m: 17.07, rh2m:78.38 ,prectotcorr:0 },
      {date:'2025-05-17T09:00:00' ,t2m: 19.89, rh2m:67 ,prectotcorr:0 },
      {date:'2025-05-17T10:00:00' ,t2m: 21.91, rh2m:60.62 ,prectotcorr:0 },
      {date:'2025-05-17T11:00:00' ,t2m: 23.15, rh2m:57.25 ,prectotcorr:0 },
      {date:'2025-05-17T12:00:00' ,t2m: 23.87, rh2m:55.81 ,prectotcorr:0 },
      {date:'2025-05-17T13:00:00' ,t2m: 24.19, rh2m:55.56 ,prectotcorr:0 },
      {date:'2025-05-17T14:00:00' ,t2m: 24.2, rh2m:56.38 ,prectotcorr:0 },
      {date:'2025-05-17T15:00:00' ,t2m: 23.65, rh2m:60.94 ,prectotcorr:0 },
      {date:'2025-05-17T16:00:00' ,t2m: 21.43, rh2m:73.44 ,prectotcorr:0 },
      {date:'2025-05-17T17:00:00' ,t2m: 18.75, rh2m:75.94 ,prectotcorr:0 },
      {date:'2025-05-17T18:00:00' ,t2m: 17.44, rh2m:79.81 ,prectotcorr:0 },
      {date:'2025-05-17T19:00:00' ,t2m: 16.76, rh2m:81.31 ,prectotcorr:0 },
      {date:'2025-05-17T20:00:00' ,t2m: 16.3, rh2m:82.69 ,prectotcorr:0 },
      {date:'2025-05-17T21:00:00' ,t2m: 15.78, rh2m:85.5 ,prectotcorr:0 },
      {date:'2025-05-17T22:00:00' ,t2m: 15.18, rh2m:89.69 ,prectotcorr:0 },
      {date:'2025-05-17T23:00:00' ,t2m: 14.44, rh2m:95 ,prectotcorr:0 },
      {date:'2025-05-18T00:00:00' ,t2m: 13.62, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-18T01:00:00' ,t2m: 12.95, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-18T02:00:00' ,t2m: 12.43, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-18T03:00:00' ,t2m: 12.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-18T04:00:00' ,t2m: 11.69, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-18T05:00:00' ,t2m: 11.26, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-18T06:00:00' ,t2m: 11.45, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-18T07:00:00' ,t2m: 14.79, rh2m:92.38 ,prectotcorr:0 },
      {date:'2025-05-18T08:00:00' ,t2m: 17.51, rh2m:76.94 ,prectotcorr:0 },
      {date:'2025-05-18T09:00:00' ,t2m: 20.01, rh2m:67.19 ,prectotcorr:0 },
      {date:'2025-05-18T10:00:00' ,t2m: 21.98, rh2m:61.5 ,prectotcorr:0 },
      {date:'2025-05-18T11:00:00' ,t2m: 23.38, rh2m:57.88 ,prectotcorr:0 },
      {date:'2025-05-18T12:00:00' ,t2m: 24.16, rh2m:56.5 ,prectotcorr:0 },
      {date:'2025-05-18T13:00:00' ,t2m: 24.49, rh2m:55.75 ,prectotcorr:0 },
      {date:'2025-05-18T14:00:00' ,t2m: 24.37, rh2m:56.12 ,prectotcorr:0 },
      {date:'2025-05-18T15:00:00' ,t2m: 23.83, rh2m:59.12 ,prectotcorr:0 },
      {date:'2025-05-18T16:00:00' ,t2m: 21.87, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-18T17:00:00' ,t2m: 19.72, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-18T18:00:00' ,t2m: 18.65, rh2m:71.88 ,prectotcorr:0 },
      {date:'2025-05-18T19:00:00' ,t2m: 17.74, rh2m:74.62 ,prectotcorr:0 },
      {date:'2025-05-18T20:00:00' ,t2m: 16.94, rh2m:77.81 ,prectotcorr:0 },
      {date:'2025-05-18T21:00:00' ,t2m: 16.18, rh2m:82 ,prectotcorr:0 },
      {date:'2025-05-18T22:00:00' ,t2m: 15.33, rh2m:88.06 ,prectotcorr:0 },
      {date:'2025-05-18T23:00:00' ,t2m: 14.47, rh2m:94.62 ,prectotcorr:0 },
      {date:'2025-05-19T00:00:00' ,t2m: 13.4, rh2m:93.56 ,prectotcorr:0 },
      {date:'2025-05-19T01:00:00' ,t2m: 12.88, rh2m:98.69 ,prectotcorr:0 },
      {date:'2025-05-19T02:00:00' ,t2m: 12.3, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-19T03:00:00' ,t2m: 11.65, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-19T04:00:00' ,t2m: 11.19, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-19T05:00:00' ,t2m: 10.92, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-19T06:00:00' ,t2m: 11.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-19T07:00:00' ,t2m: 14.29, rh2m:91.5 ,prectotcorr:0 },
      {date:'2025-05-19T08:00:00' ,t2m: 17.07, rh2m:78.38 ,prectotcorr:0 },
      {date:'2025-05-19T09:00:00' ,t2m: 19.89, rh2m:67 ,prectotcorr:0 },
      {date:'2025-05-19T10:00:00' ,t2m: 21.91, rh2m:60.62 ,prectotcorr:0 },
      {date:'2025-05-19T11:00:00' ,t2m: 23.15, rh2m:57.25 ,prectotcorr:0 },
      {date:'2025-05-19T12:00:00' ,t2m: 23.87, rh2m:55.81 ,prectotcorr:0 },
      {date:'2025-05-19T13:00:00' ,t2m: 24.19, rh2m:55.56 ,prectotcorr:0 },
      {date:'2025-05-19T14:00:00' ,t2m: 24.2, rh2m:56.38 ,prectotcorr:0 },
      {date:'2025-05-19T15:00:00' ,t2m: 23.65, rh2m:60.94 ,prectotcorr:0 },
      {date:'2025-05-19T16:00:00' ,t2m: 21.43, rh2m:73.44 ,prectotcorr:0 },
      {date:'2025-05-19T17:00:00' ,t2m: 18.75, rh2m:75.94 ,prectotcorr:0 },
      {date:'2025-05-19T18:00:00' ,t2m: 17.44, rh2m:79.81 ,prectotcorr:0 },
      {date:'2025-05-19T19:00:00' ,t2m: 16.76, rh2m:81.31 ,prectotcorr:0 },
      {date:'2025-05-19T20:00:00' ,t2m: 16.3, rh2m:82.69 ,prectotcorr:0 },
      {date:'2025-05-19T21:00:00' ,t2m: 15.78, rh2m:85.5 ,prectotcorr:0 },
      {date:'2025-05-19T22:00:00' ,t2m: 15.18, rh2m:89.69 ,prectotcorr:0 },
      {date:'2025-05-19T23:00:00' ,t2m: 14.44, rh2m:95 ,prectotcorr:0 },
      {date:'2025-05-20T00:00:00' ,t2m: 13.62, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-20T01:00:00' ,t2m: 12.95, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-20T02:00:00' ,t2m: 12.43, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-20T03:00:00' ,t2m: 12.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-20T04:00:00' ,t2m: 11.69, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-20T05:00:00' ,t2m: 11.26, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-20T06:00:00' ,t2m: 11.45, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-20T07:00:00' ,t2m: 14.79, rh2m:92.38 ,prectotcorr:0 },
      {date:'2025-05-20T08:00:00' ,t2m: 17.51, rh2m:76.94 ,prectotcorr:0 },
      {date:'2025-05-20T09:00:00' ,t2m: 20.01, rh2m:67.19 ,prectotcorr:0 },
      {date:'2025-05-20T10:00:00' ,t2m: 21.98, rh2m:61.5 ,prectotcorr:0 },
      {date:'2025-05-20T11:00:00' ,t2m: 23.38, rh2m:57.88 ,prectotcorr:0 },
      {date:'2025-05-20T12:00:00' ,t2m: 24.16, rh2m:56.5 ,prectotcorr:0 },
      {date:'2025-05-20T13:00:00' ,t2m: 24.49, rh2m:55.75 ,prectotcorr:0 },
      {date:'2025-05-20T14:00:00' ,t2m: 24.37, rh2m:56.12 ,prectotcorr:0 },
      {date:'2025-05-20T15:00:00' ,t2m: 23.83, rh2m:59.12 ,prectotcorr:0 },
      {date:'2025-05-20T16:00:00' ,t2m: 21.87, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-20T17:00:00' ,t2m: 19.72, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-20T18:00:00' ,t2m: 18.65, rh2m:71.88 ,prectotcorr:0 },
      {date:'2025-05-20T19:00:00' ,t2m: 17.74, rh2m:74.62 ,prectotcorr:0 },
      {date:'2025-05-20T20:00:00' ,t2m: 16.94, rh2m:77.81 ,prectotcorr:0 },
      {date:'2025-05-20T21:00:00' ,t2m: 16.18, rh2m:82 ,prectotcorr:0 },
      {date:'2025-05-20T22:00:00' ,t2m: 15.33, rh2m:88.06 ,prectotcorr:0 },
      {date:'2025-05-20T23:00:00' ,t2m: 14.47, rh2m:94.62 ,prectotcorr:0 },
      {date:'2025-05-21T00:00:00' ,t2m: 13.4, rh2m:93.56 ,prectotcorr:0 },
      {date:'2025-05-21T01:00:00' ,t2m: 12.88, rh2m:98.69 ,prectotcorr:0 },
      {date:'2025-05-21T02:00:00' ,t2m: 12.3, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-21T03:00:00' ,t2m: 11.65, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-21T04:00:00' ,t2m: 11.19, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-21T05:00:00' ,t2m: 10.92, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-21T06:00:00' ,t2m: 11.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-21T07:00:00' ,t2m: 14.29, rh2m:91.5 ,prectotcorr:0 },
      {date:'2025-05-21T08:00:00' ,t2m: 17.07, rh2m:78.38 ,prectotcorr:0 },
      {date:'2025-05-21T09:00:00' ,t2m: 19.89, rh2m:67 ,prectotcorr:0 },
      {date:'2025-05-21T10:00:00' ,t2m: 21.91, rh2m:60.62 ,prectotcorr:0 },
      {date:'2025-05-21T11:00:00' ,t2m: 23.15, rh2m:57.25 ,prectotcorr:0 },
      {date:'2025-05-21T12:00:00' ,t2m: 23.87, rh2m:55.81 ,prectotcorr:0 },
      {date:'2025-05-21T13:00:00' ,t2m: 24.19, rh2m:55.56 ,prectotcorr:0 },
      {date:'2025-05-21T14:00:00' ,t2m: 24.2, rh2m:56.38 ,prectotcorr:0 },
      {date:'2025-05-21T15:00:00' ,t2m: 23.65, rh2m:60.94 ,prectotcorr:0 },
      {date:'2025-05-21T16:00:00' ,t2m: 21.43, rh2m:73.44 ,prectotcorr:0 },
      {date:'2025-05-21T17:00:00' ,t2m: 18.75, rh2m:75.94 ,prectotcorr:0 },
      {date:'2025-05-21T18:00:00' ,t2m: 17.44, rh2m:79.81 ,prectotcorr:0 },
      {date:'2025-05-21T19:00:00' ,t2m: 16.76, rh2m:81.31 ,prectotcorr:0 },
      {date:'2025-05-21T20:00:00' ,t2m: 16.3, rh2m:82.69 ,prectotcorr:0 },
      {date:'2025-05-21T21:00:00' ,t2m: 15.78, rh2m:85.5 ,prectotcorr:0 },
      {date:'2025-05-21T22:00:00' ,t2m: 15.18, rh2m:89.69 ,prectotcorr:0 },
      {date:'2025-05-21T23:00:00' ,t2m: 14.44, rh2m:95 ,prectotcorr:0 },
      {date:'2025-05-22T00:00:00' ,t2m: 13.62, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-22T01:00:00' ,t2m: 12.95, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-22T02:00:00' ,t2m: 12.43, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-22T03:00:00' ,t2m: 12.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-22T04:00:00' ,t2m: 11.69, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-22T05:00:00' ,t2m: 11.26, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-22T06:00:00' ,t2m: 11.45, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-22T07:00:00' ,t2m: 14.79, rh2m:92.38 ,prectotcorr:0 },
      {date:'2025-05-22T08:00:00' ,t2m: 17.51, rh2m:76.94 ,prectotcorr:0 },
      {date:'2025-05-22T09:00:00' ,t2m: 20.01, rh2m:67.19 ,prectotcorr:0 },
      {date:'2025-05-22T10:00:00' ,t2m: 21.98, rh2m:61.5 ,prectotcorr:0 },
      {date:'2025-05-22T11:00:00' ,t2m: 23.38, rh2m:57.88 ,prectotcorr:0 },
      {date:'2025-05-22T12:00:00' ,t2m: 24.16, rh2m:56.5 ,prectotcorr:0 },
      {date:'2025-05-22T13:00:00' ,t2m: 24.49, rh2m:55.75 ,prectotcorr:0 },
      {date:'2025-05-22T14:00:00' ,t2m: 24.37, rh2m:56.12 ,prectotcorr:0 },
      {date:'2025-05-22T15:00:00' ,t2m: 23.83, rh2m:59.12 ,prectotcorr:0 },
      {date:'2025-05-22T16:00:00' ,t2m: 21.87, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-22T17:00:00' ,t2m: 19.72, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-22T18:00:00' ,t2m: 18.65, rh2m:71.88 ,prectotcorr:0 },
      {date:'2025-05-22T19:00:00' ,t2m: 17.74, rh2m:74.62 ,prectotcorr:0 },
      {date:'2025-05-22T20:00:00' ,t2m: 16.94, rh2m:77.81 ,prectotcorr:0 },
      {date:'2025-05-22T21:00:00' ,t2m: 16.18, rh2m:82 ,prectotcorr:0 },
      {date:'2025-05-22T22:00:00' ,t2m: 15.33, rh2m:88.06 ,prectotcorr:0 },
      {date:'2025-05-22T23:00:00' ,t2m: 14.47, rh2m:94.62 ,prectotcorr:0 },
      {date:'2025-05-23T00:00:00' ,t2m: 13.4, rh2m:93.56 ,prectotcorr:0 },
      {date:'2025-05-23T01:00:00' ,t2m: 12.88, rh2m:98.69 ,prectotcorr:0 },
      {date:'2025-05-23T02:00:00' ,t2m: 12.3, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-23T03:00:00' ,t2m: 11.65, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-23T04:00:00' ,t2m: 11.19, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-23T05:00:00' ,t2m: 10.92, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-23T06:00:00' ,t2m: 11.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-23T07:00:00' ,t2m: 14.29, rh2m:91.5 ,prectotcorr:0 },
      {date:'2025-05-23T08:00:00' ,t2m: 17.07, rh2m:78.38 ,prectotcorr:0 },
      {date:'2025-05-23T09:00:00' ,t2m: 19.89, rh2m:67 ,prectotcorr:0 },
      {date:'2025-05-23T10:00:00' ,t2m: 21.91, rh2m:60.62 ,prectotcorr:0 },
      {date:'2025-05-23T11:00:00' ,t2m: 23.15, rh2m:57.25 ,prectotcorr:0 },
      {date:'2025-05-23T12:00:00' ,t2m: 23.87, rh2m:55.81 ,prectotcorr:0 },
      {date:'2025-05-23T13:00:00' ,t2m: 24.19, rh2m:55.56 ,prectotcorr:0 },
      {date:'2025-05-23T14:00:00' ,t2m: 24.2, rh2m:56.38 ,prectotcorr:0 },
      {date:'2025-05-23T15:00:00' ,t2m: 23.65, rh2m:60.94 ,prectotcorr:0 },
      {date:'2025-05-23T16:00:00' ,t2m: 21.43, rh2m:73.44 ,prectotcorr:0 },
      {date:'2025-05-23T17:00:00' ,t2m: 18.75, rh2m:75.94 ,prectotcorr:0 },
      {date:'2025-05-23T18:00:00' ,t2m: 17.44, rh2m:79.81 ,prectotcorr:0 },
      {date:'2025-05-23T19:00:00' ,t2m: 16.76, rh2m:81.31 ,prectotcorr:0 },
      {date:'2025-05-23T20:00:00' ,t2m: 16.3, rh2m:82.69 ,prectotcorr:0 },
      {date:'2025-05-23T21:00:00' ,t2m: 15.78, rh2m:85.5 ,prectotcorr:0 },
      {date:'2025-05-23T22:00:00' ,t2m: 15.18, rh2m:89.69 ,prectotcorr:0 },
      {date:'2025-05-23T23:00:00' ,t2m: 14.44, rh2m:95 ,prectotcorr:0 },
      {date:'2025-05-24T00:00:00' ,t2m: 13.62, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-24T01:00:00' ,t2m: 12.95, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-24T02:00:00' ,t2m: 12.43, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-24T03:00:00' ,t2m: 12.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-24T04:00:00' ,t2m: 11.69, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-24T05:00:00' ,t2m: 11.26, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-24T06:00:00' ,t2m: 11.45, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-24T07:00:00' ,t2m: 14.79, rh2m:92.38 ,prectotcorr:0 },
      {date:'2025-05-24T08:00:00' ,t2m: 17.51, rh2m:76.94 ,prectotcorr:0 },
      {date:'2025-05-24T09:00:00' ,t2m: 20.01, rh2m:67.19 ,prectotcorr:0 },
      {date:'2025-05-24T10:00:00' ,t2m: 21.98, rh2m:61.5 ,prectotcorr:0 },
      {date:'2025-05-24T11:00:00' ,t2m: 23.38, rh2m:57.88 ,prectotcorr:0 },
      {date:'2025-05-24T12:00:00' ,t2m: 24.16, rh2m:56.5 ,prectotcorr:0 },
      {date:'2025-05-24T13:00:00' ,t2m: 24.49, rh2m:55.75 ,prectotcorr:0 },
      {date:'2025-05-24T14:00:00' ,t2m: 24.37, rh2m:56.12 ,prectotcorr:0 },
      {date:'2025-05-24T15:00:00' ,t2m: 23.83, rh2m:59.12 ,prectotcorr:0 },
      {date:'2025-05-24T16:00:00' ,t2m: 21.87, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-24T17:00:00' ,t2m: 19.72, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-24T18:00:00' ,t2m: 18.65, rh2m:71.88 ,prectotcorr:0 },
      {date:'2025-05-24T19:00:00' ,t2m: 17.74, rh2m:74.62 ,prectotcorr:0 },
      {date:'2025-05-24T20:00:00' ,t2m: 16.94, rh2m:77.81 ,prectotcorr:0 },
      {date:'2025-05-24T21:00:00' ,t2m: 16.18, rh2m:82 ,prectotcorr:0 },
      {date:'2025-05-24T22:00:00' ,t2m: 15.33, rh2m:88.06 ,prectotcorr:0 },
      {date:'2025-05-24T23:00:00' ,t2m: 14.47, rh2m:94.62 ,prectotcorr:0 },
      {date:'2025-05-25T00:00:00' ,t2m: 13.4, rh2m:93.56 ,prectotcorr:0 },
      {date:'2025-05-25T01:00:00' ,t2m: 12.88, rh2m:98.69 ,prectotcorr:0 },
      {date:'2025-05-25T02:00:00' ,t2m: 12.3, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-25T03:00:00' ,t2m: 11.65, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-25T04:00:00' ,t2m: 11.19, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-25T05:00:00' ,t2m: 10.92, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-25T06:00:00' ,t2m: 11.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-25T07:00:00' ,t2m: 14.29, rh2m:91.5 ,prectotcorr:0 },
      {date:'2025-05-25T08:00:00' ,t2m: 17.07, rh2m:78.38 ,prectotcorr:0 },
      {date:'2025-05-25T09:00:00' ,t2m: 19.89, rh2m:67 ,prectotcorr:0 },
      {date:'2025-05-25T10:00:00' ,t2m: 21.91, rh2m:60.62 ,prectotcorr:0 },
      {date:'2025-05-25T11:00:00' ,t2m: 23.15, rh2m:57.25 ,prectotcorr:0 },
      {date:'2025-05-25T12:00:00' ,t2m: 23.87, rh2m:55.81 ,prectotcorr:0 },
      {date:'2025-05-25T13:00:00' ,t2m: 24.19, rh2m:55.56 ,prectotcorr:0 },
      {date:'2025-05-25T14:00:00' ,t2m: 24.2, rh2m:56.38 ,prectotcorr:0 },
      {date:'2025-05-25T15:00:00' ,t2m: 23.65, rh2m:60.94 ,prectotcorr:0 },
      {date:'2025-05-25T16:00:00' ,t2m: 21.43, rh2m:73.44 ,prectotcorr:0 },
      {date:'2025-05-25T17:00:00' ,t2m: 18.75, rh2m:75.94 ,prectotcorr:0 },
      {date:'2025-05-25T18:00:00' ,t2m: 17.44, rh2m:79.81 ,prectotcorr:0 },
      {date:'2025-05-25T19:00:00' ,t2m: 16.76, rh2m:81.31 ,prectotcorr:0 },
      {date:'2025-05-25T20:00:00' ,t2m: 16.3, rh2m:82.69 ,prectotcorr:0 },
      {date:'2025-05-25T21:00:00' ,t2m: 15.78, rh2m:85.5 ,prectotcorr:0 },
      {date:'2025-05-25T22:00:00' ,t2m: 15.18, rh2m:89.69 ,prectotcorr:0 },
      {date:'2025-05-25T23:00:00' ,t2m: 14.44, rh2m:95 ,prectotcorr:0 },
      {date:'2025-05-26T00:00:00' ,t2m: 13.62, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-26T01:00:00' ,t2m: 12.95, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-26T02:00:00' ,t2m: 12.43, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-26T03:00:00' ,t2m: 12.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-26T04:00:00' ,t2m: 11.69, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-26T05:00:00' ,t2m: 11.26, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-26T06:00:00' ,t2m: 11.45, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-26T07:00:00' ,t2m: 14.79, rh2m:92.38 ,prectotcorr:0 },
      {date:'2025-05-26T08:00:00' ,t2m: 17.51, rh2m:76.94 ,prectotcorr:0 },
      {date:'2025-05-26T09:00:00' ,t2m: 20.01, rh2m:67.19 ,prectotcorr:0 },
      {date:'2025-05-26T10:00:00' ,t2m: 21.98, rh2m:61.5 ,prectotcorr:0 },
      {date:'2025-05-26T11:00:00' ,t2m: 23.38, rh2m:57.88 ,prectotcorr:0 },
      {date:'2025-05-26T12:00:00' ,t2m: 24.16, rh2m:56.5 ,prectotcorr:0 },
      {date:'2025-05-26T13:00:00' ,t2m: 24.49, rh2m:55.75 ,prectotcorr:0 },
      {date:'2025-05-26T14:00:00' ,t2m: 24.37, rh2m:56.12 ,prectotcorr:0 },
      {date:'2025-05-26T15:00:00' ,t2m: 23.83, rh2m:59.12 ,prectotcorr:0 },
      {date:'2025-05-26T16:00:00' ,t2m: 21.87, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-26T17:00:00' ,t2m: 19.72, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-26T18:00:00' ,t2m: 18.65, rh2m:71.88 ,prectotcorr:0 },
      {date:'2025-05-26T19:00:00' ,t2m: 17.74, rh2m:74.62 ,prectotcorr:0 },
      {date:'2025-05-26T20:00:00' ,t2m: 16.94, rh2m:77.81 ,prectotcorr:0 },
      {date:'2025-05-26T21:00:00' ,t2m: 16.18, rh2m:82 ,prectotcorr:0 },
      {date:'2025-05-26T22:00:00' ,t2m: 15.33, rh2m:88.06 ,prectotcorr:0 },
      {date:'2025-05-26T23:00:00' ,t2m: 14.47, rh2m:94.62 ,prectotcorr:0 },
      {date:'2025-05-27T00:00:00' ,t2m: 13.4, rh2m:93.56 ,prectotcorr:0 },
      {date:'2025-05-27T01:00:00' ,t2m: 12.88, rh2m:98.69 ,prectotcorr:0 },
      {date:'2025-05-27T02:00:00' ,t2m: 12.3, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-27T03:00:00' ,t2m: 11.65, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-27T04:00:00' ,t2m: 11.19, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-27T05:00:00' ,t2m: 10.92, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-27T06:00:00' ,t2m: 11.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-27T07:00:00' ,t2m: 14.29, rh2m:91.5 ,prectotcorr:0 },
      {date:'2025-05-27T08:00:00' ,t2m: 17.07, rh2m:78.38 ,prectotcorr:0 },
      {date:'2025-05-27T09:00:00' ,t2m: 19.89, rh2m:67 ,prectotcorr:0 },
      {date:'2025-05-27T10:00:00' ,t2m: 21.91, rh2m:60.62 ,prectotcorr:0 },
      {date:'2025-05-27T11:00:00' ,t2m: 23.15, rh2m:57.25 ,prectotcorr:0 },
      {date:'2025-05-27T12:00:00' ,t2m: 23.87, rh2m:55.81 ,prectotcorr:0 },
      {date:'2025-05-27T13:00:00' ,t2m: 24.19, rh2m:55.56 ,prectotcorr:0 },
      {date:'2025-05-27T14:00:00' ,t2m: 24.2, rh2m:56.38 ,prectotcorr:0 },
      {date:'2025-05-27T15:00:00' ,t2m: 23.65, rh2m:60.94 ,prectotcorr:0 },
      {date:'2025-05-27T16:00:00' ,t2m: 21.43, rh2m:73.44 ,prectotcorr:0 },
      {date:'2025-05-27T17:00:00' ,t2m: 18.75, rh2m:75.94 ,prectotcorr:0 },
      {date:'2025-05-27T18:00:00' ,t2m: 17.44, rh2m:79.81 ,prectotcorr:0 },
      {date:'2025-05-27T19:00:00' ,t2m: 16.76, rh2m:81.31 ,prectotcorr:0 },
      {date:'2025-05-27T20:00:00' ,t2m: 16.3, rh2m:82.69 ,prectotcorr:0 },
      {date:'2025-05-27T21:00:00' ,t2m: 15.78, rh2m:85.5 ,prectotcorr:0 },
      {date:'2025-05-27T22:00:00' ,t2m: 15.18, rh2m:89.69 ,prectotcorr:0 },
      {date:'2025-05-27T23:00:00' ,t2m: 14.44, rh2m:95 ,prectotcorr:0 },
      {date:'2025-05-28T00:00:00' ,t2m: 13.62, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-28T01:00:00' ,t2m: 12.95, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-28T02:00:00' ,t2m: 12.43, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-28T03:00:00' ,t2m: 12.01, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-28T04:00:00' ,t2m: 11.69, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-28T05:00:00' ,t2m: 11.26, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-28T06:00:00' ,t2m: 11.45, rh2m:100 ,prectotcorr:0 },
      {date:'2025-05-28T07:00:00' ,t2m: 14.79, rh2m:92.38 ,prectotcorr:0 },
      {date:'2025-05-28T08:00:00' ,t2m: 17.51, rh2m:76.94 ,prectotcorr:0 },
      {date:'2025-05-28T09:00:00' ,t2m: 20.01, rh2m:67.19 ,prectotcorr:0 },
      {date:'2025-05-28T10:00:00' ,t2m: 21.98, rh2m:61.5 ,prectotcorr:0 },
      {date:'2025-05-28T11:00:00' ,t2m: 23.38, rh2m:57.88 ,prectotcorr:0 },
      {date:'2025-05-28T12:00:00' ,t2m: 24.16, rh2m:56.5 ,prectotcorr:0 },
      {date:'2025-05-28T13:00:00' ,t2m: 24.49, rh2m:55.75 ,prectotcorr:0 },
      {date:'2025-05-28T14:00:00' ,t2m: 24.37, rh2m:56.12 ,prectotcorr:0 },
      {date:'2025-05-28T15:00:00' ,t2m: 23.83, rh2m:59.12 ,prectotcorr:0 },
      {date:'2025-05-28T16:00:00' ,t2m: 21.87, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-28T17:00:00' ,t2m: 19.72, rh2m:69.75 ,prectotcorr:0 },
      {date:'2025-05-28T18:00:00' ,t2m: 18.65, rh2m:71.88 ,prectotcorr:0 },
      {date:'2025-05-28T19:00:00' ,t2m: 17.74, rh2m:74.62 ,prectotcorr:0 },
      {date:'2025-05-28T20:00:00' ,t2m: 16.94, rh2m:77.81 ,prectotcorr:0 },
      {date:'2025-05-28T21:00:00' ,t2m: 16.18, rh2m:82 ,prectotcorr:0 },
      {date:'2025-05-28T22:00:00' ,t2m: 15.33, rh2m:88.06 ,prectotcorr:0 },
      {date:'2025-05-28T23:00:00' ,t2m: 14.47, rh2m:94.62 ,prectotcorr:0 },
    ]
    return data
  }
  private stringToDate(dateString: string): Date {
    const d = dateString.split("T")[0].split("-").join("") 
    const year = parseInt(d.substring(0, 4));
    const month = parseInt(d.substring(4, 6)) - 1;
    const day = parseInt(d.substring(6, 8));
    // const hours = parseInt(dateString.substring(8, 10));
  
    return new Date(year, month, day);
  }

  public async prepararDados(){
    const d = new Date()
    const e = new Date(d.getFullYear(), d.getMonth(), d.getDate()+3)
    const values = await this.preencherValores().then()
    // values.map(a => this.stringToDate(a.date))
    this.perfectDays = values.map(a => this.stringToDate(a.date));
    // this.perfectDays = await this.precargarDiasOptimos(values).then()
  }
  async precargarDiasOptimos(values:any[]){
    const array:any[] = []
    values.forEach(item => {
      if (this.filtros.tipoActividadSeleccionado === 1) { // Cosecha
        switch (this.filtros.cultivoSeleccionado) {
          case 1: // Trigo
            if (20 <= item.t2m && item.t2m <= 30 && item.rh2m <= 70 && item.prectotcorr <= 5)
              array.push(item);
              break
          case 2: // Soja
            if (20 <= item.t2m && item.t2m <= 40 && item.rh2m <= 70 && item.prectotcorr <= 5)
              array.push(item);
              break
          case 3: // Maíz
            if (24 <= item.t2m && item.t2m <= 30 && 60 <= item.rh2m && item.rh2m <= 70 && item.prectotcorr <= 5)
              array.push(item);
              break
         
        }
      } else if (this.filtros.tipoActividadSeleccionado === 2) { // Siembra
        switch (this.filtros.cultivoSeleccionado) {
          case 1: // Trigo
            if( 15 <= item.t2m && item.t2m <= 25 && item.rh2m >= 70 && item.prectotcorr >= 10)
              array.push(item);
            break;
          case 2: // Soja
            if( 20 <= item.t2m && item.t2m <= 30 && item.rh2m >= 70 && item.prectotcorr >= 15)
              array.push(item);
            break;
          case 3: // Maíz
            if( 25 <= item.t2m && item.t2m <= 35 && item.rh2m >= 70 && item.prectotcorr >= 10)
              array.push(item);
            break;
          
        }
      } 
    
    })
    return array
  }
  public async cargarClick() {  
    this.hideHeader = true
    // this.chartDatasource = await this.service.getPredictData(this.filtros.tipoActividadSeleccionado, 
    //   this.filtros.cultivoSeleccionado, this.filtros.fecha_inicial, 
    //   this.filtros.fecha_final).then();
    await this.prepararDados().then()
    if(this.calendarComponent)
    this.calendarComponent.updateCalendar()
  }
  limpiarClick(){
    this.diaSeleccionado={};
    this.hideHeader = false;
  }
}
