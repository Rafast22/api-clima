import { IAqi } from "./aqi";
import { IWeatherOne } from "./weather-owm.interface";

export interface IWeatherCombined {
  weather: IWeatherOne;
  aqi: IAqi;
}
