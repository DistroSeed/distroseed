#!/bin/bash
current_dir=${pwd}
# rsync all torrent files and exclude everything else
rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' rsync://mirrors.kernel.org/mirrors/ ${pwd}/tmp/
# move those torrent files back to the root directory of the folder
find ${pwd}/tmp/ -regex ".*\.torrent" -exec cp '{}' ${pwd}/torrents/ \;
