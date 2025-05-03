import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

export interface SettingsData {}

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [MatFormFieldModule,
      MatInputModule,
      FormsModule,
      MatButtonModule,
      MatDialogTitle,
      MatDialogContent,
      MatDialogActions,
      MatDialogClose],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.css'
})
export class SettingsComponent {
  readonly dialogRef = inject(MatDialogRef<SettingsComponent>);
  readonly data = inject<SettingsData>(MAT_DIALOG_DATA);

  constructor(){}

  onNoClick(): void {
    this.dialogRef.close();
  }
}
