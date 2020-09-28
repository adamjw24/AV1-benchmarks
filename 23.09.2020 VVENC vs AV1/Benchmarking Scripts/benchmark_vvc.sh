#!/bin/bash

for cpu in faster fast medium slow; do
    for i in 40 37 34 31 28 25 22; do
    cat <<EOF
runtime=\$(vvencapp -i "$1" --size 1920x1080 --framerate 50 --format yuv420_10 --output vvc${i}_${cpu}.vvc --preset ${cpu} --qp ${i} --threads 4 --qpa 0 --intraperiod 48) && vvdecapp -b vvc${i}_${cpu}.vvc -o vvc${i}_${cpu}.yuv &> /dev/null && ffmpeg -y -hide_banner -loglevel panic -r 50 -s 1920x1080 -pix_fmt yuv420p10le -i vvc${i}_${cpu}.yuv -r 50 -s 1920x1080 -pix_fmt yuv420p10le -i "$1" -filter_complex libvmaf=eof_action=endall:psnr=1:ssim=1:ms_ssim=1:log_path=${i}_${cpu}.json:log_fmt=json -f null - && rm vvc${i}_${cpu}.yuv && printf "('vvc', %s, '%s', %d, %s, %s, %s, %s, %s)," "\$(echo "\$runtime" | awk '/Total Time/{print \$3}')" "$cpu" "$i" "\$(echo "\$runtime" | awk '/Bitrate/{getline; print \$3}')" "\$(jq '.["VMAF score"]' "${i}_${cpu}.json")" "\$(jq '.["PSNR score"]' "${i}_${cpu}.json")" "\$(jq '.["SSIM score"]' "${i}_${cpu}.json")" "\$(jq '.["MS-SSIM score"]' "${i}_${cpu}.json")" | tee -a "vvc_${1}data.txt"
EOF
    done
done | parallel -u -j 2
