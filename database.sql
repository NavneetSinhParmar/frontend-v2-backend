-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Profiles Table (links to auth.users)
create table profiles (
  id uuid references auth.users on delete cascade primary key,
  email text,
  role text check (role in ('admin', 'user')) default 'user',
  created_at timestamptz default now()
);

-- Trigger to create profile on signup
create or replace function public.handle_new_user() 
returns trigger as $$
begin
  insert into public.profiles (id, email, role)
  values (new.id, new.email, 'user');
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Clients Table
create table clients (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  description text,
  projectCount int default 0,
  environmentCount int default 0,
  status text check (status in ('active', 'inactive', 'maintenance')) default 'active',
  lastActivity timestamptz default now()
);

-- Projects Table
create table projects (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  clientId uuid references clients(id),
  description text,
  status text check (status in ('active', 'development', 'maintenance', 'planning')) default 'active',
  progress int default 0,
  lastDeployment timestamptz,
  repository text,
  technology text[],
  createdAt timestamptz default now()
);

-- Environments Table
create table environments (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  projectId uuid references projects(id),
  status text default 'active',
  health text default 'healthy',
  url text,
  lastDeployment timestamptz,
  version text,
  resources jsonb, -- {cpu, memory, storage}
  services text[],
  uptime float default 100.0,
  createdAt timestamptz default now()
);

-- Servers Table
create table servers (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  environmentId uuid references environments(id),
  type text, -- EC2, RDS, etc.
  status text default 'running',
  cpu text,
  memory text,
  region text,
  privateIp text
);

-- Monitors Table
create table monitors (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  url text not null,
  status text default 'up',
  responseTime float,
  uptime float default 100.0,
  lastCheck timestamptz default now(),
  incidents int default 0,
  downtimeToday text default '0m'
);

-- Seed Data (Mock Data)

-- Clients
INSERT INTO clients (id, name, description, status) VALUES 
('c0a80121-7ac0-4cf5-9b2f-7640c0f0d231', 'Acme Corp', 'Global enterprise solutions', 'active'),
('c0a80121-7ac0-4cf5-9b2f-7640c0f0d232', 'TechStart', 'Cutting edge startup', 'active'),
('c0a80121-7ac0-4cf5-9b2f-7640c0f0d233', 'GlobalFinance', 'Financial services', 'warning'),
('c0a80121-7ac0-4cf5-9b2f-7640c0f0d234', 'EduTech', 'Education platform', 'maintenance'),
('c0a80121-7ac0-4cf5-9b2f-7640c0f0d235', 'HealthPlus', 'Healthcare systems', 'active');

-- Secrets Table
create table secrets (
  id uuid default uuid_generate_v4() primary key,
  key text not null,
  value text,
  environment text,
  lastUpdated timestamptz default now()
);

-- Settings Table
create table settings (
  id uuid default uuid_generate_v4() primary key,
  key text unique not null,
  value text,
  description text
);

-- Secrets Data
INSERT INTO secrets (key, value, environment) VALUES
('AWS_ACCESS_KEY', 'AKIA................', 'Production'),
('DB_PASSWORD', 'supersecret', 'Staging');

-- Settings Data
INSERT INTO settings (key, value, description) VALUES
('site_name', 'DragonOps', 'Application Name'),
('maintenance_mode', 'false', 'Enable maintenance mode'),
('allow_signup', 'true', 'Allow new user registration');

-- Projects
INSERT INTO projects (id, name, clientId, description, status, progress, technology) VALUES
('p0a80121-7ac0-4cf5-9b2f-7640c0f0d331', 'Client Portal', 'c0a80121-7ac0-4cf5-9b2f-7640c0f0d231', 'Customer facing portal', 'active', 75, ARRAY['React', 'Node.js']),
('p0a80121-7ac0-4cf5-9b2f-7640c0f0d332', 'Admin Dashboard', 'c0a80121-7ac0-4cf5-9b2f-7640c0f0d232', 'Internal admin tool', 'development', 40, ARRAY['Vue', 'Python']),
('p0a80121-7ac0-4cf5-9b2f-7640c0f0d333', 'Mobile App API', 'c0a80121-7ac0-4cf5-9b2f-7640c0f0d233', 'API for mobile application', 'active', 90, ARRAY['Go', 'gRPC']);

-- Environments
INSERT INTO environments (id, name, projectId, status, health, url, resources) VALUES
('e0a80121-7ac0-4cf5-9b2f-7640c0f0d431', 'Production', 'p0a80121-7ac0-4cf5-9b2f-7640c0f0d331', 'active', 'healthy', 'https://portal.acme.com', '{"cpu": "45%", "memory": "2.4GB", "storage": "120GB"}'),
('e0a80121-7ac0-4cf5-9b2f-7640c0f0d432', 'Staging', 'p0a80121-7ac0-4cf5-9b2f-7640c0f0d331', 'active', 'warning', 'https://staging.portal.acme.com', '{"cpu": "15%", "memory": "1.2GB", "storage": "40GB"}'),
('e0a80121-7ac0-4cf5-9b2f-7640c0f0d433', 'Dev', 'p0a80121-7ac0-4cf5-9b2f-7640c0f0d332', 'active', 'healthy', 'https://dev.dashboard.techstart.io', '{"cpu": "5%", "memory": "512MB", "storage": "10GB"}');

-- Servers
INSERT INTO servers (name, environmentId, type, status, cpu, memory, region, privateIp) VALUES
('web-prod-01', 'e0a80121-7ac0-4cf5-9b2f-7640c0f0d431', 'EC2', 'running', '45%', '2.4GB', 'us-east-1', '10.0.1.12'),
('db-prod-01', 'e0a80121-7ac0-4cf5-9b2f-7640c0f0d431', 'RDS', 'running', '60%', '8GB', 'us-east-1', '10.0.2.15'),
('web-staging-01', 'e0a80121-7ac0-4cf5-9b2f-7640c0f0d432', 'EC2', 'running', '15%', '1.2GB', 'us-east-1', '10.0.1.22');

-- Monitors
INSERT INTO monitors (name, url, status, responseTime) VALUES
('Acme Portal', 'https://portal.acme.com', 'up', 120),
('TechStart API', 'https://api.techstart.io', 'up', 85),
('Internal Admin', 'https://admin.globalfinance.com', 'down', 0);
