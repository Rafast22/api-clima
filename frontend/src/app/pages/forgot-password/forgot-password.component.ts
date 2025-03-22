import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, inject, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { AuthService } from '../../services/auth/auth.service';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';

interface RescuePassword{
  Email:String
}

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogContent,
    MatDialogClose,
    MatIconModule,
  MatCardModule, ReactiveFormsModule, CommonModule],
  templateUrl: './forgot-password.component.html',
  styleUrl: './forgot-password.component.css'
})
export class ForgotPasswordComponent implements AfterViewInit{
  // readonly dialogRef = inject(MatDialogRef<ForgotPasswordComponent>);
  // readonly data = inject<RescuePassword>(MAT_DIALOG_DATA);
  @ViewChild('email') CampoEmail: any = undefined;
  
  recuperarSenhaForm: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService, private router:Router) {
    this.recuperarSenhaForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });
   }

   ngAfterViewInit(): void {
    setTimeout(() => {
      this.CampoEmail.nativeElement.elements[0].focus()
    }, 100);
   }

  onNoClick(): void {
    // this.dialogRef.close();
  }

  onSubmit() {
    if (this.recuperarSenhaForm.valid) {
      const email = this.recuperarSenhaForm.value.email;
      // this.authService.recuperarCOntrase
      // this.http.post('http://localhost:8000/recuperar-senha', { email }).subscribe({
      //   next: () => {
      //     this.snackBar.open('Um email de recuperação foi enviado.', 'Fechar', {
      //       duration: 3000
      //     });
      //   },
      //   error: () => {
      //     this.snackBar.open('Erro ao enviar email de recuperação.', 'Fechar', {
      //       duration: 3000
      //     });
      //   }
      // });
    }
  }

  backToLogin(){
    this.router.navigateByUrl("login")
  }

}

