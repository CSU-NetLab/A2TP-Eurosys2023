cat ../datasample/job_A.txt | awk '{if($1=="Thr") print $2}' > thr_A.txt
cat ../datasample/job_B.txt | awk '{if($1=="Thr") print $2}' > thr_B.txt
cat ../datasample/switch.txt | awk '{if($1=="appID[1]") print $3}' > occ_A.txt
cat ../datasample/switch.txt | awk '{if($1=="appID[2]") print $3}' > occ_B.txt

python gencsv.py