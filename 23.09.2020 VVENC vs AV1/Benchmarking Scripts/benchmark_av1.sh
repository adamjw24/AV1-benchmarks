j=0

#for cpu in 6 5 4 3 2 1 0 ; do
for cpu in 0 ; do
    for i in 63 58 53 48 43 38 ; do
cat <<EOF
        runtime=\$(av1an -fmt yuv420p10le -p 1 -s 0 -i "${1}" -v " --threads=4 --end-usage=q --cq-level=$i --cpu-used=${cpu} " --temp aom${cpu}_${i} -o "aom${cpu}_${i}" | grep Finished | cut -d' ' -f2 | tr -d '[:alpha:]'); \
        ffmpeg -nostdin -r 50 -i "aom${cpu}_${i}.mkv" -r 50 -i "${1}" -filter_complex "libvmaf=psnr=1:ssim=1:ms_ssim=1:log_path=aom${cpu}_${i}.json:log_fmt=json" -f null - 2> /dev/null; \
        printf "('%s', %s, %s, %s, %s, %s, %s, %s, %s)," \
            "aom" \
            "\$runtime" \
            "${cpu}" \
            "$i" \
            "\$(ffprobe -i aom${cpu}_${i}.mkv 2>&1 | grep bitrate | rev | cut -d' ' -f2 | rev)" \
            "\$(jq '.["VMAF score"]' aom${cpu}_${i}.json)" \
            "\$(jq '.["PSNR score"]' aom${cpu}_${i}.json)" \
            "\$(jq '.["SSIM score"]' aom${cpu}_${i}.json)" \
            "\$(jq '.["MS-SSIM score"]' aom${cpu}_${i}.json)" | \
            tee -a "aom_${1}data.txt"; \
        echo
EOF
    done
done | parallel -u -j 2
