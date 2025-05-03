import { Directive, ElementRef, HostListener, Input, OnChanges, OnInit, Renderer2, SimpleChanges } from '@angular/core';

@Directive({
  selector: '[dayInfo]',
  standalone: true,

})
export class DiaOptimoDirective implements OnInit, OnChanges {
  @Input() dayInfo?: any;
  @Input() selectDay: (date?: Date) => void = () => { };

  constructor(private el: ElementRef, private renderer: Renderer2) {
  }
  @HostListener('click')
  onClick() {
    if (this.dayInfo)
      if (this.selectDay) this.selectDay(this.dayInfo.Date);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['dayInfo']) {
      this.ngOnInit();
    }
  }

  ngOnInit() {
    if (this.dayInfo.Optimo && this.dayInfo.Optimo > 60 ) {
      this.renderer.removeClass(this.el.nativeElement, "date")
      this.renderer.addClass(this.el.nativeElement, "perfect-date") 
    }
    else {
      this.renderer.removeClass(this.el.nativeElement, "perfect-date")
      this.renderer.addClass(this.el.nativeElement, "date")
    }

    // switch (this.dayInfo.Optimo) {
    //   case 2:
    //     // this.removeClass("date", "perfect-date muito")
    //     this.renderer.removeStyle(this.el.nativeElement, 'backgroundColor');
    //     this.renderer.setStyle(this.el.nativeElement, 'backgroundColor', '#ff0000');
    //     break;
    //   case 1:
    //     // this.removeClass("date", "perfect-date ruim");
    //     this.renderer.removeStyle(this.el.nativeElement, 'backgroundColor');
    //     this.renderer.setStyle(this.el.nativeElement, 'backgroundColor', '#ff8000');
    //     break;
    //   case 0:
    //     // this.removeClass("date", "perfect-date neutro");
    //     // this.renderer.removeStyle(this.el.nativeElement, 'backgroundColor');
    //     // this.renderer.setStyle(this.el.nativeElement, 'backgroundColor', '#ffff00');
    //     break;
    //   case -1:
    //     // this.removeClass("date", "perfect-date bom");
    //     this.renderer.removeStyle(this.el.nativeElement, 'backgroundColor');
    //     this.renderer.setStyle(this.el.nativeElement, 'backgroundColor', '#80ff00');
    //     break;
    //   case -2:
    //     // this.removeClass("date", "perfect-date excelente");
    //     this.renderer.removeStyle(this.el.nativeElement, 'backgroundColor');
    //     this.renderer.setStyle(this.el.nativeElement, 'backgroundColor', '#00ff00');
    //     break;
    //   default:
    //     // this.removeClass("muito", "date")
    //     // this.removeClass("ruim", "date")
    //     // this.removeClass("neutro", "date")
    //     // this.removeClass("bom", "date")
    //     // this.removeClass("excelente", "date")
    //     break;
    // }
    
    if (this.dayInfo.Today) this.renderer.addClass(this.el.nativeElement, "today")

  }
}