package com.api.ejemplo.apidocker.model;

import com.amazonaws.services.dynamodbv2.datamodeling.*;
//import lombok.Data;

import java.util.List;

//@Data
@DynamoDBTable(tableName = "Clientes") // Nombre de la tabla en DynamoDB
public class Cliente {

    @DynamoDBAutoGeneratedKey
    @DynamoDBHashKey(attributeName = "Id")
    private String id;

    @DynamoDBAttribute(attributeName = "Nombres")
    private String nombres;

    @DynamoDBAttribute(attributeName = "Apellidos")
    private String apellidos;

    @DynamoDBAttribute(attributeName = "tipoIdentificacion")
    private String tipoIdentificacion;

    @DynamoDBAttribute(attributeName = "numeroIdentificacion")
    private String numeroIdentificacion;

    @DynamoDBAttribute(attributeName = "Email")
    private String email;

    @DynamoDBAttribute(attributeName = "Telefono")
    private String telefono;

    @DynamoDBAttribute(attributeName = "saldoActual")
    private double saldoActual;

    @DynamoDBAttribute(attributeName = "fondosSuscritos")
    private List<FondoSuscrito> fondosSuscritos;

    @DynamoDBAttribute(attributeName = "historialTransacciones")
    private List<Transaccion> historialTransacciones;

    @DynamoDBAttribute(attributeName = "preferenciaNotificacion")
    private String preferenciaNotificacion;

    // Getters y Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getNombres() {
        return nombres;
    }

    public void setNombres(String nombres) {
        this.nombres = nombres;
    }

    public String getApellidos() {
        return apellidos;
    }

    public void setApellidos(String apellidos) {
        this.apellidos = apellidos;
    }

    public String getTipoIdentificacion() {
        return tipoIdentificacion;
    }

    public void setTipoIdentificacion(String tipoIdentificacion) {
        this.tipoIdentificacion = tipoIdentificacion;
    }

    public String getNumeroIdentificacion() {
        return numeroIdentificacion;
    }

    public void setNumeroIdentificacion(String numeroIdentificacion) {
        this.numeroIdentificacion = numeroIdentificacion;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getTelefono() {
        return telefono;
    }

    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }

    public double getSaldoActual() {
        return saldoActual;
    }

    public void setSaldoActual(double saldoActual) {
        this.saldoActual = saldoActual;
    }

    public List<FondoSuscrito> getFondosSuscritos() {
        return fondosSuscritos;
    }

    public void setFondosSuscritos(List<FondoSuscrito> fondosSuscritos) {
        this.fondosSuscritos = fondosSuscritos;
    }

    public List<Transaccion> getHistorialTransacciones() {
        return historialTransacciones;
    }

    public void setHistorialTransacciones(List<Transaccion> historialTransacciones) {
        this.historialTransacciones = historialTransacciones;
    }

    public String getPreferenciaNotificacion() {
        return preferenciaNotificacion;
    }

    public void setPreferenciaNotificacion(String preferenciaNotificacion) {
        this.preferenciaNotificacion = preferenciaNotificacion;
    }
}