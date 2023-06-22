# Cisco-ASA-Config-Compare

This script can be used to automate comparing configuration changes on a firewall over a span of time. The script is currently configured to compare to a "template" or single version of a firewall configuration to the current version, but can easily be modified to compare daily revisions. The script uses the python library conf-diff to do the comparisons. conf-diff is a great library to quickly compare files and report differences. You can check out the creater of the library here: https://github.com/muhammad-rafi
