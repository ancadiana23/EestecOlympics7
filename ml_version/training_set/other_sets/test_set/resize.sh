#!/bin/bash
for i in 1 2
do
	for file in $i/*.png $i/*.jpg
	do
		convert $file -colorspace Gray $file
	done
done
