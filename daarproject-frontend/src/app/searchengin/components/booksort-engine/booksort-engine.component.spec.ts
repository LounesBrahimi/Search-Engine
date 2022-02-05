import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BooksortEngineComponent } from './booksort-engine.component';

describe('BooksortEngineComponent', () => {
  let component: BooksortEngineComponent;
  let fixture: ComponentFixture<BooksortEngineComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BooksortEngineComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BooksortEngineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
