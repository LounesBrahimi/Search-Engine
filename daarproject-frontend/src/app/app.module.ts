import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BookEngineComponent } from './searchengin/components/book-engine/book-engine.component';
import { BookEngineServicesService } from './searchengin/services/book-engine-services.service';
import { BooksortEngineComponent } from './searchengin/components/booksort-engine/booksort-engine.component';

@NgModule({
  declarations: [
    AppComponent,
    BookEngineComponent,
    BooksortEngineComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [BookEngineServicesService],
  bootstrap: [AppComponent]
})
export class AppModule { }
