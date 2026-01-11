-- =========================
-- EXTENSIONS
-- =========================
create extension if not exists "uuid-ossp";

-- =========================
-- PROFILES (SUPABASE AUTH)
-- =========================
create table if not exists profiles (
  id uuid references auth.users on delete cascade primary key,
  email text,
  role text check (role in ('admin', 'user')) default 'user',
  created_at timestamptz default now()
);

create or replace function public.handle_new_user() 
returns trigger as $$
begin
  insert into public.profiles (id, email, role)
  values (new.id, new.email, 'user')
  on conflict (id) do nothing;
  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;

create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();


-- =========================
-- CLIENTS
-- =========================
create table if not exists clients (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  description text,
  projectCount int default 0,
  environmentCount int default 0,
  status text check (status in ('active', 'inactive', 'maintenance', 'warning')) default 'active',
  lastActivity timestamptz default now()
);

-- =========================
-- PROJECTS
-- =========================
create table if not exists projects (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  clientId uuid references clients(id) on delete cascade,
  description text,
  status text check (status in ('active', 'development', 'maintenance', 'planning')) default 'active',
  progress int default 0,
  lastDeployment timestamptz,
  repository text,
  technology text[],
  createdAt timestamptz default now()
);

-- =========================
-- ENVIRONMENTS
-- =========================
create table if not exists environments (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  projectId uuid references projects(id) on delete cascade,
  status text default 'active',
  health text default 'healthy',
  url text,
  lastDeployment timestamptz,
  version text,
  resources jsonb,
  services text[],
  uptime float default 100.0,
  createdAt timestamptz default now()
);

-- =========================
-- SERVERS
-- =========================
create table if not exists servers (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  environmentId uuid references environments(id) on delete cascade,
  type text,
  status text default 'running',
  cpu text,
  memory text,
  region text,
  privateIp text
);

-- =========================
-- MONITORS
-- =========================
create table if not exists monitors (
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

-- =========================
-- SECRETS
-- =========================
create table if not exists secrets (
  id uuid default uuid_generate_v4() primary key,
  key text not null,
  value text,
  environment text,
  lastUpdated timestamptz default now()
);

-- =========================
-- SETTINGS
-- =========================
create table if not exists settings (
  id uuid default uuid_generate_v4() primary key,
  key text unique not null,
  value text,
  description text
);

-- =========================
-- SEED DATA (UUID SAFE)
-- =========================

-- Clients
insert into clients (name, description, status) values 
('Acme Corp', 'Global enterprise solutions', 'active'),
('TechStart', 'Cutting edge startup', 'active'),
('GlobalFinance', 'Financial services', 'warning'),
('EduTech', 'Education platform', 'maintenance'),
('HealthPlus', 'Healthcare systems', 'active');

-- Projects
insert into projects (name, clientId, description, status, progress, technology) values
('Client Portal', (select id from clients where name='Acme Corp'), 'Customer facing portal', 'active', 75, ARRAY['React', 'Node.js']),
('Admin Dashboard', (select id from clients where name='TechStart'), 'Internal admin tool', 'development', 40, ARRAY['Vue', 'Python']),
('Mobile App API', (select id from clients where name='GlobalFinance'), 'API for mobile application', 'active', 90, ARRAY['Go', 'gRPC']);

-- Environments
insert into environments (name, projectId, status, health, url, resources) values
('Production', (select id from projects where name='Client Portal'), 'active', 'healthy', 'https://portal.acme.com', '{"cpu":"45%","memory":"2.4GB","storage":"120GB"}'),
('Staging', (select id from projects where name='Client Portal'), 'active', 'warning', 'https://staging.portal.acme.com', '{"cpu":"15%","memory":"1.2GB","storage":"40GB"}'),
('Dev', (select id from projects where name='Admin Dashboard'), 'active', 'healthy', 'https://dev.dashboard.techstart.io', '{"cpu":"5%","memory":"512MB","storage":"10GB"}');

-- Servers
insert into servers (name, environmentId, type, status, cpu, memory, region, privateIp) values
('web-prod-01', (select id from environments where name='Production'), 'EC2', 'running', '45%', '2.4GB', 'us-east-1', '10.0.1.12'),
('db-prod-01', (select id from environments where name='Production'), 'RDS', 'running', '60%', '8GB', 'us-east-1', '10.0.2.15'),
('web-staging-01', (select id from environments where name='Staging'), 'EC2', 'running', '15%', '1.2GB', 'us-east-1', '10.0.1.22');

-- Monitors
insert into monitors (name, url, status, responseTime) values
('Acme Portal', 'https://portal.acme.com', 'up', 120),
('TechStart API', 'https://api.techstart.io', 'up', 85),
('Internal Admin', 'https://admin.globalfinance.com', 'down', 0);

-- Secrets
insert into secrets (key, value, environment) values
('AWS_ACCESS_KEY', 'AKIA................', 'Production'),
('DB_PASSWORD', 'supersecret', 'Staging');

-- Settings
insert into settings (key, value, description) values
('site_name', 'DragonOps', 'Application Name'),
('maintenance_mode', 'false', 'Enable maintenance mode'),
('allow_signup', 'true', 'Allow new user registration')
on conflict (key) do nothing;
