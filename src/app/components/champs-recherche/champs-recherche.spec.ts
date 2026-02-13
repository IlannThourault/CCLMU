import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChampsRecherches } from './champs-recherches';

describe('ChampsRecherches', () => {
  let component: ChampsRecherches;
  let fixture: ComponentFixture<ChampsRecherches>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChampsRecherches]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChampsRecherches);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
