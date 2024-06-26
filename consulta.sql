SELECT DISTINCT c.nombre, c.apellidos,c.ciudad 
FROM cliente c
JOIN inscripcion i ON c.id = i.idCliente
JOIN producto p ON i.idProducto= p.id
JOIN disponibilidad d ON p.idProducto = d.idProducto
JOIN sucursal s ON d.idSucursal = s.id
JOIN visitan v ON c.id = v.idCliente AND s.id = v.idSucursal
WHERE NOT EXISTS (
    SELECT 1
    FROM disponibilidad d2
    WHERE d2.idProducto = p.id
      AND d2.idSucursal NOT IN (
          SELECT s2.id
          FROM sucursal s2
          JOIN disponibilidad d3 ON s2.id = d3.idSucursal
          WHERE d3.idProducto = p.id
      )
);


Selección de Columnas:

SELECT DISTINCT c.nombre, c.apellidos,c.ciudad 
Condición NOT EXISTS:

WHERE NOT EXISTS (...):
Se utiliza para asegurarse de que no existan otras sucursales donde el producto esté disponible y que el cliente no visita. Esto garantiza que el producto esté disponible solo en las sucursales que el cliente visita y donde el producto específico está disponible.

Subconsultas:

SELECT s2.id FROM sucursal s2 JOIN disponibilidad d3 ON s2.id = d3.idSucursal WHERE d3.idProducto = p.id: 
Subconsulta para obtener las sucursales que ofrecen el mismo producto (p.id) que el cliente ha inscrito.