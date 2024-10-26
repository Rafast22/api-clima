import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { confirmPasswordValidator } from './validators/confirmar-contrasena.validator';
import {MatInputModule} from '@angular/material/input';
import { UserService } from '../../services/user/user.service';
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule, MatIconModule, HttpClientModule, MatInputModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css',
  
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
    private userService:UserService
    
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
      contrasena: ['', [Validators.required, confirmPasswordValidator, Validators.pattern('^(?=.*?[!@#$%¨&*])(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')]],
      confirmContrasena: ['', [Validators.required, confirmPasswordValidator]]
      
    })
  }
  btnEntrar(){
    this.route.navigateByUrl("/login");
  }
  async register() {
    if(this.formulario.valid){
      // this.userService.cadastrar(this.formulario).subscribe()
    }
  }
}
