
import { AsyncPipe, CommonModule } from "@angular/common";
import { ChangeDetectionStrategy, Component, inject, input } from "@angular/core";
import { PrecipitacionPipe } from "../shared/precipitacion.pipe";
import { TemperaturePipe } from "../shared/temperatura-pipe.pipe";
import { PresionPipe } from "../shared/presion-pipe.pipe";
import { VelocidadPipe } from "../shared/velocidad-pipe.pipe";
import { VisibilidadPipePipe } from "../shared/visibilidad-pipe.pipe";
import { IconesPipePipe } from "../shared/icones-pipe.pipe";
import { IconsService } from "../service/icons.service";
import { UnitsService } from "../service/units.service";
import { LoaderService } from "../service/loader.service";
@Component({
  selector: 'app-clima-actual',
  standalone: true,
  imports: [CommonModule,

    PrecipitacionPipe,
    TemperaturePipe,
    PresionPipe,
    VelocidadPipe,
    VisibilidadPipePipe,
    IconesPipePipe,
    AsyncPipe],
  templateUrl: './clima-actual.component.html',
  styleUrl: './clima-actual.component.css'
})
export class ClimaActualComponent {
  public data = input.required<any>();
  public geoData = input.required<any>();

  /**
   * Injects the iconsService to retrieve the list of weather icons.
   */
  public iconsService: IconsService = inject(IconsService);

  /**
   * Injects the UnitsService to manage user preferences for units of measurement.
   */
  public unitsService: UnitsService = inject(UnitsService);

  /**
   * Inject the LoaderService to show or hide the skeleton loader
   */
  public loaderService: LoaderService = inject(LoaderService);

  /**
   * Holds the current date.
   */
  public currentDate = new Date();
}
