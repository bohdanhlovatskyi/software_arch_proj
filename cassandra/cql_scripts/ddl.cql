CREATE KEYSPACE software_arch_proj WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 2 };

USE software_arch_proj;

CREATE TABLE image_metadata (
    user_id text, 
    img_id text, 
    img_path text, 
    img_description text, 
    PRIMARY KEY ((user_id), img_id)
);
