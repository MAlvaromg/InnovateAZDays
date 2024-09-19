import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TaskManagerComponent } from './taskmanager/taskmanager.component';
 
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [TaskManagerComponent, RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'scaffold';
}