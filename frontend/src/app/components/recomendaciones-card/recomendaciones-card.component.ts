import { AfterViewInit, ChangeDetectionStrategy, Component, ElementRef, model, viewChild, ViewChild } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MAT_DATE_LOCALE, provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MatSelectModule } from '@angular/material/select';
import Chart from 'chart.js/auto';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatGridListModule } from '@angular/material/grid-list';
import { PredicService } from '../../services/predictions/predic.service';
import { CalendarComponent } from '../calendar/calendar.component';
import { ClimaCardComponent } from '../clima-card/clima-card.component';
import { MatExpansionModule } from '@angular/material/expansion';
import { FormsModule } from '@angular/forms';
import {MatRadioModule} from '@angular/material/radio';


@Component({
  selector: 'app-recomendaciones-card',
  standalone: true,
  imports: [MatToolbarModule, MatCardModule, MatDatepickerModule, 
    MatExpansionModule, MatSelectModule, MatGridListModule, MatFormFieldModule, 
    MatInputModule, MatButtonModule, CalendarComponent, ClimaCardComponent, MatRadioModule, FormsModule],
  templateUrl: './recomendaciones-card.component.html',
  styleUrl: './recomendaciones-card.component.css',
  providers: [provideNativeDateAdapter(), { provide: MAT_DATE_LOCALE, useValue: 'es-PY' }],
  changeDetection: ChangeDetectionStrategy.OnPush,

})
export class RecomendacionesCardComponent implements AfterViewInit {
  @ViewChild('calendarComponent') calendarComponent: CalendarComponent | undefined = undefined;
  @ViewChild("picker") picker!: any;

  chart: Chart = <Chart>{};
  perfectDays: any[] = [];
  actividadOptions: Option[] = [];
  cultivoOptions: Option[] = [];

  public chartDatasource: DateObject[] = [];
  public diaSeleccionado: any;
  public hideHeader: boolean = false
  public _CardClimaOpen: boolean = true;
  public _CardDiasOptimos: boolean = false;
  public filtros: Filtros = <Filtros>{};
  private currentDate: Date = new Date();

  public get _diaSelecionado(): boolean {
    return (this.diaSeleccionado ? false : true)
  }
  public get getCultivoSelecionado(): string {
    if (this.filtros.Cultivo)
      return this.cultivos.find(f => f.value == this.filtros.Cultivo).description
    else return ""

  }
  public get getTipoSelecionado(): string {
    if (this.filtros.Actividad)
      return this.cultivos.find(f => f.value == this.filtros.Actividad).description
    else return ""
  }
  get isMobile(): boolean {
    return this.breakpointObserver.isMatched('(max-width: 767px)');
  }
  public get CardClimaOpen(): boolean {
    return !this._CardDiasOptimos;
  }
  public set CardClimaOpen(v: boolean) {
    this._CardClimaOpen = v;
  }
  public get CardDiasOptimos(): boolean {
    return !this._CardClimaOpen;
  }
  public set CardDiasOptimos(v: boolean) {
    this._CardDiasOptimos = v;
  }
  cultivos: any[] = [
    { value: 1, description: "Maíz" },
    { value: 2, description: "Trigo" },
    { value: 3, description: "Soja" }
  ];

  actividades: any[] = [
    { value: 1, description: "Cosecha" },
    { value: 2, description: "Siembra" }
  ];

  async ngAfterViewInit() {
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
    this._onSelectDate();
    this.prepararDados();

  }
  constructor(private breakpointObserver: BreakpointObserver, private service: PredicService) {
    const d: Date = new Date();
    this.perfectDays = [];
    this.filtros.Actividad = 1;
    this.filtros.Cultivo = 1;
    this.createCombos(this.cultivos, this.filtros.Cultivo);
    this.createCombos(this.actividades, this.filtros.Actividad);
  }

  protected createCombos(itens: any[], defaultChecked: number){
    for (const item of itens) {
      var Checked = item.value == defaultChecked;
      this.actividadOptions.push({
        name: item.description,
        value: item.value,
        checked: Checked,
      });
    }
  }

  public CultivoChange(){
    this.monthChange(this.currentDate);
  }

  public ActividadChange(){
    this.monthChange(this.currentDate);
  }

  async monthChange(currentDate: Date){
    this.currentDate = currentDate;
    const data = await this.service.getPredictDataByRange(
      new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()),
      new Date(currentDate.getFullYear(), currentDate.getMonth()+1, currentDate.getDate()), this.filtros.Actividad,
      this.filtros.Cultivo).then();
      this.perfectDays = [];
      this.perfectDays = data;
  }

  async _onSelectDate(day?: Date) {
    if(!day){
      const today = new Date();
      day = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    } 
    this.diaSeleccionado = {}
    const a = await this.service.getPredictDataDate(day)
    a.forEach((element: any) => {
      element.date = new Date(element.date);
    });
    this.chartDatasource = [...a];
    this.diaSeleccionado.Dia = day;
    this.diaSeleccionado.HumedadMedia = (this.chartDatasource.reduce((acumuladorH: number, humedad: any) => acumuladorH + humedad.rh2m, 0) / this.chartDatasource.length).toFixed(2);
    this.diaSeleccionado.PrecipitacionMedia = (this.chartDatasource.reduce((acumuladorP: number, precip: any) => acumuladorP + precip.prectotcorr, 0) / this.chartDatasource.length).toFixed(2);
    this.diaSeleccionado.TemperaturaMedia = (this.chartDatasource.reduce((acumuladorT: number, temperatura: any) => acumuladorT + temperatura.t2m, 0) / this.chartDatasource.length).toFixed(2);
    this.changeChartInfo();
  }

  private async changeChartInfo() {
    const tempList = this.chartDatasource.map( m => m.t2m);
    const humList = this.chartDatasource.map(m => m.rh2m);
    const preList = this.chartDatasource.map(m => m.prectotcorr);
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
    const labels = this.chartDatasource.map((d: any) => {
      return `${d.date.getHours() < 10 ? '0' + d.date.getHours() : d.date.getHours()}:${d.date.getMinutes() < 10 ? '0' + d.date.getMinutes() : d.date.getMinutes()}`;
    });
    this.chart.data.datasets = [...dataSources];
    this.chart.data.labels = [...labels];
    this.chart.update();
  }
  
  public async prepararDados() {
    const today: Date = new Date();

    this.chartDatasource = await this.service.getPredictDataByRange(
      new Date(today.getFullYear(), today.getMonth(), today.getDate()),
      new Date(today.getFullYear(), today.getMonth()+1, today.getDate()), this.filtros.Actividad,
      this.filtros.Cultivo).then();
      if (this.calendarComponent)
        this.calendarComponent.updateCalendar();
  }

}

interface DateObject{
  prectotcorr: number,
  qv2m: number,
  rh2m: number,
  ws2m: number,
  date: Date,
  t2m: number
}

interface Filtros{
  Actividad: number;
  Cultivo: number;
}
interface Option {
  name: string;
  value: number;
  checked: boolean;
}
