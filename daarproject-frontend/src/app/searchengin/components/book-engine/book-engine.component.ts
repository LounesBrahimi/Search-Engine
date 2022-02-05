import { Component, Input, OnInit } from '@angular/core';
import { Book } from '../../models/book';
import { BookEngineServicesService } from '../../services/book-engine-services.service'

@Component({
  selector: 'app-book-engine',
  templateUrl: './book-engine.component.html',
  styleUrls: ['./book-engine.component.scss']
})
export class BookEngineComponent implements OnInit {

  books : Book[] = [];
  suggestions : Book[] = [];
  @Input() word:string = "";

  constructor(private searchenginService:BookEngineServicesService) {}

  ngOnInit(): void {
   //
  }

  onSubmit(): void {
		console.log("mot recherché : "+this.word); 
    this.searchenginService.getBooksByWord(this.word)
                           .subscribe(result => {
                              console.log(result.books)
                              console.log(result.suggestions)
                              this.books = result.books ;
                              this.suggestions = result.suggestions ; 
                            })
  }

}
