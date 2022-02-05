import { TestBed } from '@angular/core/testing';

import { BookEngineServicesService } from './book-engine-services.service';

describe('BookEngineServicesService', () => {
  let service: BookEngineServicesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BookEngineServicesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
