import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable} from 'rxjs';
import { tap } from 'rxjs/operators';
import { Book } from '../models/book';

@Injectable({
  providedIn: 'root'
})
export class BookEngineServicesService {

  private urlBooks:string = "Books"          // http://127.0.0.1:8000/Books/
  private urlSearch:string = "Books/Search"  // http://127.0.0.1:8000/Books/Search/

  constructor(private http: HttpClient) { 

  }

  getBooks(): Observable<Book[]> {
		var result:Observable<Book[]> =  this.http.get<Book[]>(this.urlBooks+"/getAllBooks/");
      return result ; 
	}

  getBooksByWord(word:string): Observable<any> {
    const url = `${this.urlSearch}/${word}`;

    return this.http.get<Object>(url).pipe(
      tap (
          success => console.log('success response'),
          error => console.log('error')
       ), 
    );
	}


}
