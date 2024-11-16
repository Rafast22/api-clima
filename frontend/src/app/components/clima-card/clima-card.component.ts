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
    const date:Date = new Date();
    for (let index = date.getDate(); index < (date.getDate()+7); index++) {
      const day:weather = <weather>{};
      day.today = index==date.getDate();
      day.data = new Date(date.getFullYear(), date.getMonth(), index);
      day.name = day.data.toLocaleString('default', { weekday: 'long'});
      day.name = day.name.charAt(0).toUpperCase() + day.name.slice(1);
      day.month = day.data.toLocaleString('default', { month: 'short'})
      day.iconUrl = 'https://www.tiempo.com/css/v3/svgs/symbols/color/1.svg'
      this.weatherData.push(day)
      day.min = '°';
      day.max  ='°'
      day.precip = '%'
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
  precip:string;
}