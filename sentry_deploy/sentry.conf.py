from sentry.conf.server import *  # NOQA


def get_internal_network():
    import ctypes
    import fcntl
    import math
    import socket
    import struct

    iface = b"eth0"
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ifreq = struct.pack(b"16sH14s", iface, socket.AF_INET, b"\x00" * 14)

    try:
        ip = struct.unpack(
            b"!I", struct.unpack(b"16sH2x4s8x", fcntl.ioctl(sockfd, 0x8915, ifreq))[2]
        )[0]
        netmask = socket.ntohl(
            struct.unpack(b"16sH2xI8x", fcntl.ioctl(sockfd, 0x891B, ifreq))[2]
        )
    except IOError:
        return ()
    base = socket.inet_ntoa(struct.pack(b"!I", ip & netmask))
    netmask_bits = 32 - int(round(math.log(ctypes.c_uint32(~netmask).value + 1, 2), 1))
    return "{0:s}/{1:d}".format(base, netmask_bits)


INTERNAL_SYSTEM_IPS = (get_internal_network(),)

DATABASES = {
    "default": {
        "ENGINE": "sentry.db.postgres",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "postgres",
        "PORT": "",
    }
}

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = True

# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
# General #
###########

# Instruct Sentry that this install intends to be run by a single organization
# and thus various UI optimizations should be enabled.
SENTRY_SINGLE_ORGANIZATION = True

SENTRY_OPTIONS["system.event-retention-days"] = int(
    env("SENTRY_EVENT_RETENTION_DAYS", "90")
)

#########
# Redis #
#########

# Generic Redis configuration used as defaults for various things including:
# Buffers, Quotas, TSDB

SENTRY_OPTIONS["redis.clusters"] = {
    "default": {
        "hosts": {0: {"host": "redis", "password": "", "port": "6379", "db": "0"}}
    }
}

#########
# Queue #
#########

# See https://develop.sentry.dev/services/queue/ for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

rabbitmq_host = None
if rabbitmq_host:
    BROKER_URL = "amqp://{username}:{password}@{host}/{vhost}".format(
        username="guest", password="guest", host=rabbitmq_host, vhost="/"
    )
else:
    BROKER_URL = "redis://:{password}@{host}:{port}/{db}".format(
        **SENTRY_OPTIONS["redis.clusters"]["default"]["hosts"][0]
    )

#########
# Cache #
#########

# Sentry currently utilizes two separate mechanisms. While CACHES is not a
# requirement, it will optimize several high throughput patterns.

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": ["memcached:11211"],
        "TIMEOUT": 3600,
    }
}

# A primary cache is required for things such as processing events
SENTRY_CACHE = "sentry.cache.redis.RedisCache"

DEFAULT_KAFKA_OPTIONS = {
    "bootstrap.servers": "kafka:9092",
    "message.max.bytes": 50000000,
    "socket.timeout.ms": 1000,
}

SENTRY_EVENTSTREAM = "sentry.eventstream.kafka.KafkaEventStream"
SENTRY_EVENTSTREAM_OPTIONS = {"producer_configuration": DEFAULT_KAFKA_OPTIONS}

KAFKA_CLUSTERS["default"] = DEFAULT_KAFKA_OPTIONS

###############
# Rate Limits #
###############

# Rate limits apply to notification handlers and are enforced per-project
# automatically.

SENTRY_RATELIMITER = "sentry.ratelimits.redis.RedisRateLimiter"

##################
# Update Buffers #
##################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

SENTRY_BUFFER = "sentry.buffer.redis.RedisBuffer"

##########
# Quotas #
##########

# Quotas allow you to rate limit individual projects or the Sentry install as
# a whole.

SENTRY_QUOTAS = "sentry.quotas.redis.RedisQuota"

########
# TSDB #
########

# The TSDB is used for building charts as well as making things like per-rate
# alerts possible.

SENTRY_TSDB = "sentry.tsdb.redissnuba.RedisSnubaTSDB"

#########
# SNUBA #
#########

SENTRY_SEARCH = "sentry.search.snuba.EventsDatasetSnubaSearchBackend"
SENTRY_SEARCH_OPTIONS = {}
SENTRY_TAGSTORE_OPTIONS = {}

###########
# Digests #
###########

# The digest backend powers notification summaries.

SENTRY_DIGESTS = "sentry.digests.backends.redis.RedisBackend"

##############
# Web Server #
##############

SENTRY_WEB_HOST = "0.0.0.0"
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    "http": "%s:%s" % (SENTRY_WEB_HOST, SENTRY_WEB_PORT),
    "protocol": "uwsgi",
    # This is needed in order to prevent https://github.com/getsentry/sentry/blob/c6f9660e37fcd9c1bbda8ff4af1dcfd0442f5155/src/sentry/services/http.py#L70
    "uwsgi-socket": None,
    "so-keepalive": True,
    # Keep this between 15s-75s as that's what Relay supports
    "http-keepalive": 15,
    "http-chunked-input": True,
    # the number of web workers
    "workers": 3,
    "threads": 4,
    "memory-report": False,
    # Some stuff so uwsgi will cycle workers sensibly
    "max-requests": 100000,
    "max-requests-delta": 500,
    "max-worker-lifetime": 86400,
    # Duplicate options from sentry default just so we don't get
    # bit by sentry changing a default value that we depend on.
    "thunder-lock": True,
    "log-x-forwarded-for": False,
    "buffer-size": 32768,
    "limit-post": 209715200,
    "disable-logging": True,
    "reload-on-rss": 600,
    "ignore-sigpipe": True,
    "ignore-write-errors": True,
    "disable-write-exception": True,
}

