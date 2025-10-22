-- Script para limpiar TODAS las tablas de permisos, roles y usuarios

-- Eliminar todas las relaciones usuario-rol
DELETE FROM usuario_rol;

-- Eliminar todos los perfiles de usuario
DELETE FROM perfil_usuario;

-- Eliminar todas las relaciones roles-permisos
DELETE FROM roles_rol_permisos;

-- Eliminar todos los roles
DELETE FROM roles_rol;

-- Eliminar todos los permisos
DELETE FROM permisos_permiso;

-- Eliminar todos los usuarios (excepto superusuarios si existen)
DELETE FROM auth_user WHERE is_superuser = false;

-- Reiniciar secuencias
ALTER SEQUENCE permisos_permiso_id_seq RESTART WITH 1;
ALTER SEQUENCE roles_rol_id_seq RESTART WITH 1;
ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;