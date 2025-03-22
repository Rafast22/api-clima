import { Directive, ElementRef, HostListener, Input, OnInit, Renderer2 } from '@angular/core';

@Directive({
  selector: '[Dia]',
  standalone: true,

})
export class DiaOptimoDirective implements OnInit {
  @Input() Dia?:any; 
  @Input() selectDay: (date?: Date) => void = () => {};

  constructor(private el: ElementRef, private renderer: Renderer2) { 
  }
  @HostListener('click')
  onClick() {
    // if (this.Dia.Optimo) {
      if(this.selectDay) this.selectDay(this.Dia.UTCDate);
    // }
  }

  ngOnInit() {
    if (this.Dia.Optimo) { 
      this.renderer.removeClass(this.el.nativeElement, "date")
      this.renderer.addClass(this.el.nativeElement, "perfect-date")
    }
    else{
      this.renderer.removeClass(this.el.nativeElement, "perfect-date")
      this.renderer.addClass(this.el.nativeElement, "date")
    }
    if(this.Dia.Today) this.renderer.addClass(this.el.nativeElement, "today")

  }
}