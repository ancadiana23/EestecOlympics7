#!/bin/bash
for file in *.jpg
do
	echo $file
	convert $file -resize 20x30! $file
	convert $file -colorspace Gray $file
done

