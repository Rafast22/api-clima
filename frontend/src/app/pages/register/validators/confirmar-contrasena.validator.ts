import {
    AbstractControl,
    ValidationErrors,
    ValidatorFn,
  } from '@angular/forms';
  
  export const confirmPasswordValidator: ValidatorFn = (
    control: AbstractControl
  ): ValidationErrors | null => {
    if(!control.parent) return null;
    const password = control.parent.get("password")
    const confirmPassword = control.parent.get("confirmPassword")
    if(confirmPassword && password)
      return confirmPassword.value.contrasena === control.value.confirmContrasena ? null : { PasswordNoMatch: true };
    return null;
  };