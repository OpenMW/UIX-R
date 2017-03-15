#!/usr/bin/env bash

# create screnshots of NIFs with nifskope
find . -iname "*.nif" | while read f;
do
  echo ${f};
  DIR=album/$(dirname "${f}")
  echo ${DIR}
  mkdir -p "$DIR" # create directories
  nifskope "${f}"& sleep 3; # open nifskope with NIF
  wmctrl -c nifskope; sleep 2; # close the PNG ICCC warning window
  wmctrl -a nifskope; # raise nifskope to top
  gnome-screenshot -w -d 1 -f "album/${f}.png"  # screenshot top window
  wmctrl -c nifskope; wmctrl -c nifskope; # close any open nifskope windows
done

# find any screenshots that are incorrect and try to retake them
find ./album -name '*.png' -exec file {} \; | sed 's/\(.*png\): .* \([0-9]* x [0-9]*\).*/\2 \1/' | awk 'int($1) == 1202 {print}' | while read f;
do
  f=${f:19:-4}
  echo ${f};
  DIR=album/$(dirname "${f}")
  echo ${DIR}
  mkdir -p "$DIR"
  nifskope "${f}"& sleep 3;
  wmctrl -c nifskope; sleep 2;
  wmctrl -a nifskope;
  gnome-screenshot -w -d 1 -f "album/${f}.png"
  wmctrl -c nifskope; wmctrl -c nifskope;
done

