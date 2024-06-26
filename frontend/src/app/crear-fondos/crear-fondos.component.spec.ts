import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CrearFondosComponent } from './crear-fondos.component';

describe('CrearFondosComponent', () => {
  let component: CrearFondosComponent;
  let fixture: ComponentFixture<CrearFondosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CrearFondosComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CrearFondosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
