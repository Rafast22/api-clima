import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Route, Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule, MatIconModule, HttpClientModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  
  formulario! : FormGroup;

  submetido = false
  
  email: string = '';
  password: string = '';
  confirmPassword: string = '';

  constructor(
    private fb: FormBuilder,
    private route: Router,
    private matIconRegistry: MatIconRegistry,private domSanitizer: DomSanitizer,
    
  ) {
    this.matIconRegistry.addSvgIcon(
      "google",
      this.domSanitizer.bypassSecurityTrustResourceUrl("../../../assets/imagen/google_icon.svg")
    );
  }
  ngOnInit(): void {
    this.formulario = this.fb.group({
      nome: ['', [Validators.required, Validators.maxLength(120)]],
      email: ['',[ Validators.required,  Validators.email]],
      senha: ['', [Validators.required, Validators.pattern('^(?=.*?[!@#$%¨&*])(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')]]
    })
  }
  btnEntrar(){
    this.route.navigateByUrl("/login")
  }
  register() {
    this.route.navigateByUrl("/principal")
  }
}
