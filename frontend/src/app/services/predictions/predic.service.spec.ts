import { TestBed } from '@angular/core/testing';

import { PredicService } from './predic.service';

describe('PredicService', () => {
  let service: PredicService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PredicService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
