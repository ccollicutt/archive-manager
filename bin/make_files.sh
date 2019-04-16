#!/bin/sh

root=/var/tmp/archive-manager-backup
b1=$root/backup-1
b2=$root/backup-2

rm -rf $root
echo "Creating $root"
mkdir $root
mkdir $b1 
mkdir $b2

for i in $(seq 0 99); do
    echo "Creating $b1/$i-test.tar.gz"
    echo "Creating $b2/$i-test.tar.gz"
    fallocate -l 10240 $b1/$i-test.tar.gz
    fallocate -l 10240 $b2/$i-test.tar.gz
    #sleep 0.1
done

ls $root/*