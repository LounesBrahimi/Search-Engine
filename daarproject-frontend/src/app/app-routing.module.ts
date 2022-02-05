import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BookEngineComponent } from './searchengin/components/book-engine/book-engine.component';

const routes: Routes = [ 
	{
		path: 'books engine',
		children: [
      { path: '', redirectTo: 'home', pathMatch: 'full'},
      { path: 'home'  , component: BookEngineComponent}
		]
	}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
