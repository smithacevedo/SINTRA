-- Arreglar secuencia de auth_user
SELECT setval('auth_user_id_seq', (SELECT MAX(id) FROM auth_user) + 1);