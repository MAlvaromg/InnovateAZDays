import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TaskService } from './task.service';
import { Task } from './task.model';

@Component({
  selector: 'app-taskmanager',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './taskmanager.component.html',
  styleUrls: ['./taskmanager.component.css']
})
export class TaskManagerComponent implements OnInit {
  tasks: Task[] = [];
  newTask: Task = { id: '', name: '', description: '', done: false };

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.loadTasks();
  }

  loadTasks(): void {
    this.taskService.getTasks().subscribe((tasks) => (this.tasks = tasks));
  }

  addTask(): void {
    if (this.newTask.name && this.newTask.description) {
      this.taskService.createTask(this.newTask).subscribe((task) => {
        this.tasks.push(task);
        this.newTask = { id: '', name: '', description: '', done: false };
      });
    }
  }

  updateTask(task: Task): void {
    this.taskService.updateTask(task).subscribe();
  }

  deleteTask(id: string): void {
    this.taskService.deleteTask(id).subscribe(() => {
      this.tasks = this.tasks.filter((task) => task.id !== id);
    });
  }
}
