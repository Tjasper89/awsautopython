#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron: Deploy websotes with AWS

Webotron automates the process of deploying static websites to AWS.
- Configure AWS S3 buckets
 - Create them
 - Set them up for static website hosting
 - Deply local files to them
- Configure DNS with AWS Route 53
- Configure a CDN and SSL with AWS CloudFront
"""


import boto3
import click

from bucket import BucketManager

session = boto3.Session(profile_name='pythonauto')
bucket_manager = BucketManager(session)


@click.group()
def cli():
    """Webotron deploys websites to AWS"""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all s3 list_buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_buckets_objects(bucket):
    """List objects in a s3 bucket"""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure a S3 bucket"""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)


    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync cotents of PATHNAME to BUCKET"""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
