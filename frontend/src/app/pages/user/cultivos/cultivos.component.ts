import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

export interface CultivosData { }

@Component({
  selector: 'app-cultivos',
  standalone: true,
  imports: [MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose],
  templateUrl: './cultivos.component.html',
  styleUrl: './cultivos.component.css'
})
export class CultivosComponent {
  readonly dialogRef = inject(MatDialogRef<CultivosComponent>);
  readonly data = inject<CultivosData>(MAT_DIALOG_DATA);

  constructor() { }

  onNoClick(): void {
    this.dialogRef.close();
  }
}
