import { Component, ElementRef, EventEmitter, Input, OnInit, Output, Renderer2, ViewChild } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { PredicService } from '../../services/predictions/predic.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-clima-card',
  standalone: true,
  imports: [MatIconModule, MatButtonModule, CommonModule],
  templateUrl: './clima-card.component.html',
  styleUrl: './clima-card.component.css'
})
export class ClimaCardComponent implements OnInit {
  @ViewChild('calendarContainer') calendarContainer: ElementRef | undefined = undefined;
  @Output()
  selectCard:EventEmitter<Date> = new EventEmitter<Date>();
  selectedDate: Date

  weatherData: Weather[] = [];
  public predicciones: Predict[] = [];
  constructor(private renderer: Renderer2, private service: PredicService, private matIconRegistry: MatIconRegistry, private domSanitizer: DomSanitizer) {
    const today = new Date();
    this.selectedDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    for (let index = 1; index < 21; index++) {
      this.matIconRegistry.addSvgIcon(index.toString(), this.domSanitizer.bypassSecurityTrustResourceUrl(`../../../assets/icons/newWeatherIcons/${index}.svg`));
    }
    for (let index = 1; index < 21; index++) {
      this.matIconRegistry.addSvgIcon(`wind-${index}`, this.domSanitizer.bypassSecurityTrustResourceUrl(`../../../assets/icons/viento/${index}.svg`));
    }
  }

  moverCards(direcao: number) {
    if (!this.calendarContainer) return;
    const container = this.calendarContainer.nativeElement;
    const weatherCard = container.querySelector('.weather-card');
    if (!weatherCard) return;
    const cardWidth = weatherCard.offsetWidth;
    const scrollAmount = cardWidth * direcao + 10;
    container.scrollLeft += scrollAmount;
  }


  async ngOnInit() {
    this.predicciones = await this.service.getPredictWeek();
    for (const a of this.predicciones) {
      Object.assign(a, { 'date': new Date(a.date) })
    }
    await this.prepareDayList()
  }

  async prepareDayList(): Promise<void> {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    for (let offset = 0; offset < 8; offset++) {
      const date = new Date(today);
      date.setDate(today.getDate() + offset);

      const day: Weather = {
        today: offset === 0,
        data: date,
        name: this.getDayName(offset),
        month: date.toLocaleString('es-ES', { month: 'short' }),
        iconUrl: 'https://www.tiempo.com/css/v3/svgs/symbols/color/2.svg',
      };

      const predicts = this.predicciones.filter(
        (p) => p.date.getDate() === day.data.getDate() && p.date.getMonth() === day.data.getMonth()
      );

      this.setWeatherData(day, predicts);
      this.weatherData.push(day);
    }
  }

  private getDayName(offset: number): string {
    const date = new Date();
    date.setDate(date.getDate() + offset);

    if (offset === 0) return 'Hoy';
    if (offset === 1) return 'Mañana';

    const dayName = date.toLocaleString('es-ES', { weekday: 'long' });
    return dayName.charAt(0).toUpperCase() + dayName.slice(1);
  }

  private setWeatherData(day: Weather, predicts: { t2m: number; prectotcorr: number, probability_rain: number, info: boolean }[]): void {
    const t2mValues = predicts.map((p) => p.t2m);
    if (t2mValues.length > 0) {
      day.min = `${Math.round(Math.min(...t2mValues))}°`;
      day.max = `${Math.round(Math.max(...t2mValues))}°`;
    }
    else {
      day.min = '0°'
      day.max = '0°'
    }

    const precipAvg = predicts.reduce((acc, curr) => acc + curr.prectotcorr, 0) / predicts.length;
    const rainProAvg = predicts.reduce((acc, curr) => acc + curr.probability_rain, 0) / predicts.length;
    const infos = predicts.filter(r => r.info == false);
    const info = infos.length < 1
    if (info && precipAvg > 0) {
      day.precip = `${precipAvg.toFixed(2)} %`;
      day.precipMM = `🌧️ ${precipAvg.toFixed(2)} mm`;
      day.iconUrl = this.getIconUrl(precipAvg);
    }
    else {
      day.precipMM = ``;
      day.iconUrl = this.getIconUrl(0);
    }
    if (info && rainProAvg > 0) {
      day.precip = `💧 ${rainProAvg.toFixed(2)} %`;
    }
    else {
      day.precip = '';

    }
  }

  selectWeatherCard(e: Date) {
    this.selectCard.emit(e);
    this.selectedDate = e;
    const date = this.weatherData.find((r:Weather) => r.today);
    if(date)
      date.today = false;
  }

  private getIconUrl(precipAvg: number): string {
    const icons: { min: number; max: number; url: string }[] = [
      { min: 0, max: 10, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg' },
      { min: 10, max: 20, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/2.svg' },
      { min: 20, max: 30, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/3.svg' },
      { min: 30, max: 40, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/4.svg' },
      { min: 40, max: 50, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/5.svg' },
      { min: 50, max: 60, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/12.svg' },
      { min: 60, max: 70, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/13.svg' },
      { min: 70, max: 80, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/14.svg' },
      { min: 80, max: 90, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/15.svg' },
      { min: 90, max: 100, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/28.svg' },
      { min: 100, max: 1000, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/29.svg' },

    ];

    const match = icons.find((icon) => precipAvg >= icon.min && precipAvg < icon.max);
    return match?.url || 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg';
  }
}


interface Weather {
  name?: string;
  month?: string
  iconUrl?: string;
  data: Date;
  today?: boolean;
  min?: string;
  max?: string;
  precipMM?: string;
  precip?: string;
}

interface Predict {
  date: Date;
  prectotcorr: number;
  qv2m: number;
  rh2m: number;
  t2m: number;
  ws2m: number;
  probability_rain: number;
  info: boolean;
}