# CPU information

`cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c`

# the number of physical CPUs

`cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l`

# the number of cores in each physical CPU (the number of cores)

`cat /proc/cpuinfo| grep "cpu cores"| uniq`

# the number of logical CPUs

`cat /proc/cpuinfo| grep "processor"| wc -l`

