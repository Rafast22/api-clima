import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable, delay, forkJoin, of, switchMap } from "rxjs";
import { environment } from "../../environments/environment.development";
import { IWeatherOne } from "../interfaces/weather-owm.interface";
/**
 * Service to retrieve weather data from OpenWeatherMap API.
 */
@Injectable({
  providedIn: "root",
})
export class WeatherService {
   /**
   * HttpClient to perform HTTP requests.
   */
   private http: HttpClient = inject(HttpClient);

   /**
    * Service to manage language settings.
    */
   
 
   /**
    * API key for OpenWeatherMap.
    */
   private readonly weatherOwmKey: string = environment.WEATHER_OWM_KEY;
 
   /**
    * Environment URLs for production or mock data.
    */
   private readonly isProduction: boolean = environment.IS_PRODUCTION;
 
   /**
    * URL for the OpenWeatherMap One Call endpoint.
    */
   private readonly weatherOwmOne_mock: string = environment.MOCK.WEATHER_OWM_ONE;
   private readonly weatherOwmOne_endpoint: string = environment.ENDPOINT.WEATHER_OWM_ONE;
 
   /**
    * URL for the OpenWeatherMap AQI endpoint.
    */
   private readonly weatherOwmAqi_mock: string = environment.MOCK.WEATHER_OWM_AQI;
   private readonly weatherOwmAqi_endpoint: string = environment.ENDPOINT.WEATHER_OWM_AQI;
 
   /**
    * Retrieves comprehensive weather data in a single request.
    * @returns {Observable<IWeatherOne>} An Observable emitting the weather data.
    */
   private getWeatherOne(lat: number, lon: number): Observable<IWeatherOne> {
     const url = this.isProduction
       ? `${this.weatherOwmOne_endpoint}lat=${lat}&lon=${lon}&units=metric&lang=es&appid=${this.weatherOwmKey}`
       : this.weatherOwmOne_mock;
     return this.http.get<IWeatherOne>(url);
   }
 
   /**
    * Retrieves air quality index (AQI) data.
    * @returns {Observable<any>} An Observable emitting the AQI data.
    */
   private getWeatherAqi(lat: number, lon: number): Observable<any> {
     const url = this.isProduction
       ? `${this.weatherOwmAqi_endpoint}lat=${lat}&lon=${lon}&appid=${this.weatherOwmKey}`
       : this.weatherOwmAqi_mock;
     return this.http.get<any>(url);
   }
 
   /**
    * Combines weather and AQI data into a single object.
    * @returns {Observable<any>} An Observable emitting an object containing both weather data and AQI information.
    */
   public weatherMergeData(lat: number, lon: number): Observable<any> {
     return forkJoin({
       weather: this.getWeatherOne(lat, lon),
       aqi: this.getWeatherAqi(lat, lon),
     }).pipe(
       switchMap((results) => {
         const combinedData = {
           ...results.weather,
           aqi: results.aqi,
         };
         return of(combinedData);
       }),
     );
   }
 }