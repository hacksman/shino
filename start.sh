if [ -z $1 ]
then
  echo '⚠️ start failed: u must be set run env. eg: sh run.sh debug.'
else
  echo 'start check db'
  python shino/check.py --env $1
  echo 'db is ok'
  echo 'start create table system need'
  python shino/gentable.py --env $1
  echo 'table system need create success'

  server_names=("saver" "cleaner" "extractor" "downloader" "seed_generator")

  for server in ${server_names[@]}
    do
      echo "start shino.$server"
      nohup python -m shino.$server --env $1 > /dev/null 2>&1 &
    done
fi
exit