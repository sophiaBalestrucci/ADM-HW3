awk -F'\t' '{print $8}' data2.tsv > first.tsv #consider only 8th field
echo 'How many places can be found in each country?'
echo 'Italy'
awk -F'\t' '{s+=gsub(/Italy/,"Italy")} END {print s}' first.tsv 
echo 'Spain'
awk -F'\t' '{s+=gsub(/Spain/,"Spain")} END {print s}' first.tsv
echo 'France'
awk -F'\t' '{s+=gsub(/France/,"France")} END {print s}' first.tsv
echo 'England'
awk -F'\t'  '{s+=gsub(/England/,"England")} END {print s}' first.tsv
echo 'United States'
awk -F'\t' '{s+=gsub(/United States/,"United States")} END {print s}' first.tsv
echo 'How many people, on average, have visited the places in each country?'
echo 'Italy'
awk -F'\t' '{print $3 $8}' data2.tsv > second.tsv
grep 'Italy' second.tsv | awk '{ total += $1 } END { print int(total/NR) }'
echo 'Spain'
grep 'Spain' second.tsv | awk '{ total += $1 } END { print int(total/NR) }'
echo 'France'
grep 'France' second.tsv | awk '{ total += $1 } END { print int(total/NR) }'
echo 'England'
grep 'England' second.tsv | awk '{ total += $1 } END { print int(total/NR) }'
echo 'United States'
grep 'United States' second.tsv | awk '{ total += $1 } END { print int(total/NR) }'
echo 'How many people in total want to visit the places in each country?'
echo 'Italy'
awk -F'\t' '{print $4 $8}' data2.tsv > third.tsv
echo 'Italy'
grep 'Italy' third.tsv | awk -F'\t' '{sum+=$1} END {print sum}'
echo 'Spain'
grep 'Spain' third.tsv | awk -F'\t' '{sum+=$1} END {print sum}'
echo 'France'
grep 'France' third.tsv | awk -F'\t' '{sum+=$1} END {print sum}'
echo 'England'
grep 'England' third.tsv | awk -F'\t' '{sum+=$1} END {print sum}'
echo 'United States'
grep 'United States' third.tsv | awk -F'\t' '{sum+=$1} END {print sum}'
