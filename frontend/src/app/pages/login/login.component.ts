import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormsModule, NgModel, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { HttpClientModule } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';
import { UserService } from '../../services/user/user.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule, MatIconModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  providers:[UserService]
})
export class LoginComponent implements OnInit {
  formLogar! : FormGroup;
  mensagemErro = "";
  submetido = false;

  public email:string = '';
  public password:string = '';
  
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
   }
  

  ngOnInit(): void {
    this.formLogar = this.fb.group({
      username: ['',[ Validators.required]],
      password: ['', [Validators.required]]
    })
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
