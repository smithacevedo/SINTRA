-- Scripts para crear permisos y roles

-- Insertar permisos
INSERT INTO permisos_permiso (nombre, llave) VALUES
('Ver Dashboard', 'ver_dashboard'),
('Ver Productos', 'ver_productos'),
('Crear Productos', 'crear_productos'),
('Editar Productos', 'editar_productos'),
('Eliminar Productos', 'eliminar_productos'),
('Ver Clientes', 'ver_clientes'),
('Crear Clientes', 'crear_clientes'),
('Editar Clientes', 'editar_clientes'),
('Eliminar Clientes', 'eliminar_clientes'),
('Ver Pedidos', 'ver_pedidos'),
('Crear Pedidos', 'crear_pedidos'),
('Editar Pedidos', 'editar_pedidos'),
('Eliminar Pedidos', 'eliminar_pedidos'),
('Ver Despachos', 'ver_despachos'),
('Crear Despachos', 'crear_despachos'),
('Editar Despachos', 'editar_despachos'),
('Ver Remisiones', 'ver_remisiones'),
('Crear Remisiones', 'crear_remisiones'),
('Editar Remisiones', 'editar_remisiones'),
('Ver Usuarios', 'ver_usuarios'),
('Crear Usuarios', 'crear_usuarios'),
('Editar Usuarios', 'editar_usuarios'),
('Eliminar Usuarios', 'eliminar_usuarios'),
('Ver Roles', 'ver_roles'),
('Crear Roles', 'crear_roles'),
('Editar Roles', 'editar_roles'),
('Eliminar Roles', 'eliminar_roles'),
('Ver Permisos', 'ver_permisos'),
('Crear Permisos', 'crear_permisos'),
('Editar Permisos', 'editar_permisos'),
('Eliminar Permisos', 'eliminar_permisos');

-- Insertar roles
INSERT INTO roles_rol (nombre) VALUES
('Administrador'),
('Gerente'),
('Operador'),
('Consultor');

-- Asignar todos los permisos al rol Administrador
INSERT INTO roles_rol_permisos (rol_id, permiso_id)
SELECT 1, id FROM permisos_permiso;

-- Asignar permisos al rol Gerente
INSERT INTO roles_rol_permisos (rol_id, permiso_id)
SELECT 2, id FROM permisos_permiso 
WHERE llave IN ('ver_dashboard', 'ver_productos', 'crear_productos', 'editar_productos', 
                'ver_clientes', 'crear_clientes', 'editar_clientes',
                'ver_pedidos', 'crear_pedidos', 'editar_pedidos');

-- Asignar permisos al rol Operador
INSERT INTO roles_rol_permisos (rol_id, permiso_id)
SELECT 3, id FROM permisos_permiso 
WHERE llave IN ('ver_dashboard', 'ver_despachos', 'crear_despachos', 'editar_despachos',
                'ver_remisiones', 'crear_remisiones', 'editar_remisiones');

-- Asignar permisos al rol Consultor
INSERT INTO roles_rol_permisos (rol_id, permiso_id)
SELECT 4, id FROM permisos_permiso 
WHERE llave IN ('ver_dashboard', 'ver_productos', 'ver_clientes', 'ver_pedidos', 
                'ver_despachos', 'ver_remisiones');

-- NOTA: El usuario administrador se crea con el script Python crear_admin.py
-- No crear usuario aquí porque el hash de contraseña debe ser generado por Django