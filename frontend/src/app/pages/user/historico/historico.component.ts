import { AfterViewInit, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { HistoricoService } from '../../../services/historico/historico.service';
import { MatTableModule } from '@angular/material/table';
import { CommonModule } from '@angular/common';
import { Historico } from '../../../models/historico';
export interface HistoricoData{}
@Component({
  selector: 'app-historico',
  standalone: true,
  imports: [MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,CommonModule,
    MatTableModule],
  templateUrl: './historico.component.html',
  styleUrl: './historico.component.css'
})
export class HistoricoComponent implements AfterViewInit {
  readonly dialogRef = inject(MatDialogRef<HistoricoComponent>);
  readonly data = inject<HistoricoData>(MAT_DIALOG_DATA);
  readonly service = inject(HistoricoService);
  displayedColumns: string[] = ['id', 'nome', 'preco'];
  dataSource: Historico[] = [];
  constructor(){}
  ngAfterViewInit(): void {
    this.service.getHistorico(1, 50).subscribe( r => this.dataSource = r)
  }
  onNoClick(): void {
    this.dialogRef.close();
  }

}