###########
# SSL/TLS #
###########

# If you're using a reverse SSL proxy, you should enable the X-Forwarded-Proto
# header and enable the settings below

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# USE_X_FORWARDED_HOST = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# End of SSL/TLS settings

########
# Mail #
########

SENTRY_OPTIONS["mail.list-namespace"] = env('SENTRY_MAIL_HOST', 'localhost')
SENTRY_OPTIONS["mail.from"] = f"sentry@{SENTRY_OPTIONS['mail.list-namespace']}"

############
# Features #
############

SENTRY_FEATURES["projects:sample-events"] = False
SENTRY_FEATURES.update(
    {
        feature: True
        for feature in (
        "organizations:discover",
        "organizations:events",
        "organizations:global-views",
        "organizations:incidents",
        "organizations:integrations-issue-basic",
        "organizations:integrations-issue-sync",
        "organizations:invite-members",
        "organizations:metric-alert-builder-aggregate",
        "organizations:sso-basic",
        "organizations:sso-rippling",
        "organizations:sso-saml2",
        "organizations:performance-view",
        "organizations:advanced-search",
        "projects:custom-inbound-filters",
        "projects:data-forwarding",
        "projects:discard-groups",
        "projects:plugins",
        "projects:rate-limits",
        "projects:servicehooks",
    )
    }
)

#######################
# MaxMind Integration #
#######################

GEOIP_PATH_MMDB = '/geoip/GeoLite2-City.mmdb'

#########################
# Bitbucket Integration #
#########################

# BITBUCKET_CONSUMER_KEY = 'YOUR_BITBUCKET_CONSUMER_KEY'
# BITBUCKET_CONSUMER_SECRET = 'YOUR_BITBUCKET_CONSUMER_SECRET'

####################
# LDAP Integration #
####################
SENTRY_USE_LDAP = env('SENTRY_USE_LDAP', True)

if SENTRY_USE_LDAP:
    import ldap
    from django_auth_ldap.config import (
        GroupOfNamesType,
        GroupOfUniqueNamesType,
        LDAPSearch,
        NestedGroupOfNamesType,
        PosixGroupType,
    )

    AUTH_LDAP_SERVER_URI = 'ldap://corp.yadro.com:389'
    AUTH_LDAP_BIND_DN = 'LDAPLookUpUser-spb'
    AUTH_LDAP_BIND_PASSWORD = 'Ue!ng#eeveeCh7r'

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        'dc=corp,dc=yadro,dc=com',
        ldap.SCOPE_SUBTREE,
        '(objectClass=top)',
    )
    AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

    AUTH_LDAP_CONNECTION_OPTIONS = {ldap.OPT_REFERRALS: 0}

    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        'dc=corp,dc=yadro,dc=com',
        ldap.SCOPE_SUBTREE,
        '(sAMAccountName=%(user)s)',  # noqa: WPS323
    )

    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }

    AUTH_LDAP_DEFAULT_SENTRY_ORGANIZATION = u'Yadro'
    AUTH_LDAP_SENTRY_ORGANIZATION_ROLE_TYPE = 'member'
    AUTH_LDAP_SENTRY_SUBSCRIBE_BY_DEFAULT = True
    AUTH_LDAP_SENTRY_ORGANIZATION_GLOBAL_ACCESS = True

    ldap_is_active = env('LDAP_GROUP_ACTIVE', "CN=msk-all@yadro.com,CN=Users,DC=corp,DC=yadro,DC=com")
    ldap_is_superuser = env('LDAP_GROUP_SUPERUSER', "CN=msk-all@yadro.com,CN=Users,DC=corp,DC=yadro,DC=com")
    ldap_is_staff = env('LDAP_GROUP_STAFF', "CN=msk-all@yadro.com,CN=Users,DC=corp,DC=yadro,DC=com")

    if ldap_is_active or ldap_is_superuser or ldap_is_staff:
        AUTH_LDAP_USER_FLAGS_BY_GROUP = {
            'is_active': ldap_is_active,
            'is_superuser': ldap_is_superuser,
            'is_staff': ldap_is_staff,
        }

    # Cache group memberships for an hour to minimize LDAP traffic
    AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True
    AUTH_LDAP_ALWAYS_UPDATE_USER = True
    AUTH_LDAP_FIND_GROUP_PERMS = True
    # AUTH_LDAP_CACHE_GROUPS = False
    AUTH_LDAP_CACHE_GROUPS = env('LDAP_CACHE_GROUPS', True)
    AUTH_LDAP_GROUP_CACHE_TIMEOUT = env('LDAP_GROUP_CACHE_TIMEOUT', 3600)

    AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
        'sentry_ldap_auth.backend.SentryLdapBackend',
    )

    # setup logging for django_auth_ldap
    import logging

    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    ldap_loglevel = getattr(logging, env('LDAP_LOGLEVEL', 'DEBUG'))
    logger.setLevel(ldap_loglevel)
    LOGGING['overridable'] = ['sentry', 'django_auth_ldap']
    LOGGING['loggers']['django_auth_ldap'] = {
        'handlers': ['console'],
        'level': 'DEBUG'
    }
