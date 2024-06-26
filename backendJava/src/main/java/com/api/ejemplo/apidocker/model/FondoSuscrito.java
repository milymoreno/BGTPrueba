package com.api.ejemplo.apidocker.model;

import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBAttribute;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBDocument;
//import lombok.Data;

//@Data
@DynamoDBDocument
public class FondoSuscrito {

    
    @DynamoDBAttribute(attributeName = "fondoId")
    private String fondoId;

    @DynamoDBAttribute(attributeName = "montoSuscrito")
    private double montoSuscrito;

    @DynamoDBAttribute(attributeName = "fechaSuscripcion")
    private String fechaSuscripcion; // Debe ser un String formateado como ISO 8601

  

    // Getters y Setters
    public String getFondoId() {
        return fondoId;
    }

    public void setFondoId(String fondoId) {
        this.fondoId = fondoId;
    }

    public double getMontoSuscrito() {
        return montoSuscrito;
    }

    public void setMontoSuscrito(double montoSuscrito) {
        this.montoSuscrito = montoSuscrito;
    }

    public String getFechaSuscripcion() {
        return fechaSuscripcion;
    }

    public void setFechaSuscripcion(String fechaSuscripcion) {
        this.fechaSuscripcion = fechaSuscripcion;
    }
}
