import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-clima-card',
  standalone: true,
  imports: [],
  templateUrl: './clima-card.component.html',
  styleUrl: './clima-card.component.css'
})
export class ClimaCardComponent implements OnInit{
  weatherData:weather[]=[];
  constructor(){
    
  }
  getDiasDaSemanaAtual(): any[] {
    const diasDaSemana: string[] = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
    const hoje = new Date();
    const diaDaSemanaHoje = hoje.getDay();
  
    return diasDaSemana.slice(diaDaSemanaHoje).concat(diasDaSemana.slice(0, diaDaSemanaHoje)).map((nome, index) => ({
      nome,
      data: new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate() + index),
      iconUrl: 'https://storage.googleapis.com/a1aa/image/GxzhrCYDdoJpExIrQf1lC2ACcmyXf3ZuAE3UTK6hejdpGhRnA.jpg'
    }));
  }

  ngOnInit(): void {
    this.weatherData = this.getDiasDaSemanaAtual();
    // [
    //   { name: 'Domingo', iconUrl: 'https://storage.googleapis.com/a1aa/image/GxzhrCYDdoJpExIrQf1lC2ACcmyXf3ZuAE3UTK6hejdpGhRnA.jpg' },
    //   { name: 'Lunes', iconUrl: 'https://storage.googleapis.com/a1aa/image/FelFfKRwbHmQIUKgoBAcFHxZtSOwWzrJXUVxGTFQOgDRjwoTA.jpg' },
    //   { name: 'Martes', iconUrl: 'https://storage.googleapis.com/a1aa/image/FelFfKRwbHmQIUKgoBAcFHxZtSOwWzrJXUVxGTFQOgDRjwoTA.jpg' },
    //   { name: 'Miercoles', iconUrl: 'https://storage.googleapis.com/a1aa/image/FelFfKRwbHmQIUKgoBAcFHxZtSOwWzrJXUVxGTFQOgDRjwoTA.jpg' },
    //   { name: 'Jueves', iconUrl: 'https://storage.googleapis.com/a1aa/image/FelFfKRwbHmQIUKgoBAcFHxZtSOwWzrJXUVxGTFQOgDRjwoTA.jpg' },
    //   { name: 'Viernes', iconUrl: 'https://storage.googleapis.com/a1aa/image/FelFfKRwbHmQIUKgoBAcFHxZtSOwWzrJXUVxGTFQOgDRjwoTA.jpg' },
    //   { name: 'Sabado', iconUrl: 'https://storage.googleapis.com/a1aa/image/FelFfKRwbHmQIUKgoBAcFHxZtSOwWzrJXUVxGTFQOgDRjwoTA.jpg' },
    // ];
  }

}
interface weather{
  name:string;
  iconUrl?:string;
  data:Date;

}