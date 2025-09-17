# Redis Configuration for Squirll Multi-Environment Setup

## Overview

This document outlines the Redis configuration for the Squirll backend using Azure Redis Cache across Development and UAT environments.

## Environment Configurations

### Development Environment (rg-squirll-dev-015)
- **Resource Group**: `rg-squirll-dev-015`
- **Redis Instance**: `redis-squirll-dev-015`
- **Hostname**: `redis-squirll-dev-015.redis.cache.windows.net`
- **App Services**: 
  - `app-squirll-services-dev-015`
- **SKU**: `Basic C0`

### UAT Environment (rg-squirll-uat-015)
- **Resource Group**: `rg-squirll-uat-015`
- **Redis Instance**: `redis-squirll-uat-rdy`
- **Hostname**: `redis-squirll-uat-rdy.redis.cache.windows.net`
- **App Services**: 
  - `app-squirll-services-uat-rdy`
  - `app-squirll-services-uat-001`
- **SKU**: `Standard C1` (with replication)

### Common Configuration
- **SSL Port**: `6380` (recommended for production)
- **Non-SSL Port**: `6379` (disabled for security)
- **Redis Version**: `6.0`
- **Minimum TLS Version**: `1.2`

## Environment Variables Required

Environment variables are set per environment and automatically applied during deployment.

### Development Environment (.env.development)
```bash
# Azure Redis Configuration (rg-squirll-dev-015)
REDIS_HOST=redis-squirll-dev-015.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=gFU9zHfMl3iJH6clZICRsdfQZohqj7thzAzCaIfECNY=
```

### UAT Environment (.env.uat)
```bash
# Azure Redis Configuration (rg-squirll-uat-015)
REDIS_HOST=redis-squirll-uat-rdy.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=OyYwKwX8BIumF9x9q5EWxB1wxKP4rdkRtAzCaM6Lyyw=
```

### Production Environment (Future)
```bash
# Azure Redis Configuration (to be configured)
REDIS_HOST=redis-squirll-prod-xxx.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=your-production-redis-password
```

## Required Python Packages

The following packages have been added to `requirements.txt`:

- `redis==6.2.0` - Redis Python client
- `channels-redis==4.2.1` - Redis channel layer for Django Channels
- `django-redis==5.4.0` - Django Redis cache backend

## Django Settings Configuration

### Development Environment (`development.py`)

The development settings now conditionally use Redis when environment variables are provided:

- **With Redis variables**: Uses Azure Redis for caching and WebSocket channels
- **Without Redis variables**: Falls back to in-memory alternatives for local development

### Production Environment (`production.py`)

Production settings require Redis and will raise an error if Redis environment variables are not set.

### Staging Environment (`staging.py`)

Staging continues to use in-memory alternatives, inheriting from production but overriding Redis settings.

## What Redis is Used For

1. **Django Channels**: WebSocket channel layer for real-time notifications
2. **Django Cache**: Application-level caching for improved performance
3. **Session Storage**: Can be configured for Redis-based sessions (future enhancement)

## Testing the Configuration

To test if Redis is working correctly:

1. Set the environment variables in your `.env` file
2. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
3. Check the logs for any Redis connection errors
4. Test WebSocket functionality through the frontend

## Database Configuration

Redis uses two separate databases:
- **Database 0**: Django Channels (WebSocket communication)
- **Database 1**: Django Cache (application caching)

## Security Notes

- SSL/TLS is enforced (port 6380)
- Access keys are used for authentication
- Non-SSL port (6379) is disabled
- Minimum TLS version is 1.2

## Troubleshooting

### Common Issues

1. **Connection Timeout**: Check if Redis host and port are correct
2. **Authentication Failed**: Verify Redis password is correct
3. **SSL Errors**: Ensure you're using port 6380 and `ssl_cert_reqs=none` parameter

### Testing Redis Connection

```python
import redis
import os

# Test connection
client = redis.Redis(
    host='redis-squirll-dev-015.redis.cache.windows.net',
    port=6380,
    password='gFU9zHfMl3iJH6clZICRsdfQZohqj7thzAzCaIfECNY=',
    ssl=True,
    ssl_cert_reqs=None
)

# Test basic operations
client.set('test_key', 'test_value')
print(client.get('test_key'))
```

## Next Steps for UAT Environment

For UAT deployment, you'll need to:

1. Get Redis configuration for UAT resource group
2. Update environment variables for UAT environment
3. Ensure production settings work with UAT Redis instance

## References

- [Django Channels Redis](https://channels-redis.readthedocs.io/)
- [Django Redis Cache](https://django-redis.readthedocs.io/)
- [Azure Redis Cache Documentation](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/)
