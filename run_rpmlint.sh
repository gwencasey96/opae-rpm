#!/bin/sh

date
cat /etc/redhat-release

dist=fc31
ver=3

cd ~/rpmbuild/SRPMS
echo "opae-1.4.0-${ver}.${dist}.src.rpm"
rpmlint opae-1.4.0-${ver}.${dist}.src.rpm

cd ~/rpmbuild/RPMS/x86_64
R="opae-1.4.0-${ver}.${dist}.x86_64.rpm \
   opae-debuginfo-1.4.0-${ver}.${dist}.x86_64.rpm \
   opae-debugsource-1.4.0-${ver}.${dist}.x86_64.rpm  \
   opae-devel-1.4.0-${ver}.${dist}.x86_64.rpm \
   opae-devel-debuginfo-1.4.0-${ver}.${dist}.x86_64.rpm"


for r in $R; do
    echo "$r"
    rpmlint $r
done


