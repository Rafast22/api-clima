import { Component, ElementRef, Input, OnInit, Renderer2, ViewChild } from '@angular/core';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-clima-card',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './clima-card.component.html',
  styleUrl: './clima-card.component.css'
})
export class ClimaCardComponent implements OnInit{
  @ViewChild('calendarContainer') calendarContainer: ElementRef | undefined = undefined;
  weatherData:weather[]=[];
  constructor(private renderer: Renderer2, private matIconRegistry: MatIconRegistry,private domSanitizer: DomSanitizer){
    for (let index = 1; index < 21; index++) {
      this.matIconRegistry.addSvgIcon(index.toString(), this.domSanitizer.bypassSecurityTrustResourceUrl(`../../../assets/icons/newWeatherIcons/${index}.svg`));
    }
    for (let index = 1; index < 21; index++) {
      this.matIconRegistry.addSvgIcon(`wind-${index}`, this.domSanitizer.bypassSecurityTrustResourceUrl(`../../../assets/icons/viento/${index}.svg`));
    }
    this.predicciones = [];
  }
  @Input()
  public predicciones:any[];
  
  moverCards(direcao: number) {
    if(!this.calendarContainer) return;
    const container = this.calendarContainer.nativeElement;
    // const cards = container.querySelector('.container');
    const cardWidth = container.querySelector('.weather-card').offsetWidth; // Largura de um card
    const scrollAmount = cardWidth * direcao + 10; // Quantidade de pixels para rolar

    // Usa `scrollLeft` para mover os cards horizontalmente
    container.scrollLeft += scrollAmount; 
  }


  ngOnInit(): void {
    // this.weatherData = this.getDiasDaSemanaAtual();
    this.prepareDayList()

  }

  prepareDayList(){
    if(this.predicciones){

      const date:Date = new Date();
      for (let index = date.getDate(); index < (date.getDate()+7); index++) {
        const day:weather = <weather>{};
        day.today = index==date.getDate();
        day.data = new Date(date.getFullYear(), date.getMonth(), index);
        if(index == date.getDate()){
          day.name = "Hoy"
        }
        else if(index == date.getDate()+1){
          day.name = "Mañana"
        }
        else{
          day.name = day.data.toLocaleString('default', { weekday: 'long'});
          day.name = day.name.charAt(0).toUpperCase() + day.name.slice(1);
        }
        day.month = day.data.toLocaleString('default', { month: 'short'})
        day.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/2.svg'
        this.weatherData.push(day)
        // day.min = '°';
        // day.max  ='°'
        // day.precip = '%'
      }
      for (let index = 0; index < this.predicciones.length; index++) {
        const predict = this.predicciones[index];
        const data = this.weatherData[index];
        data.min = predict.min+'°';
        data.max = predict.max+'°';
        if(predict.precip) {
          data.precip = predict.precip+"%";
          data.precipMM = predict.precipMM+" mm";
          if (predict.precip <20) 
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg'
          else if(predict.precip >=20 && predict.precip <30)
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/2.svg'
          else if(predict.precip >=30 && predict.precip <40)
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/3.svg'
          else if(predict.precip >=40 && predict.precip <50)
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/4.svg'
          else if(predict.precip >=50 && predict.precip <60)
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/4.svg'
          else if(predict.precip >=60 && predict.precip <70)
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/5.svg'
          else if(predict.precip >=70 && predict.precip <80)
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/13.svg'
          else if(predict.precip >=80 && predict.precip <90)
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/14.svg'
          else if(predict.precip >=90 && predict.precip <=100)
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/15.svg'
          else
            data.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg'

        }
          
        
      }

    }
    
  }

}
interface weather{
  name:string;
  month:string
  iconUrl?:string;
  data:Date;
  today:boolean;
  min:string;
  max:string;
  precipMM:string;
  precip:string;
}