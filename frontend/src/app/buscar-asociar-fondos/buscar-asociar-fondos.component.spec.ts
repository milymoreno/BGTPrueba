import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BuscarAsociarFondosComponent } from './buscar-asociar-fondos.component';

describe('BuscarAsociarFondosComponent', () => {
  let component: BuscarAsociarFondosComponent;
  let fixture: ComponentFixture<BuscarAsociarFondosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BuscarAsociarFondosComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BuscarAsociarFondosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
