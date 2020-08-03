#!/bin/bash

declare -a bar=("alpha" "bravo" "charlie")
declare -a foo=("delta" "echo" "foxtrot" "golf")

declare -a groups=("bar" "foo")

for group in "${groups[@]}"; do
    val="$group[0]"; echo "${!val}"
    val="$group[1]"
    echo "${!val}"
    #echo "group name: ${group} with group members: ${!lst}"
    #for element in "${!lst}"; do
    #    echo -en "\tworking on $element of the $group group\n"
    #done
done
