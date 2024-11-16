import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormsModule, NgModel, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { HttpClientModule } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';
import { UserService } from '../../services/user/user.service';
import {MatInputModule} from '@angular/material/input';
import {merge} from 'rxjs';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';



@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule, MatIconModule, HttpClientModule, MatInputModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  providers:[UserService]
})
export class LoginComponent implements OnInit {
  readonly email = new FormControl('', [Validators.required, Validators.email]);
  readonly password = new FormControl('', [Validators.required]);
  errorMessageEmail = signal('');
  errorMessagepassword = signal('');

  formLogar! : FormGroup;
  mensagemErro = "";
  submetido = false;

  // public email:string = '';
  // public password:string = '';
  
  constructor(
    private fb: FormBuilder,
    private service: UserService,
    private route: Router,
    private matIconRegistry: MatIconRegistry,private domSanitizer: DomSanitizer,
    
  ) { 
    this.matIconRegistry.addSvgIcon(
      "google",
      this.domSanitizer.bypassSecurityTrustResourceUrl("../../../assets/imagen/google_icon.svg")
    );
    this.matIconRegistry.addSvgIcon(
      "facebook",
      this.domSanitizer.bypassSecurityTrustResourceUrl("../../../assets/imagen/facebook_icon.svg")
    );
    this.formLogar = this.fb.group({
      email: this.email,
      password: this.password,
    })
    const merger = merge; 
    merger(this.email.statusChanges, this.email.valueChanges).pipe(takeUntilDestroyed()).subscribe(() => this.updateErrorMessage());
    merger(this.password.statusChanges, this.password.valueChanges).pipe(takeUntilDestroyed()).subscribe(() => this.updateErrorMessagePassword());
   
   }
  
   updateErrorMessage() {
      if (this.email.hasError('required')) {
        this.errorMessageEmail.set('El email es obligatorio');
      } else if (this.email.hasError('email')) {
        this.errorMessageEmail.set('El email debe ser valido');
      } else{
        this.errorMessageEmail.set('');
      }
    
  

  }

  updateErrorMessagePassword() {
  
      if(this.password.hasError("required")) {
        this.errorMessagepassword.set('La contraseña es obligatoria');
      }
      else{
        this.errorMessagepassword.set('');
      }

  }

  ngOnInit(): void {
    
  }
  btnInscrever(){
    this.route.navigateByUrl('register')
  }

  async login():Promise<void>{
    this.submetido = true
    if(this.formLogar.valid){
      const form = this.formLogar.value
      await this.service.login(form).then((resposta : boolean)=>{
        console.log (resposta)
        if(resposta){
          this.route.navigateByUrl("principal")
        }else{
            this.mensagemErro = 'Usuario o Contrasenha incorrecta'
            console.log(this.mensagemErro)
        }
      })
    }
  }

  public registerWithFacebook(){
    
  }

}
