#!/bin/bash

# Removing sqlite3 database
rm -rf db.sqlite3

# Clearing config cache
rm -rf config/__pycache__

# Clearing config.settings cache
rm -rf config/settings/__pycache__

# Clearing apps cache
rm -rf apps/__pycache__

# Clearing apps.authentication cache
rm -rf apps/authentication/__pycache__
rm -rf apps/authentication/migrations/__pycache__
rm -rf apps/authentication/migrations/0*

# Clearing apps.dashboard cache
rm -rf apps/dashboard/__pycache__
rm -rf apps/dashboard/migrations/__pycache__
rm -rf apps/dashboard/migrations/0*

# Clearing apps.cadastro cache
rm -rf apps/cadastro/__pycache__

# Clearing apps.cadastro.policiais cache
rm -rf apps/cadastro/policiais/__pycache__
rm -rf apps/cadastro/policiais/migrations/__pycache__
rm -rf apps/cadastro/policiais/migrations/0*

# Clearing apps.cadastro.complementos cache
rm -rf apps/cadastro/complementos/__pycache__
rm -rf apps/cadastro/complementos/migrations/__pycache__
rm -rf apps/cadastro/complementos/migrations/0*
