#!/bin/sh

date
cat /etc/redhat-release

dist=fc31
ver=4

cd ~/rpmbuild/SRPMS
mock --verbose opae-1.4.0-${ver}.${dist}.src.rpm

