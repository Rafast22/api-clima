import { AsyncPipe, CommonModule } from '@angular/common';
import { Component, HostListener, inject, input } from '@angular/core';

import { CarouselModule } from 'primeng/carousel';
import { PrecipitacionPipe } from '../shared/precipitacion.pipe';
import { UnixTimestampPipe } from '../shared/u-timestamp-pipe.pipe';
import { TemperaturePipe } from '../shared/temperatura-pipe.pipe';
import { VisibilidadPipePipe } from '../shared/visibilidad-pipe.pipe';
import { PresionPipe } from '../shared/presion-pipe.pipe';
import { VelocidadPipe } from '../shared/velocidad-pipe.pipe';
import { IconesPipePipe } from '../shared/icones-pipe.pipe';
import { IconsService } from '../service/icons.service';
import { UnitsService } from '../service/units.service';
import { LoaderService } from '../service/loader.service';

@Component({
  selector: 'app-clima-pronostico',
  standalone: true,
  imports: [
    CommonModule,
    CarouselModule,
   /*SkeletonModule,*/
    PrecipitacionPipe,
    UnixTimestampPipe,
    TemperaturePipe,
    VisibilidadPipePipe,
    PresionPipe,
    VelocidadPipe,
    IconesPipePipe,
    AsyncPipe
  ],
  templateUrl: './clima-pronostico.component.html',
  styleUrl: './clima-pronostico.component.css'
})
export class ClimaPronosticoComponent {

/**
   * The input data containing weather information.
   */
public readonly dataInput = input.required<any>();
/**
 * The type of forecast to display, either 'hourly' or 'daily'.
 */
public readonly forecastType = input.required<"hourly" | "daily">();

/**
 * The number of slides to show in the view, adjusted based on screen width.
 */
public slidesPerView: number = 5;

/**
 * The current width of the screen, used to adjust `slidesPerView`.
 */
private screenWidth!: number;

/**
 * Listens to window resize events to adjust the number of visible slides.
 */
@HostListener("window:resize")
getScreenWidth(): void {
  this.screenWidth = window.innerWidth;
  if (this.screenWidth >= 320 && this.screenWidth <= 620) {
    this.slidesPerView = 3;
  } else if (this.screenWidth >= 620 && this.screenWidth <= 998) {
    this.slidesPerView = 4;
  } else {
    this.slidesPerView = 5;
  }
}

/**
 * Service to retrieve and manage weather icons.
 */
public iconsService: IconsService = inject(IconsService);

/**
 * Service to manage user preferences for units of measurement.
 */
public unitsService: UnitsService = inject(UnitsService);

/**
 * Service to control the display of the skeleton loader during data loading.
 */
public loaderService: LoaderService = inject(LoaderService);
}

