"""
Migration script to add a new table named `oidc_rp` for authentication and authorization.
"""
from __future__ import print_function

import logging

from sqlalchemy import Column, ForeignKey, Integer, MetaData, Table, TEXT, VARCHAR

log = logging.getLogger(__name__)
metadata = MetaData()

social_auth_association = Table(
    "social_auth_association", metadata,
    Column('id', Integer, primary_key=True),
    Column('server_url', VARCHAR(255)),
    Column('handle', VARCHAR(255)),
    Column('secret', VARCHAR(255)),
    Column('issued', Integer),
    Column('lifetime', Integer),
    Column('assoc_type', VARCHAR(64)))


social_auth_code = Table(
    "social_auth_code", metadata,
    Column('id', Integer, primary_key=True),
    Column('email', VARCHAR(200)),
    Column('code', VARCHAR(32)))


psa_nonce = Table(
    "psa_nonce", metadata,
    Column('id', Integer, primary_key=True),
    Column('server_url', VARCHAR(255)),
    Column('timestamp', Integer),
    Column('salt', VARCHAR(40)))


social_auth_partial = Table(
    "social_auth_partial", metadata,
    Column('id', Integer, primary_key=True),
    Column('token', VARCHAR(32)),
    Column('data', TEXT),
    Column('next_step', Integer),
    Column('backend', VARCHAR(32)))


oidc_rp_user_authnz_tokens = Table(
    "oidc_rp_user_authnz_tokens", metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("galaxy_user.id"), index=True),
    Column('uid', VARCHAR(255)),
    Column('provider', VARCHAR(32)),
    Column('extra_data', TEXT),
    Column('lifetime', Integer),
    Column('assoc_type', VARCHAR(64)))


def upgrade(migrate_engine):
    print(__doc__)
    metadata.bind = migrate_engine
    metadata.reflect()

    # Create UserOAuth2Table
    try:
        social_auth_association.create()
        social_auth_code.create()
        psa_nonce.create()
        social_auth_partial.create()
        oidc_rp_user_authnz_tokens.create()
    except Exception as e:
        log.exception("Creating UserOAuth2 table failed: %s" % str(e))


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()

    # Drop UserOAuth2Table
    try:
        social_auth_association.drop()
        social_auth_code.drop()
        pas_nonce.drop()
        social_auth_partial.drop()
        oidc_rp_user_authnz_tokens.drop()
    except Exception as e:
        log.exception("Dropping UserOAuth2 table failed: %s" % str(e))
