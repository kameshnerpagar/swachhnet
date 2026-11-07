-- 001_init_schema.sql
-- Relational PostgreSQL schema for SwachhNet Municipal Garbage System

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(32) NOT NULL CHECK (role IN ('user', 'admin', 'worker', 'superadmin')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ward_authorities (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    address TEXT DEFAULT '',
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    rating_score NUMERIC(3, 2) DEFAULT 0.0,
    rating_count INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS workers (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    truck_number VARCHAR(64) NOT NULL,
    assigned_ward_id UUID REFERENCES users(id) ON DELETE SET NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    status VARCHAR(32) DEFAULT 'idle' CHECK (status IN ('idle', 'busy'))
);

CREATE TABLE IF NOT EXISTS complaints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_name VARCHAR(255),
    authority_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    worker_id UUID REFERENCES users(id) ON DELETE SET NULL,
    s3_key VARCHAR(512) NOT NULL,
    image_url TEXT,
    after_s3_key VARCHAR(512),
    after_image_url TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    address TEXT DEFAULT '',
    status VARCHAR(32) DEFAULT 'open' CHECK (status IN ('open', 'assigned', 'pending_verification', 'resolved', 'rejected')),
    description TEXT DEFAULT '',
    rating INT CHECK (rating >= 1 AND rating <= 5),
    rating_comment TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS complaint_transfers (
    id BIGSERIAL PRIMARY KEY,
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    from_authority_name VARCHAR(255),
    to_authority_name VARCHAR(255),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Performance and Query Indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_complaints_user ON complaints(user_id);
CREATE INDEX IF NOT EXISTS idx_complaints_authority ON complaints(authority_id);
CREATE INDEX IF NOT EXISTS idx_complaints_worker ON complaints(worker_id);
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);
CREATE INDEX IF NOT EXISTS idx_complaints_created_at ON complaints(created_at);
CREATE INDEX IF NOT EXISTS idx_workers_ward_status ON workers(assigned_ward_id, status);

