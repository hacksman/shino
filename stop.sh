server_names=("seed_generator" "downloader" "extractor" "cleaner" "saver")

for server in ${server_names[@]};
do
  server_pids=`ps -ef | grep shino.$server | grep -v grep | awk '{print $2}'`
  if [ "$server_pids" ]
  then
    kill -TERM $server_pids
    echo "stop shino.$server"
  else
    echo "shino.$server is not running..."
  fi
done
