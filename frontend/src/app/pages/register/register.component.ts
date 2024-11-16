import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { confirmPasswordValidator } from './validators/confirmar-contrasena.validator';
import {MatInputModule} from '@angular/material/input';
import { UserService } from '../../services/user/user.service';
import { merge, take } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { User } from '../../services/user/user';
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule, MatIconModule, HttpClientModule, MatInputModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css',
  
})
export class RegisterComponent {
  errorMessageName = signal('');
  errorMessageEmail = signal('');
  errorMessagePassword = signal('');
  errorMessageConfirmPassword = signal('');
  formulario! : FormGroup;

  submetido = false
  
  readonly full_name = new FormControl('', [Validators.required, Validators.maxLength(120)])
  readonly email = new FormControl('',[ Validators.required,  Validators.email])
  readonly password = new FormControl('', [Validators.required,Validators.minLength(8)])
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
    this.matIconRegistry.addSvgIcon(
      "facebook",
      this.domSanitizer.bypassSecurityTrustResourceUrl("../../../assets/imagen/facebook_icon.svg")
    );
    const merger = merge; 
    merger(this.email.statusChanges, this.email.valueChanges).pipe(takeUntilDestroyed()).subscribe(() => this.updateErrorMessage("email"));
    merger(this.full_name.statusChanges, this.full_name.valueChanges).pipe(takeUntilDestroyed()).subscribe(() => this.updateErrorMessage("full_name"));
    merger(this.password.statusChanges, this.password.valueChanges).pipe(takeUntilDestroyed()).subscribe(() => this.updateErrorMessage("password"));
    // merger(this.confirmPassword.statusChanges, this.confirmPassword.valueChanges).pipe(takeUntilDestroyed()).subscribe(() => this.updateErrorMessage("confirmPassword"));
   
  }
  ngOnInit(): void {
    this.formulario = this.fb.group({
      full_name: this.full_name,
      email: this.email,
      password: this.password,
      
    })
  }
  btnEntrar(){
    this.route.navigateByUrl("/login");
  }
  async register() {
    const user:User = new User(this.formulario.value)
    if(this.formulario.valid){
      await this.userService.cadastrar(user).then((r:any) => {
        if(r.Ok){
          this.btnEntrar();
        }
        else{
          console.log(r)
        }
      })
    }
  }

  updateErrorMessage(campo:string) {
    switch (campo) {
      case 'full_name':  
        if (this.email.hasError('required')) 
          this.errorMessageName.set('El nombre es obligatorio'); 
        else
          this.errorMessageName.set("");
        break;        
      case 'email':
        if (this.email.hasError('required')) {
          this.errorMessageEmail.set('El email es obligatorio');
        } else if (this.email.hasError('email')) {
          this.errorMessageEmail.set('El email debe ser valido');
        } else{
          this.errorMessageEmail.set('');
        }    
        break;
      case 'password':
        if(this.password.hasError("required")) {
          this.errorMessagePassword.set('La contraseña es obligatoria');
        }else if(this.password.hasError('minlength')) {
          this.errorMessagePassword.set('la contraseña debe tener como minimo 8 caracteres');
        }
        else{
          this.errorMessagePassword.set('');
        }
  
        break;
      default:
        break;
    }
    }
  
}
