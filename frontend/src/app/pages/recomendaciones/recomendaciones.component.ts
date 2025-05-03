import { AfterViewInit, ChangeDetectionStrategy, Component, ElementRef, inject, model, viewChild, ViewChild } from '@angular/core';
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
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PredicService } from '../../services/predictions/predic.service';
import { CalendarComponent } from '../../components/calendar/calendar.component';
import { ClimaCardComponent } from '../../components/clima-card/clima-card.component';
import { MatExpansionModule } from '@angular/material/expansion';
import { FormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { finalize, tap } from 'rxjs';
import { CommonModule } from '@angular/common';
import { LoadingOverlayService } from '../../components/loading-overlay/loading-overlay.service';
import { LoadingOverlayComponent } from '../../components/loading-overlay/loading-overlay.component';


@Component({
  selector: 'recomendaciones',
  standalone: true,
  imports: [MatToolbarModule, MatCardModule, MatDatepickerModule, CommonModule,
    MatExpansionModule, MatSelectModule, MatGridListModule, MatFormFieldModule,
    MatInputModule, MatButtonModule, CalendarComponent, ClimaCardComponent, MatRadioModule, FormsModule, LoadingOverlayComponent],
  templateUrl: './recomendaciones.component.html',
  styleUrl: './recomendaciones.component.css',
  providers: [provideNativeDateAdapter(), { provide: MAT_DATE_LOCALE, useValue: 'es-PY' }],
  changeDetection: ChangeDetectionStrategy.OnPush,

})
export class RecomendacionesComponent implements AfterViewInit {
  @ViewChild('calendarComponent') calendarComponent: CalendarComponent | undefined = undefined;
  @ViewChild("picker") picker!: any;
  isLoading: boolean = false;
  chart: Chart = <Chart>{};
  _perfectDays: any[] = [];
  public get perfectDays(): any[] {
    if (this.calendarComponent)
      return this._perfectDays;
    return []
  }
  public set perfectDays(v: any[]) {
    for (const r of v) {
      r.date = new Date(r.date);
    }
    // this._perfectDays = [...v];
    this._perfectDays = [...v];
    if (this.calendarComponent) {
      this.calendarComponent?.updateCalendar();
    }
    this.setPerfectDaysDict(`${this.currentDate.getMonth()}-${this.currentDate.getFullYear()}`, v)
  }
  isLoading$ = this.loadingService.loading$;
  actividadOptions: Option[] = [];
  cultivoOptions: Option[] = [];

  public chartDatasource: DateObject[] = [];
  public diaSeleccionado: any;
  public hideHeader: boolean = false
  public _CardClimaOpen: boolean = true;
  public _CardDiasOptimos: boolean = false;
  public filtros: Filtros = <Filtros>{};
  private currentDate: Date = new Date();
  private _perfectDaysDict: { [date: string]: string } = {};
  public get _diaSelecionado(): boolean {
    return (this.diaSeleccionado ? false : true)
  }
  public get getCultivoSelecionado(): string {
    if (this.filtros.Cultivo)
      return this.cultivos.find(f => f.value == this.filtros.Cultivo).description
    else return ""
  }

  public getPerfectDaysDict(monthYear: string): any | undefined {
    return this._perfectDaysDict[monthYear];
  }
  public setPerfectDaysDict(monthYear: string, value: any) {
    const [month, year] = monthYear.split("-");

    this._perfectDaysDict[monthYear] = value;
    // this._perfectDaysDict.forEach
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
  constructor(private breakpointObserver: BreakpointObserver, private service: PredicService, private loadingService: LoadingOverlayService) {
    const d: Date = new Date();
    this.perfectDays = [];
    this.filtros.Actividad = 1;
    this.filtros.Cultivo = 1;
    this.createCombos(this.cultivos, this.filtros.Cultivo);
    this.createCombos(this.actividades, this.filtros.Actividad);
  }

  protected createCombos(itens: any[], defaultChecked: number) {
    for (const item of itens) {
      var Checked = item.value == defaultChecked;
      this.actividadOptions.push({
        name: item.description,
        value: item.value,
        checked: Checked,
      });
    }
  }

  public CultivoChange() {
    this.prepararDados(this.currentDate);
    this._perfectDaysDict = {};
  }

  public ActividadChange() {
    this.prepararDados(this.currentDate);
    this._perfectDaysDict = {};
  }

  async monthChange(currentDate: Date) {
    this.currentDate = currentDate;
    if (this.calendarComponent)
      this.calendarComponent.currentDate = currentDate;
    this.chamarCacheOffset(currentDate);
    const cachePerfectDays = this.getPerfectDaysDict(`${currentDate.getMonth()}-${currentDate.getFullYear()}`);
    if (cachePerfectDays) {
      this.perfectDays = cachePerfectDays;
      return;
    }
    this.service.getPredictDataByRange(this.filtros.Actividad,
      this.filtros.Cultivo, new Date(currentDate.getFullYear(), currentDate.getMonth(), 1),
      new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0)).then(data => this.perfectDays = [...data.map((m: any) => ({ date: m.date, perfect: m.perfect }))]);

  }

  chamarCacheOffset(currentDate: Date) {
    [-2, -1, 1, 2].forEach(offset => {
      this.preencherCacheOffset(currentDate, offset)
    })
  }

  preencherCacheOffset(currentDate: Date, offset: number) {
    const d = new Date(currentDate.getFullYear(), currentDate.getMonth() + offset, 1)
    if (!(`${d.getMonth()}-${d.getFullYear()}` in Object.keys(this._perfectDaysDict))) {
      this.service.getPredictDataByRange(this.filtros.Actividad,
        this.filtros.Cultivo, d,
        new Date(currentDate.getFullYear(), currentDate.getMonth() + offset + 1, 0)).then(data =>
          this.setPerfectDaysDict(`${currentDate.getMonth() + offset}-${currentDate.getFullYear()}`, data));

    }
  }

  async _onSelectDate(day?: Date) {
    if (!day) {
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
    const tempList = this.chartDatasource.map(m => m.t2m);
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

  public async prepararDados(currentDate?:Date) {
    let today: Date = new Date();

    if(currentDate){
      today = currentDate
    }
    let first_day = new Date(today.getFullYear(), today.getMonth(), 1)
    
    this.loadingService.show();
    this.service.getObserverPredictDataByRange(this.filtros.Actividad, this.filtros.Cultivo, first_day, new Date(today.getFullYear(), today.getMonth() + 1, 0)).pipe(
      tap(_ => {
        this.perfectDays = _;
      }),
      finalize(() => {
        this.loadingService.hide();

      })
    ).subscribe(
      () => { }, 
      (error) => {
        console.error('Erro na chamada ao backend:', error);
        this.loadingService.hide();
      }
    );


    // this.perfectDays = [...this.chartDatasource.map((m: any) => ({ date: m.date, perfect: m.perfect }))]
    this.chamarCacheOffset(first_day);


  }

}

interface DateObject {
  prectotcorr: number,
  qv2m: number,
  rh2m: number,
  ws2m: number,
  date: Date,
  t2m: number
}

interface Filtros {
  Actividad: number;
  Cultivo: number;
}
interface Option {
  name: string;
  value: number;
  checked: boolean;
}
