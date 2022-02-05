import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookEngineComponent } from './book-engine.component';

describe('BookEngineComponent', () => {
  let component: BookEngineComponent;
  let fixture: ComponentFixture<BookEngineComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BookEngineComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BookEngineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
