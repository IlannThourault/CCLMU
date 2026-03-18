import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LogoSite } from './logo-site';

describe('LogoSite', () => {
  let component: LogoSite;
  let fixture: ComponentFixture<LogoSite>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LogoSite]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LogoSite);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
