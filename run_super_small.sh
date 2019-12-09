# Create new file name with time stamp:
time_stamp=$(date +%Y%m%d%H%M)
file_name="${time_stamp}_run_history"
file_name_path="history/$file_name.txt"
# Write file id in first line of txt file:
echo $file_name > $file_name_path
echo "benchmark.sh is running..."
# Write output of benchmark.sh in txt file:
bash benchmark_super_small.sh >> $file_name_path
# Print output of benchmark:
cat $file_name_path
# Save data in csv file:
python3 history/process_history.py < $file_name_path