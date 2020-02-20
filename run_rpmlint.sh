#!/bin/sh

date
cat /etc/redhat-release

cd ~/rpmbuild/SRPMS
echo "opae-1.4.0-1.src.rpm"
rpmlint opae-1.4.0-1.src.rpm

cd ~/rpmbuild/RPMS/x86_64
R="opae-1.4.0-1.x86_64.rpm \
   opae-debuginfo-1.4.0-1.x86_64.rpm \
   opae-debugsource-1.4.0-1.x86_64.rpm  \
   opae-devel-1.4.0-1.x86_64.rpm \
   opae-samples-1.4.0-1.x86_64.rpm \
   opae-samples-debuginfo-1.4.0-1.x86_64.rpm  \
   opae-tools-1.4.0-1.x86_64.rpm \
   opae-tools-debuginfo-1.4.0-1.x86_64.rpm \
   opae-tools-extra-1.4.0-1.x86_64.rpm \
   opae-tools-extra-debuginfo-1.4.0-1.x86_64.rpm"

for r in $R; do
    echo "$r"
    rpmlint $r
done


