import { Component, ElementRef, Input, OnInit, Renderer2, ViewChild } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { PredicService } from '../../services/predictions/predic.service';

@Component({
  selector: 'app-clima-card',
  standalone: true,
  imports: [MatIconModule, MatButtonModule],
  templateUrl: './clima-card.component.html',
  styleUrl: './clima-card.component.css'
})
export class ClimaCardComponent implements OnInit{
  @ViewChild('calendarContainer') calendarContainer: ElementRef | undefined = undefined;
  weatherData:weather[]=[];
  constructor(private renderer: Renderer2, private service: PredicService, 
    private matIconRegistry: MatIconRegistry,private domSanitizer: DomSanitizer){
    for (let index = 1; index < 21; index++) {
      this.matIconRegistry.addSvgIcon(index.toString(), this.domSanitizer.bypassSecurityTrustResourceUrl(`../../../assets/icons/newWeatherIcons/${index}.svg`));
    }
    for (let index = 1; index < 21; index++) {
      this.matIconRegistry.addSvgIcon(`wind-${index}`, this.domSanitizer.bypassSecurityTrustResourceUrl(`../../../assets/icons/viento/${index}.svg`));
    }
  }

  public predicciones:Predict[] = [];
  
  moverCards(direcao: number) {
    if(!this.calendarContainer) return;
    const container = this.calendarContainer.nativeElement;
    const weatherCard = container.querySelector('.weather-card');
    if(!weatherCard) return;
    const cardWidth = weatherCard.offsetWidth; 
    const scrollAmount = cardWidth * direcao + 10; 
    container.scrollLeft += scrollAmount; 
  }


  async ngOnInit() {
    // this.weatherData = this.getDiasDaSemanaAtual();
    this.predicciones = await this.service.getPredictWeek();
    for (const a of this.predicciones){
      Object.assign(a, {'date': new Date(a.date)})
    }
    await this.prepareDayList()

  }

  // async prepareDayList(){
  //   if(this.predicciones && this.predicciones.length > 0){

  //     const date:Date = new Date();
  //     for (let index = date.getDate(); index < (date.getDate()+8); index++) {
  //       const day:weather = <weather>{};
  //       day.today = index==date.getDate();
  //       day.data = new Date(date.getFullYear(), date.getMonth(), index);
  //       if(index == date.getDate()){
  //         day.name = "Hoy"
  //       }
  //       else if(index == date.getDate()+1){
  //         day.name = "Mañana"
  //       }
  //       else{
  //         day.name = day.data.toLocaleString('default', { weekday: 'long'});
  //         day.name = day.name.charAt(0).toUpperCase() + day.name.slice(1);
  //       }
  //       day.month = day.data.toLocaleString('default', { month: 'short'})
  //       day.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/2.svg'
  //       this.weatherData.push(day)

  //     }
  //     for (let index = 0; index < this.weatherData.length; index++) {
  //       const predicts = this.predicciones.filter(r => r.date.getDate() == this.weatherData[index].data.getDate());
  //       const data = this.weatherData[index];
  //       const t2m = predicts.map(f => f.t2m);
  //       data.min = Math.round(Math.min(...t2m)).toFixed(0)+'°';
  //       data.max = Math.round(Math.max(...t2m)).toFixed(0)+'°';
  //       const prectotcorr = (predicts.reduce((acc, curr) => acc + curr.prectotcorr, 0)/predicts.length);
  //       const v = predicts.reduce((acc, curr) => acc + curr.prectotcorr, 0);
  //       if(prectotcorr) {
  //         data.precip = prectotcorr.toFixed(2)+" %";
  //         data.precipMM = prectotcorr.toFixed(2)+" mm";
  //         if (prectotcorr <20) 
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg'
  //         else if(prectotcorr >=20 && prectotcorr <30)
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/2.svg'
  //         else if(prectotcorr >=30 && prectotcorr <40)
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/3.svg'
  //         else if(prectotcorr >=40 && prectotcorr <50)
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/4.svg'
  //         else if(prectotcorr >=50 && prectotcorr <60)
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/4.svg'
  //         else if(prectotcorr >=60 && prectotcorr <70)
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/5.svg'
  //         else if(prectotcorr >=70 && prectotcorr <80)
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/13.svg'
  //         else if(prectotcorr >=80 && prectotcorr <90)
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/14.svg'
  //         else if(prectotcorr >=90 && prectotcorr <=100)
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/15.svg'
  //         else
  //           data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg'

  //       }
          
        
  //     }

  //   }
    
  // }

  async prepareDayList(): Promise<void> {
    if (!this.predicciones || this.predicciones.length === 0) return;

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    for (let offset = 0; offset < 8; offset++) {
      const date = new Date(today);
      date.setDate(today.getDate() + offset);

      const day: weather = {
        today: offset === 0,
        data: date,
        name: this.getDayName(offset),
        month: date.toLocaleString('default', { month: 'short' }),
        iconUrl: 'https://www.tiempo.com/css/v3/svgs/symbols/color/2.svg', // Default
      };

      const predicts = this.predicciones.filter(
        (p) => p.date.getDate() === day.data.getDate() && p.date.getMonth() === day.data.getMonth()
      );

      if (predicts.length > 0) {
        this.setWeatherData(day, predicts);
      }

      this.weatherData.push(day);
    }
  }

  private getDayName(offset: number): string {
    const date = new Date();
    date.setDate(date.getDate() + offset);

    if (offset === 0) return 'Hoy';
    if (offset === 1) return 'Mañana';

    const dayName = date.toLocaleString('default', { weekday: 'long' });
    return dayName.charAt(0).toUpperCase() + dayName.slice(1);
  }

  private setWeatherData(day: weather, predicts: { t2m: number; prectotcorr: number }[]): void {
    const t2mValues = predicts.map((p) => p.t2m);
    day.min = `${Math.round(Math.min(...t2mValues))}°`;
    day.max = `${Math.round(Math.max(...t2mValues))}°`;

    const precipAvg = predicts.reduce((acc, curr) => acc + curr.prectotcorr, 0) / predicts.length;
    if (precipAvg > 0) {
      day.precip = `${precipAvg.toFixed(2)} %`;
      day.precipMM = `${precipAvg.toFixed(2)} mm`;
      day.iconUrl = this.getIconUrl(precipAvg);
      return;
    }
    day.precipMM = `0 mm`;
    day.iconUrl = this.getIconUrl(0);

  }

  private getIconUrl(precipAvg: number): string {
    const icons: { min: number; max: number; url: string }[] = [
      { min: 0, max: 20, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg' },
      { min: 20, max: 30, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/2.svg' },
      { min: 30, max: 40, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/3.svg' },
      { min: 40, max: 60, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/4.svg' },
      { min: 60, max: 70, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/5.svg' },
      { min: 70, max: 80, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/13.svg' },
      { min: 80, max: 90, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/14.svg' },
      { min: 90, max: 100, url: 'https://www.tiempo.com/css/v3/svgs/symbols/color/15.svg' },
    ];

    const match = icons.find((icon) => precipAvg >= icon.min && precipAvg < icon.max);
    return match?.url || 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg';
  }
}


interface weather{
  name?:string;
  month?:string
  iconUrl?:string;
  data:Date;
  today?:boolean;
  min?:string;
  max?:string;
  precipMM?:string;
  precip?:string;
}

interface Predict{
  date:Date;
  prectotcorr:number;
  qv2m:number;
  rh2m:number;
  t2m:number;
  ws2m:number;
}