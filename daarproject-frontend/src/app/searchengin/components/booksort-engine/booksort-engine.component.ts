import { Component, Input, OnInit } from '@angular/core';
import { Book } from '../../models/book';

@Component({
  selector: 'booksort-engine',
  templateUrl: './booksort-engine.component.html',
  styleUrls: ['./booksort-engine.component.scss']
})
export class BooksortEngineComponent implements OnInit {

  @Input() books: Book [] = [];
  constructor() { }

  ngOnInit(): void {
  }

  onBookSort(type: string): any {
    if (type == 'pertinent'){
      this.books.sort((b1,b2) => {
          if (b1.rank == b2.rank) {
            return 0;
          }else if (b1.rank > b2.rank) {
              return -1;
          }else { 
              return 1;
          }
      });

    }else if(type == 'title'){
      this.books.sort((b1,b2) => {
        if (b1.title == b2.title) {
          return 0;
        }else if (b1.title > b2.title) {
          return 1;
        }else { 
          return -1;
        }
      });
    }
  }

}
